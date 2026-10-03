# -*- coding: utf-8 -*-
u"""Ссылки внутри /verification/ ведут туда, куда обещают - измерением.

Зачем. Страница подписей /verification/documents/ была написана при v1 и
пережила пять подписей подряд: говорила «54 документа», а её ссылки вели в
403. Ни одна проверка этого не видела, потому что ссылки внутри
/verification/ никто не мерил, а сама страница строила их скриптом.

Что проверяет. Обходит все *.html под _v2/verification/, собирает каждый
href и src и для местных ссылок требует:

- файл существует в _v2/ (ссылка не выходит за его пределы);
- ссылка на каталог - провал, если в каталоге нет index.html: просмотр
  каталогов в nginx выключен, такая ссылка отдаёт 403;
- в ссылке нет шаблона JavaScript (`${...}`): такую ссылку статически не
  проверить, и именно так прежняя страница прятала битые адреса.

С ключом --live каждая уникальная местная ссылка запрашивается у боевого
сайта и обязана отдать 200. Внешние ссылки (Polygonscan, gpg4win) не
проверяются: их доступность - не наша вёрстка.

С ключом --selftest проверка гоняется на подложенной странице с заведомо
битыми ссылками и обязана их найти; с --live заодно запрашивается заведомо
несуществующий адрес. Проверка, которая не умеет падать, ничего не мерит.

Запуск:  python _tools/v2/verification_links.py [--live] [--selftest]
Выход:   0 - битых нет; 1 - есть битые (или самопроверка не поймала подлог).
"""
import io
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from urllib.parse import unquote, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
assert os.path.isdir(TOOLS), u'нет каталога %s' % TOOLS
sys.path.insert(0, TOOLS)

from build_site_docs import SITE        # noqa: E402
V2 = os.path.join(SITE, '_v2')
VERIF = os.path.join(V2, 'verification')
ORIGIN = 'https://earth-lings.org'

ATTR = re.compile(r'''\b(?:href|src)\s*=\s*(["'])(.*?)\1''', re.I | re.S)


def pages():
    out = []
    for root, _dirs, files in os.walk(VERIF):
        for f in files:
            if f.lower().endswith('.html'):
                out.append(os.path.join(root, f))
    return sorted(out)


def links_of(text):
    return [unescape(m.group(2)).strip() for m in ATTR.finditer(text)]


def is_external(h):
    return bool(re.match(r'^[a-z][a-z0-9+.-]*:', h, re.I)) or h.startswith('//')


def judge(page, h):
    u"""None - ссылка в порядке; иначе строка с причиной. Второе значение -
    путь от корня сайта для запроса --live (или None)."""
    if '${' in h or '{{' in h:
        return u'шаблон JavaScript, статически не проверить', None
    if not h or h.startswith('#') or is_external(h):
        return None, None
    path = unquote(urlsplit(h).path)
    if not path:
        return None, None
    if path.startswith('/'):
        target = os.path.normpath(os.path.join(V2, path.lstrip('/')))
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(page), path))
    v2n = os.path.normcase(os.path.normpath(V2))
    if not os.path.normcase(target).startswith(v2n):
        return u'выходит за пределы _v2', None
    rel = os.path.relpath(target, V2).replace(os.sep, '/')
    if os.path.isdir(target) or path.endswith('/'):
        if not os.path.isfile(os.path.join(target, 'index.html')):
            return u'каталог без index.html (на сайте 403)', None
        return None, '/' + (rel + '/' if rel != '.' else '')
    if not os.path.isfile(target):
        return u'файла нет', None
    return None, '/' + rel


def scan(items):
    u"""items: [(путь страницы, текст)]. Возвращает (ссылок, битые, адреса)."""
    total, bad, urls = 0, [], set()
    for page, text in items:
        for h in links_of(text):
            total += 1
            why, url = judge(page, h)
            if why:
                bad.append((os.path.relpath(page, V2).replace(os.sep, '/'), h, why))
            elif url:
                urls.add(url)
    return total, bad, urls


def status(url, tries=5):
    u"""Код ответа сайта. Обрыв соединения повторяется до пяти раз с растущей
    паузой: первый прогон шёл в 16 потоков и получил 106 обрывов на адресах,
    которые поодиночке отдают 200. Трёх попыток за шесть секунд тоже не хватало -
    2026-10-03 на 1708 адресах срывалось один-два, и каждый раз другие. Повтор
    трогает только сорвавшиеся адреса, поэтому пять попыток почти ничего не
    стоят. HTTP-код не повторяется: 404 - это ответ."""
    req = urllib.request.Request(ORIGIN + url, method='HEAD',
                                 headers={'User-Agent': 'earthlings-verification-links'})
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception as e:                   # noqa: BLE001
            last = u'%s: %s' % (type(e).__name__, getattr(e, 'reason', e))
            time.sleep(2 * (2 ** i))
    return last


def live(urls):
    urls = sorted(urls)
    # Четыре потока, а не шестнадцать: сервер рвёт соединения при напоре,
    # и проверка мерила бы его ограничение, а не ссылки.
    with ThreadPoolExecutor(max_workers=4) as ex:
        codes = list(ex.map(status, urls))
    return [(u, c) for u, c in zip(urls, codes) if c != 200]


def selftest(with_live):
    fake = os.path.join(VERIF, '__selftest__.html')
    text = (u'<a href="no-such-file.asc">x</a> <a href="documents/en/">dir</a> '
            u'<a href="${filePath}">tpl</a> <a href="index.html">ok</a>')
    _t, bad, _u = scan([(fake, text)])
    ok = len(bad) == 3
    print(u'самопроверка: подложено 3 битых ссылки и 1 исправная, найдено битых %d - %s'
          % (len(bad), u'ловит' if ok else u'НЕ ЛОВИТ'))
    for _p, h, why in bad:
        print(u'    %-22s %s' % (h, why))
    if with_live:
        code = status('/verification/no-such-file-%d.asc' % os.getpid())
        lok = code != 200
        print(u'самопроверка --live: заведомо несуществующий адрес отдал %s - %s'
              % (code, u'ловит' if lok else u'НЕ ЛОВИТ'))
        ok = ok and lok
    return ok


def main():
    with_live = '--live' in sys.argv
    if '--selftest' in sys.argv:
        ok = selftest(with_live)
        print(u'verification links selftest: %s' % (u'ok' if ok else u'FAILED'))
        return 0 if ok else 1

    ps = pages()
    assert ps, u'под %s нет ни одной страницы' % VERIF
    items = [(p, io.open(p, encoding='utf-8', errors='replace').read()) for p in ps]
    total, bad, urls = scan(items)
    assert total > 0, u'ни одной ссылки - разбор сломался'
    for page, h, why in bad[:30]:
        print(u'  БИТАЯ  %s: %s - %s' % (page, h, why))
    live_bad = []
    if with_live:
        live_bad = live(urls)
        for u, c in live_bad[:30]:
            print(u'  LIVE   %s -> %s' % (u, c))
    print(u'verification links: pages=%d links=%d local_unique=%d broken=%d%s'
          % (len(ps), total, len(urls), len(bad),
             u' live_checked=%d live_not_200=%d' % (len(urls), len(live_bad)) if with_live else u''))
    return 1 if bad or live_bad else 0


if __name__ == '__main__':
    sys.exit(main())
