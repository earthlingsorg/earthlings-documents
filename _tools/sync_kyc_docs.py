# -*- coding: utf-8 -*-
u"""Переносит копии документов корпуса в earthlings-kyc из дерева `_v2`.

Зачем. `id.earth-lings.org` держит свои копии части документов, и до
2026-08-26 они синхронизировались вручную - то есть не синхронизировались.
Живая `ru01.html` отдавала 4076 слов при 7375 в мастере: редакцию Декларации
ДО пересборки 5 июля. Человек ставил галочку «прочитал и подписываю» под
текстом, вытесненным из корпуса почти два месяца назад.

Решение Артура 2026-08-26: заменить копии текстом из `_v2`.

**Переносится ТЕЛО документа, а не страница целиком.** Страница `_v2` несёт
меню и подвал сайта со ссылками на `earth-lings.org`; поставить их на домен
регистрации значило бы завести там навигацию чужого сайта. Берётся только
`<main class="statute">`, и он кладётся в свою оболочку.

**Имена файлов не меняются.** `ru01.html` остаётся `ru01.html`: на эти адреса
ведут ссылки со страницы проверки личности и из писем.

**Канонический адрес ведёт на сайт, а не на `id.`** Один и тот же текст на
двух доменах - это дубль для поисковика, и первичным должен быть сайт.

**Что скрипт НЕ делает.** Не выкатывает на сервер и не решает, что сказать
подписавшим прежнюю редакцию. Первое делает cron, второе - человек.

Запуск:  python _tools/sync_kyc_docs.py [--dry]
"""
import io
import os
import re
import shutil
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
KYC = os.environ.get('EARTHLINGS_KYC') or os.path.join(
    os.path.dirname(REPO), 'earthlings-kyc')

sys.path.insert(0, TOOLS)
import build_site_docs as B                       # noqa: E402

ORIGIN = 'https://earth-lings.org'

# Стили новой темы, без которых тело документа рисуется голым текстом.
# chrome.css берётся тоже: он задаёт шрифты и фон страницы, а не только меню.
CSS = [('tokens.css', 'earthlings-tokens.css'),
       ('chrome.css', 'earthlings-chrome.css'),
       ('doc.css', 'earthlings-doc.css')]

UMAMI = ('<!--umami-start--><script>if(window.self===window.top){'
         'var s=document.createElement("script");s.defer=true;'
         's.src="https://stats.earth-lings.org/script.js";'
         's.setAttribute("data-website-id","badb2091-1880-4933-bf4e-8d7be1f7ce44");'
         'document.body.appendChild(s);}</script><!--umami-end-->')


def meta(src, pattern):
    m = re.search(pattern, src)
    return m.group(1) if m else ''


def page(lang, rtl, title, desc, canonical, body):
    u"""Оболочка копии: без меню и подвала сайта, со стилями новой темы."""
    o = ['<!DOCTYPE html>',
         '<html lang="%s"%s>' % (lang, ' dir="rtl"' if rtl else ''),
         '<head>',
         '<meta charset="UTF-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>%s</title>' % title,
         '<meta name="description" content="%s">' % desc,
         # Первичный адрес текста - сайт. На id. он лежит копией для того,
         # кто читает его перед подписанием, и в выдаче дублем быть не должен.
         '<link rel="canonical" href="%s">' % canonical,
         '<meta name="robots" content="noindex, follow">']
    for _, dst in CSS:
        o.append('<link rel="stylesheet" href="/css/%s">' % dst)
    o += ['</head>', '<body>', body, UMAMI, '</body>', '</html>']
    return '\n'.join(o) + '\n'


def main():
    dry = '--dry' in sys.argv
    root = os.path.join(KYC, 'app', 'public', 'documents')
    assert os.path.isdir(root), root

    rows, done, skipped = [], 0, 0
    for lang in sorted(os.listdir(root)):
        d = os.path.join(root, lang)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            m = re.fullmatch(r'%s([0-9]{2})\.html' % lang, fn)
            if not m:
                continue
            num = m.group(1)
            if lang not in B.SLUGS:
                rows.append((fn, u'пропуск: у языка нет слагов (хинди)'))
                skipped += 1
                continue
            src = os.path.join(SITE, '_v2', 'documents', lang,
                               B.doc_file(num, lang))
            if not os.path.isfile(src):
                rows.append((fn, u'пропуск: нет страницы в _v2'))
                skipped += 1
                continue

            s = io.open(src, encoding='utf-8').read()
            i = s.find('<main class="statute"')
            j = s.find('</main>')
            assert i > 0 and j > i, (fn, u'в странице _v2 не найден <main>')
            body = s[i:j + len('</main>')]

            # Ссылки внутри документа ведут на сайт, а не на домен регистрации:
            # на id. каталога /documents/ru/ нет, и относительный адрес дал бы
            # 404 прямо из текста Декларации.
            body = re.sub(r'href="/(?!/)', 'href="%s/' % ORIGIN, body)
            assert 'href="/' not in body, (fn, u'остался относительный адрес')

            out = page(
                lang,
                ' dir="rtl"' in re.search(r'<html[^>]*>', s).group(0),
                meta(s, r'<title>([^<]*)</title>'),
                meta(s, r'<meta name="description" content="([^"]*)"'),
                ORIGIN + B.doc_href(num, lang),
                body)

            old = io.open(os.path.join(d, fn), encoding='utf-8',
                          errors='replace').read()
            if not dry:
                io.open(os.path.join(d, fn), 'w', encoding='utf-8',
                        newline='\n').write(out)
            rows.append((fn, u'%d КБ -> %d КБ' % (len(old) // 1024,
                                                  len(out) // 1024)))
            done += 1

    # Стили. Без них тело документа - голый текст.
    for srcname, dstname in CSS:
        a = os.path.join(SITE, '_v2', 'css', srcname)
        b = os.path.join(KYC, 'app', 'public', 'css', dstname)
        assert os.path.isfile(a), a
        if not dry:
            shutil.copyfile(a, b)
        rows.append((dstname, u'стиль скопирован, %d КБ'
                     % (os.path.getsize(a) // 1024)))

    print('')
    print(u'СИНК КОПИЙ КОРПУСА В KYC%s' % (u'  (--dry, ничего не записано)'
                                           if dry else ''))
    print('=' * 66)
    for name, note in rows:
        print(u'  %-18s %s' % (name, note))
    print('=' * 66)
    print(u'перенесено: %d, пропущено: %d' % (done, skipped))
    assert done, u'не перенесено ни одного документа - проверьте пути'
    return 0


if __name__ == '__main__':
    sys.exit(main())
