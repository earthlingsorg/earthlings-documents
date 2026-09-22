# -*- coding: utf-8 -*-
u"""Страница ненайденного - одна на девять языков.

Зачем она вообще. В `_v2` её не было, и после подмены корня несуществующий
адрес отдавал бы страницу сервера по умолчанию - без обвязки, без языков и
без единой ссылки обратно. Читатель, пришедший по устаревшей ссылке из
письма, оказывался бы в тупике.

Почему одна, а не девять. Nginx отдаёт один файл на `error_page 404`, и язык
запроса ему в этот момент неизвестен. Разложить страницу по языкам можно
только правилом в конфигурации боевого сервера, а он до подмены не
правится. Одна страница делает то же самое честнее: показывает девять
выходов вместо одного угаданного.

Почему ни слова не сочинено. Строки взяты из `_tools/i18n/<язык>.json` - тех
же переводов, которыми пользуется обвязка. Формулировки «страница не
найдена» там нет ни на одном языке, и придумывать её на арабском, хинди,
грузинском и китайском значило бы завести в корпус непроверенную прозу.
Поэтому текста нет вовсе: есть число 404, имя сайта и девять ссылок,
подписанных названием языка и словом «Главная» из `nav.home`.

Запуск:  python _tools/build_404.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import site_guard as guard                       # noqa: E402
from build_site_docs import HEAD_ICONS, OG_LOCALE, UMAMI, SITE  # noqa: E402
import chrome as C                               # noqa: E402

V2 = os.path.join(SITE, '_v2')
I18N = os.path.join(HERE, 'i18n')

# Порядок тот же, что в переключателе языка обвязки: читатель, уже видевший
# список, найдёт свой язык на том же месте.
ORDER = ['ru', 'en', 'es', 'de', 'fr', 'zh', 'ar', 'hi', 'ka']


def home_word(lang):
    u"""«Главная» на этом языке. Ключ nav.home есть во всех девяти файлах;
    если он пропадёт, сборка падает, а не подставляет английское слово."""
    p = os.path.join(I18N, '%s.json' % lang)
    assert os.path.isfile(p), p
    d = json.load(io.open(p, encoding='utf-8'))
    w = (d.get('nav') or {}).get('home')
    assert w, u'нет ключа nav.home в %s' % p
    return w


def build():
    # Названия языков - из обвязки, а не списком здесь: список разошёлся бы
    # с переключателем при первом переименовании.
    names = C.LANG_LABEL
    rows = []
    for lang in ORDER:
        name = names[lang]
        rtl = ' dir="rtl"' if lang in C.RTL else ''
        rows.append(
            '<li><a href="/%s/" lang="%s"%s>'
            '<span class="langlist-lang">%s</span>'
            '<span class="langlist-title">%s</span></a></li>'
            % (lang, lang, rtl, C.esc(name), C.esc(home_word(lang))))

    return '\n'.join([
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>404 | Earthlings</title>',
        '<meta name="description" content="Page not found. '
        'Earthlings is published in nine languages - choose one.">',
        '<meta property="og:locale" content="%s">' % OG_LOCALE['en'],
        # Страница ошибки индексации не подлежит: в выдаче ей делать нечего,
        # а попав туда, она перехватывала бы запросы по имени сайта.
        '<meta name="robots" content="noindex, follow">',
        HEAD_ICONS,
        '<link rel="stylesheet" href="/css/tokens.css">',
        '<link rel="stylesheet" href="/css/chrome.css">',
        '<link rel="stylesheet" href="/css/doc.css">',
        # Из home.css странице ненайденного нужен был только список
        # языков - четыре правила из ста восьмидесяти. Он вынесен.
        '<link rel="stylesheet" href="/css/langlist.css">',
        '</head>',
        '<body>',
        '<main class="statute" id="main"><div class="sheet">',
        '<header class="doc-head">',
        '<div class="part-no">404</div>',
        '<h1 class="doc-title">Earthlings</h1>',
        '<div class="rule-double"></div>',
        '</header>',
        '<ul class="langlist">',
    ] + rows + [
        '</ul>',
        '</div></main>',
        # Счётчик на странице ошибки нужнее, чем на иной рабочей: по нему
        # видно, по каким устаревшим адресам к нам ещё ходят и какие ссылки
        # в письмах пора чинить.
        UMAMI,
        '</body>',
        '</html>',
        '',
    ])


def main():
    page = build()
    guard.write(os.path.join(V2, '404.html'), page)
    print(u'OK   _v2/404.html  %d байт, языков %d'
          % (len(page.encode('utf-8')), len(ORDER)))


if __name__ == '__main__':
    try:
        main()
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
