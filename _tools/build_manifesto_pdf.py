# -*- coding: utf-8 -*-
u"""Собирает PDF Обращения печатью страницы черновика браузером.

Источник один - `_v2/<язык>/manifest.html`, тот же файл, который встанет на
earth-lings.org/<язык>/manifest.html после подмены корня. Ничего не
дублируется: правится мастер Обращения, перезапускается build_home_v2.py,
перезапускается этот скрипт.

**Почему движок сменился.** Прежняя сборка была на reportlab: своя вёрстка,
свой шрифт, свои поля. Она давала красивый лист на семи языках и не могла дать
его на двух. reportlab кладёт кодпойнты подряд, а деванагари при отрисовке
переставляет знаки - краткое «и» пишется ПЕРЕД согласной, к которой относится, -
и арабская вязь требует соединения букв. Вывод получался бы не некрасивым, а
неправильным, и правдоподобно неправильным: чтобы заметить, надо знать язык.

Браузер это умеет: Chrome шьёт обе письменности сам. Решение Артура
2026-08-27 - пересобрать все девять одним движком, чтобы файлы были одной
семьёй, а не двумя.

**Что при этом потеряно, и это честно назвать.** Прежний PDF был набран
PT Serif на кремовом листе, вёрсткой по ширине. Повторить это на девяти языках
нельзя: PT Serif не покрывает ни деванагари, ни арабскую вязь, ни китайский,
ни грузинский. Одна семья возможна только на шрифтовой лесенке сайта, и теперь
PDF выглядит так же, как страница, с которой напечатан. Ушла и рамка-кнопка
вокруг последней строки: её рисовал прежний генератор, на странице её нет, и
дорисовывать в PDF то, чего нет в тексте, - это выдумывать.

**Что осталось от прежнего вида** - колонтитул: адрес сайта и номер страницы
внизу листа, PT Serif 8.5 пунктов. Его ставит не браузер: Chrome не понимает
`@bottom-center`. Ставится после печати, по странице за раз.

**Печатный лист** - `_v2/css/print.css`, подключён к странице. Что видит
человек, нажав Ctrl+P, то и лежит в файле.

**Откуда берутся шрифты.** `_v2` не содержит ни шрифтов письменностей, ни
картинок: в vhost для них стоит откат в общее дерево. Локальный сервер здесь
повторяет этот откат. Без него браузер получает 404 на woff2 и молча
подставляет системный шрифт - в прежнем прогоне в файл попала Nirmala UI
вместо Noto, и на другой машине тот же PDF собрался бы иначе. Поэтому 404
считаются и валят сборку.

Запуск:  python _tools/build_manifesto_pdf.py [ru|en|de|fr|es|ka|zh|ar|hi|all]
Выход:   <репозиторий сайта>/_v2/downloads/<имя из BY_LANG>

Из внешнего нужны браузер (Chrome или Edge) и PyMuPDF.
"""

import io
import os
import re
import subprocess
import sys
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import fitz

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
V2 = os.path.join(SITE, '_v2')

# Имена файлов менять нельзя: на них ведут ссылки со страниц и из писем.
# Языки нелатинских письменностей называются по-английски - так решено при
# сборке китайского и грузинского, хинди и арабский идут за ними.
BY_LANG = {
    'ru': 'obrashchenie-ru.pdf',
    'en': 'an-address-to-everyone-en.pdf',
    'de': 'eine-ansprache-an-alle-de.pdf',
    'fr': 'un-message-a-tous-fr.pdf',
    'es': 'un-mensaje-a-todos-es.pdf',
    'ka': 'an-address-to-everyone-ka.pdf',
    'zh': 'an-address-to-everyone-zh.pdf',
    'ar': 'an-address-to-everyone-ar.pdf',
    'hi': 'an-address-to-everyone-hi.pdf',
}

FOOT_FONT = os.path.join(TOOLS, 'fonts', 'PT_Serif-Web-Regular.ttf')
FOOT_TEXT = 'earth-lings.org'
FOOT_SIZE = 8.5
FOOT_COLOR = (0x5f / 255.0, 0x66 / 255.0, 0x70 / 255.0)
FOOT_UP = 34            # пунктов от низа листа

CHROMES = [
    os.environ.get('EARTHLINGS_CHROME'),
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]


def chrome_path():
    for p in CHROMES:
        if p and os.path.isfile(p):
            return p
    raise SystemExit(u'не найден браузер; укажите путь в EARTHLINGS_CHROME')


# ------------------------------------------------------------------- сервер

class Handler(SimpleHTTPRequestHandler):
    u"""Отдаёт `_v2`, при промахе - боевое дерево. Тот же откат, что в vhost."""

    misses = []

    def translate_path(self, path):
        rel = path.split('?', 1)[0].split('#', 1)[0].lstrip('/')
        rel = os.path.normpath(rel.replace('/', os.sep))
        if rel.startswith('..'):
            return os.path.join(V2, 'нет-такого')
        a = os.path.join(V2, rel)
        if os.path.exists(a):
            return a
        b = os.path.join(SITE, rel)
        if not os.path.exists(b):
            Handler.misses.append(path)
        return b

    def log_message(self, *a):
        pass


def serve():
    srv = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


# -------------------------------------------------------------- колонтитул

def page_text(src):
    u"""Видимый текст страницы: то, что обязано оказаться в PDF."""
    s = io.open(src, encoding='utf-8').read()
    i, j = s.find('<main'), s.find('</main>')
    assert i > 0 and j > i, (src, u'в странице не найден <main>')
    body = re.sub(r'<[^>]+>', ' ', s[i:j])
    body = re.sub(r'&[a-z]+;|&#\d+;', ' ', body)
    return re.sub(r'\s+', '', body)


def stamp(path):
    u"""Ставит колонтитул и приводит метаданные к постоянным.

    Chrome штампует в файл время печати, и один и тот же текст даёт разные
    байты при каждом прогоне. В репозитории это означало бы правку бинарника
    на каждом запуске - в том числе из хуков.
    """
    assert os.path.isfile(FOOT_FONT), FOOT_FONT
    doc = fitz.open(path)
    assert doc.page_count, u'в PDF ни одной страницы'
    font = fitz.Font(fontfile=FOOT_FONT)
    for i, page in enumerate(doc, 1):
        text = '%s    %d' % (FOOT_TEXT, i)
        w = font.text_length(text, FOOT_SIZE)
        page.insert_text(
            fitz.Point((page.rect.width - w) / 2, page.rect.height - FOOT_UP),
            text, fontfile=FOOT_FONT, fontname='ptserif',
            fontsize=FOOT_SIZE, color=FOOT_COLOR)
    doc.set_metadata({'producer': 'earth-lings.org', 'creator': '',
                      'title': '', 'author': '', 'subject': '',
                      'keywords': '', 'creationDate': '', 'modDate': ''})
    doc.xref_set_key(-1, 'ID', '[<00><00>]')
    # Полная пересборка файла поверх самого себя запрещена библиотекой, а
    # инкрементальная оставила бы в файле обе версии - и старую, и штампованную.
    tmp = path + '.tmp'
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    os.replace(tmp, path)
    fixed_id(path)


def fixed_id(path):
    u"""Гасит случайный идентификатор в конце файла.

    Второй элемент `/ID` библиотека пересобирает на каждом сохранении, и он
    единственное, чем два файла с одинаковым текстом отличаются друг от друга.
    Заменяется НА ТУ ЖЕ ДЛИНУ: в PDF после таблицы ссылок стоит смещение, и
    сдвиг байтов сломал бы файл.
    """
    raw = io.open(path, 'rb').read()
    m = re.search(br'/ID\s*\[\s*<([0-9A-Fa-f]*)>\s*<([0-9A-Fa-f]*)>', raw)
    if not m:
        # Библиотека пишет `/ID` не всегда. Нет его - нечего и гасить: тогда
        # случайной величины в файле не остаётся вовсе.
        return
    for g in (1, 2):
        a, b = m.span(g)
        raw = raw[:a] + b'0' * (b - a) + raw[b:]
    io.open(path, 'wb').write(raw)


# ------------------------------------------------------------------ сборка

def build(lang, port, browser):
    src = os.path.join(V2, lang, 'manifest.html')
    assert os.path.isfile(src), u'нет страницы Обращения: %s' % src
    name = BY_LANG.get(lang)
    assert name, u'язык %r не назван в BY_LANG' % lang

    out = os.path.join(V2, 'downloads', name)
    assert os.path.abspath(out).startswith(os.path.abspath(V2) + os.sep), (
        u'выход обязан лежать внутри _v2: %s' % out)
    if not os.path.isdir(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))

    Handler.misses[:] = []
    profile = tempfile.mkdtemp(prefix='earthlings-print-')
    subprocess.run(
        [browser, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
         '--user-data-dir=' + profile, '--virtual-time-budget=15000',
         '--print-to-pdf=' + out,
         'http://127.0.0.1:%d/%s/manifest.html' % (port, lang)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)

    assert not Handler.misses, (
        u'браузер не получил %d файл(ов) и подставил бы системный шрифт: %s'
        % (len(Handler.misses), ', '.join(sorted(set(Handler.misses))[:5])))
    assert os.path.isfile(out) and os.path.getsize(out) > 20000, (
        u'PDF не собрался или пуст: %s' % out)

    stamp(out)

    doc = fitz.open(out)
    pages = doc.page_count
    text = ''.join(p.get_text() for p in doc)
    doc.close()
    assert pages >= 2, u'%s: страниц всего %d - похоже, текст не дошёл' % (lang, pages)
    assert FOOT_TEXT in text, u'%s: колонтитул не встал' % lang

    # Сколько знаков «много» - зависит от письменности: китайский говорит то же
    # самое втрое короче русского. Поэтому сверяемся не с числом, а с самой
    # страницей: в PDF обязано попасть почти всё, что на ней написано.
    want = len(page_text(src))
    got = len(text) - pages * (len(FOOT_TEXT) + 5)
    assert want and got > want * 0.8, (
        u'%s: на странице %d знаков, в PDF %d - текст дошёл не весь'
        % (lang, want, got))
    return name, pages, os.path.getsize(out) // 1024


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if '--theme' in sys.argv:
        i = sys.argv.index('--theme')
        if i + 1 < len(sys.argv) and sys.argv[i + 1] in args:
            args.remove(sys.argv[i + 1])
    langs = sorted(BY_LANG) if (not args or args == ['all']) else args

    assert os.path.isdir(V2), u'нет каталога черновика: %s' % V2
    assert os.path.isdir(os.path.join(SITE, 'fonts')), (
        u'нет общего каталога шрифтов - откат для woff2 работать не будет')

    browser = chrome_path()
    srv, port = serve()
    print('')
    print(u'PDF ОБРАЩЕНИЯ: печать страниц браузером')
    print('=' * 62)
    try:
        for lang in langs:
            name, pages, kb = build(lang, port, browser)
            print(u'  %-3s %-32s %2d стр.  %3d КБ' % (lang, name, pages, kb))
    finally:
        srv.shutdown()
    print('=' * 62)
    print(u'собрано: %d' % len(langs))
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')
    sys.exit(main())
