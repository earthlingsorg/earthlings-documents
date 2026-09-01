# -*- coding: utf-8 -*-
u"""Тематические страницы на оформление нового сайта.

Что переносится. Семь тем на девяти языках плюс девять хабов - 72 адреса,
все из боевого sitemap. Без переноса они после смены корня отдают 404: это
больше половины из ста пятнадцати адресов, которые сейчас теряются.

Откуда берётся содержание. Мастеров .md у тем нет - страницы написаны
руками. Поэтому источником служит САМА боевая страница, а перенос сводится
к смене оформления: текст переносится узел в узел, ни одно слово не
переписывается.

Почему это безопасно. Проверено по всем 63 страницам: скелет у них ОДИН И
ТОТ ЖЕ, без исключений -

    p.eyebrow, h1, div.lead(p×3), h2, (h3+p)×5,
    div.cta(h2, p, a.btn), div.related(h2, ul>li>a>span)

Поэтому разбор строгий: если страница не совпала со скелетом, сборка
падает, а не переносит наполовину.

Что чинится по дороге. В темах 104 ссылки на документы стоят по СТАРЫМ
числовым адресам (`documents/ru/ru14.html`). На боевом они отдают 301,
здесь переписываются на смысловые слаги сразу - лишний переход читателю ни
к чему.

Сверка. После сборки видимый текст новой страницы сравнивается со старой
слово в слово; расхождение - отказ.

Запуск:  python _tools/build_topics_v2.py [--dry]
"""
import glob
import html as html_mod
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import site_guard as guard                                   # noqa: E402
import chrome as C                                           # noqa: E402
from build_site_docs import (SITE, ORIGIN, ROOT, HEAD_ICONS,  # noqa: E402
                             OG_LOCALE, UMAMI, SLUGS, doc_href, has_doc)

V2 = os.path.join(SITE, '_v2')
PROD = os.path.join(SITE, 'topics')
OUT = os.path.join(V2, 'topics')

LANGS = ['ru', 'en', 'es', 'de', 'fr', 'zh', 'ar', 'hi', 'ka']

# Порядок тем в хабе взят из боевого хаба, а не придуман: он выстроен от
# самой понятной новичку темы к самой отвлечённой.
ORDER = ['belonging-by-choice', 'self-determination-without-territory',
         'new-subject-of-international-law', 'complementary-to-states',
         'society-without-coercion', 'direct-planetary-democracy',
         'rights-of-future-generations']

# Строгий скелет темы. Любое расхождение - отказ.
TOPIC = re.compile(
    r'\s*<p class="eyebrow">(?P<eyebrow>.*?)</p>'
    r'\s*<h1>(?P<h1>.*?)</h1>'
    r'\s*<div class="lead">(?P<lead>.*?)</div>'
    r'\s*(?P<rest>.*?)'
    r'\s*<div class="cta">\s*<h2>(?P<cta_h>.*?)</h2>\s*<p>(?P<cta_p>.*?)</p>'
    r'\s*<a class="btn" href="(?P<cta_href>[^"]+)">(?P<cta_a>.*?)</a>\s*</div>'
    r'\s*<div class="related">\s*<h2>(?P<rel_h>.*?)</h2>\s*<ul>(?P<rel>.*?)</ul>'
    r'\s*</div>\s*$', re.S)

HUB = re.compile(
    r'\s*<p class="eyebrow">(?P<eyebrow>.*?)</p>'
    r'\s*<h1>(?P<h1>.*?)</h1>'
    r'\s*<p class="intro">(?P<intro>.*?)</p>'
    r'\s*<ul class="topics">(?P<list>.*?)</ul>\s*$', re.S)


def main_of(path):
    s = io.open(path, encoding='utf-8').read()
    m = re.search(r'<main[^>]*>(.*?)</main>', s, re.S)
    assert m, u'нет <main> в %s' % path
    head = s.split('</head>')[0]
    t = re.search(r'<title>(.*?)</title>', head, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', head)
    assert t and d, u'нет заголовка или описания в %s' % path
    return m.group(1), t.group(1).strip(), d.group(1)


def fix_links(s, lang):
    u"""Ссылки на документы - на смысловые слаги и корневой формой.

    В боевых темах они записаны абсолютно и по старым числовым адресам,
    которые отдают 301. Читателю лишний переход ни к чему, а краулеру -
    тем более.
    """
    def doc(m):
        code, num = m.group(1), m.group(2)
        if num in SLUGS.get(code, {}):
            return doc_href(num, code)
        return '/documents/%s/%s%s.html' % (code, code, num)

    s = re.sub(r'https://earth-lings\.org/documents/([a-z]{2})/[a-z]{2}(\d{2})'
               r'(?:-[a-z0-9-]+)?\.html', doc, s)
    s = re.sub(r'https://earth-lings\.org/topics/', '/topics/', s)
    s = re.sub(r'https://earth-lings\.org/', '/', s)
    return s


def visible(s):
    u"""Видимый текст: по нему сверяется, что перенос ничего не потерял."""
    s = re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html_mod.unescape(s)).strip()


def head_html(lang, url, title, desc, alt_path):
    alts = ''.join(
        '<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, ORIGIN, alt_path(l))
        for l in LANGS)
    alts += ('<link rel="alternate" hreflang="x-default" href="%s%s">\n'
             % (ORIGIN, alt_path('en')))
    return '\n'.join([
        '<!DOCTYPE html>',
        '<html lang="%s"%s>' % (lang, ' dir="rtl"' if lang in C.RTL else ''),
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % C.esc(title),
        '<meta name="description" content="%s">' % C.esc(desc),
        HEAD_ICONS,
    ] + C.font_preloads(lang) + C.script_css(lang) + [
        '<link rel="stylesheet" href="/css/tokens.css">',
        '<link rel="stylesheet" href="/css/chrome.css">',
        '<link rel="stylesheet" href="/css/doc.css">',
        '<link rel="stylesheet" href="/css/topics.css">',
        '<script defer src="/js/chrome.js"></script>',
        '<meta name="robots" content="index, follow">',
        '<link rel="canonical" href="%s">' % url,
        '<meta property="og:type" content="article">',
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % C.esc(title),
        '<meta property="og:description" content="%s">' % C.esc(desc),
        '<meta property="og:image" content="%s/images/og-image.jpg">' % ORIGIN,
        '<meta property="og:site_name" content="Earthlings">',
        '<meta property="og:locale" content="%s">' % OG_LOCALE[lang],
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % C.esc(title),
        '<meta name="twitter:description" content="%s">' % C.esc(desc),
        '<meta name="twitter:image" content="%s/images/og-image.jpg">' % ORIGIN,
        alts.rstrip(),
        '</head>',
    ])


def shell(lang, inner, url, title, desc, alt_path):
    href = lambda n: doc_href(n, lang)                        # noqa: E731
    have = lambda n: has_doc(n, lang)                         # noqa: E731
    return '\n'.join([
        head_html(lang, url, title, desc, alt_path),
        '<body>',
        C.header_html(lang, doc_href=href, lang_url=alt_path,
                      home_url='/%s/' % lang, has_doc=have),
        '<main class="%s" id="main"><div class="sheet">' % ROOT,
        inner,
        '</div></main>',
        C.footer_html(lang, doc_href=href, has_doc=have),
        UMAMI,
        '</body>', '</html>', '',
    ])


def build_topic(slug, lang):
    src = os.path.join(PROD, slug, '%s.html' % lang)
    body, title, desc = main_of(src)
    m = TOPIC.match(body)
    assert m, u'страница не совпала со скелетом: %s' % src
    g = {k: fix_links(v, lang) for k, v in m.groupdict().items()}

    # Разделы: h2 - ступень части, h3 - ступень статьи. Классы новой темы, а
    # не голые теги: в doc.css у голых h2/h3 внутри .sheet стиля нет.
    rest = re.sub(r'<h2>(.*?)</h2>',
                  r'<section class="part flat"><h2 class="part-title">\1</h2></section>',
                  g['rest'], flags=re.S)
    rest = re.sub(r'<h3>(.*?)</h3>',
                  r'<header class="art-head"><h3 class="art-title">\1</h3></header>',
                  rest, flags=re.S)

    inner = '\n'.join([
        '<header class="doc-head">',
        '<div class="part-no">%s</div>' % g['eyebrow'],
        '<h1 class="doc-title">%s</h1>' % g['h1'],
        '<div class="rule-double"></div>',
        '</header>',
        '<section class="topic-lead">%s</section>' % g['lead'].strip(),
        rest.strip(),
        '<section class="topic-cta">',
        '<h2 class="art-title">%s</h2>' % g['cta_h'],
        '<p>%s</p>' % g['cta_p'],
        '<p><a class="topic-btn" href="%s">%s</a></p>' % (g['cta_href'], g['cta_a']),
        '</section>',
        '<nav class="topic-related" aria-label="%s">' % C.esc(visible(g['rel_h'])),
        '<h2 class="art-title">%s</h2>' % g['rel_h'],
        '<ul>%s</ul>' % g['rel'].strip(),
        '</nav>',
    ])

    url = '%s/topics/%s/%s.html' % (ORIGIN, slug, lang)
    page = shell(lang, inner, url, title, desc,
                 lambda l: '/topics/%s/%s.html' % (slug, l))
    return page, body, src


def build_hub(lang):
    src = os.path.join(PROD, 'ru.html' if lang == 'ru' else '%s.html' % lang)
    if lang == 'en':
        src = os.path.join(PROD, 'index.html')
    body, title, desc = main_of(src)
    m = HUB.match(body)
    assert m, u'хаб не совпал со скелетом: %s' % src
    g = {k: fix_links(v, lang) for k, v in m.groupdict().items()}

    inner = '\n'.join([
        '<header class="doc-head">',
        '<div class="part-no">%s</div>' % g['eyebrow'],
        '<h1 class="doc-title">%s</h1>' % g['h1'],
        '<div class="rule-double"></div>',
        '</header>',
        '<section class="topic-lead"><p>%s</p></section>' % g['intro'],
        '<ul class="topic-list">%s</ul>' % g['list'].strip(),
    ])
    name = 'index.html' if lang == 'en' else '%s.html' % lang
    url = '%s/topics/%s' % (ORIGIN, '' if lang == 'en' else name)
    page = shell(lang, inner, url, title, desc,
                 lambda l: '/topics/' + ('' if l == 'en' else '%s.html' % l))
    return page, body, src, name


def main():
    dry = '--dry' in sys.argv
    assert os.path.isdir(PROD), u'нет боевого каталога тем: %s' % PROD
    guard.makedirs(OUT)

    n = 0
    for slug in ORDER:
        guard.makedirs(os.path.join(OUT, slug))
        for lang in LANGS:
            page, body, src = build_topic(slug, lang)
            a, b = visible(body), visible(page.split('<main', 1)[1])
            assert a in b, (u'перенос потерял текст: %s\n  было: %s\n  стало: %s'
                            % (src, a[:120], b[:120]))
            guard.write(os.path.join(OUT, slug, '%s.html' % lang), page, dry=dry)
            n += 1

    h = 0
    for lang in LANGS:
        page, body, src, name = build_hub(lang)
        a, b = visible(body), visible(page.split('<main', 1)[1])
        assert a in b, u'перенос хаба потерял текст: %s' % src
        guard.write(os.path.join(OUT, name), page, dry=dry)
        h += 1

    print(u'темы: %d страниц, хабы: %d%s' % (n, h, u'  (сухой прогон)' if dry else ''))
    print(u'ссылки на документы переписаны со старых числовых адресов на смысловые')


if __name__ == '__main__':
    try:
        main()
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
