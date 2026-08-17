# -*- coding: utf-8 -*-
u"""Языковая главная нового сайта: чередование полос, как на epic.org.

Зачем страница переделывается. Сейчас `/ru/`, `/en/` и остальные семь адресов
отдают ОДИН И ТОТ ЖЕ `index.html` с английскими метаданными, а текст дорисовывает
скрипт из `mainpage/<язык>/index.html`. Для краулера без JS все девять языковых
главных пусты. Здесь у каждого языка свой файл, полный в HTML, с заголовком и
описанием на своём языке.

Что на полосах. Порядок задан Артуром: белая, тёмно-синяя, белая, голубая,
тёмно-синяя, и на них Манифест, Учредительный период, Декларация. Четвёртую и
пятую он оставил на моё усмотрение - там правовая база и путь earthling с
кнопкой действия: снизу вверх это «кто мы - что происходит сейчас - чем это
учреждается - на каком праве это стоит - как войти».

Текст не сочиняется. Лид каждой полосы - первые абзацы соответствующего мастера
слово в слово. Заголовок - его H1. Отсебятины на главной быть не должно: это
самая читаемая страница сайта, и голос на ней должен быть тот же, что в корпусе.

Собирается два файла на язык:
  _v2/<язык>/index.html     - полосы
  _v2/<язык>/manifest.html  - Манифест целиком, набранный как документ

Использование:
  python build_home_v2.py            все языки, для которых есть мастера
  python build_home_v2.py ru         один язык
  python build_home_v2.py --dry      ничего не записывать
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md2doc                                              # noqa: E402
import chrome as C                                         # noqa: E402
from build_site_docs import (SITE, REPO, ORIGIN, ROOT, doc_href, has_doc,
                             ALL_LANGS, md_dir, corpus_file, SLUGS)  # noqa: E402

MANIFEST_DIR = os.path.join(REPO, '_manifest')
OUT = os.path.join(SITE, '_v2')

# Полосы: (класс темы, что показываем, номера абзацев лида, якорь).
#
# Номера, а не «первые N абзацев». Корпусные документы открываются процедурно -
# «Настоящий текст представляет...», «Возраст - 18 лет», - и механический выбор
# первого абзаца ставил на главную служебные оговорки. Абзацы выбраны глазами.
#
# Номер работает на всех языках, потому что переводы зеркалят структуру мастера
# блок в блок - это правило корпуса, а не удача. Но если мастер поправят,
# нумерация поедет молча, поэтому рядом стоит ЯКОРЬ: начало русского абзаца.
# Не совпал - сборка падает и говорит, какой документ разошёлся.
#
# Документы названы номерами: переименование документа сюда не заглядывает,
# заголовок полосы берётся из его H1.
BANDS = [
    ('white', 'manifest', [1, 2, 4], u'Международные организации'),
    ('navy',  'doc:20',   [1, 4],    u'Сегодня Декларация существует'),
    ('white', 'doc:01',   [1, 4],    u'Настоящая редакция является'),
    ('mist',  'legal',    [4, 6],    u'Международное право умеет'),
    ('navy',  'doc:14',   [12],      u'Внутри народа паспорт'),
]

# Что перечислено в правовой полосе. Порядок - от общего к частному.
LEGAL_DOCS = ['30', '04', '05', '26']
# Лид правовой полосы берём из «Как возникает субъект права»: там сказано, на
# чём всё стоит, без служебных оговорок про соотношение документов.
LEGAL_LEAD_DOC = '30'

# Подпись под Манифестом. Подписывают его авторы, а не народ (Учредительный
# период, раздел 02), поэтому здесь команда, а не «Earthlings».
SIGN = {'ru': u'Команда Earthlings', 'en': u'The Earthlings team',
        'de': u'Das Earthlings-Team'}

PDF = {
    'ru': ('/downloads/manifest-prinadlezhnosti-ru.pdf', u'Скачать Манифест в PDF'),
    'en': ('/downloads/manifesto-of-belonging-en.pdf', u'Download the Manifesto as PDF'),
    'de': ('/downloads/manifest-der-zugehoerigkeit-de.pdf', u'Manifest als PDF herunterladen'),
}


# ------------------------------------------------------------------ мастера

def read_master(path):
    assert os.path.isfile(path), u'нет мастера %s' % path
    s = io.open(path, encoding='utf-8').read()
    assert s.strip(), u'пустой мастер %s' % path
    return s


def title_of(md):
    m = re.search(r'^#\s+(.+)$', md, re.M)
    assert m, u'в мастере нет заголовка H1'
    return m.group(1).strip()


def prose(md):
    u"""Абзацы прозы мастера по порядку.

    Выброшены заголовки, цитаты, таблицы, списки, разделители, вставки схем и
    строки из одного жирного куска - это подзаголовок документа. Короче 90
    знаков тоже выброшено: такой длины бывают пункты перечня («Возраст -
    достижение возраста 18 лет»), а не абзац, которым открывают страницу.
    """
    out = []
    for block in re.split(r'\n\s*\n', md):
        b = re.sub(r'\s+', ' ', block.strip())
        if not b or b[0] in '#>|[' or b.startswith('- ') or b.startswith('* '):
            continue
        if b.startswith('---') or re.match(r'^\*\*[^*]+\*\*$', b):
            continue
        if len(b) < 90:
            continue
        out.append(b)
    assert out, u'не нашлось ни одного абзаца прозы'
    return out


def lead(md, nums, anchor, lang, where):
    u"""Абзацы лида по номерам. Якорь проверяется только на русском: он и есть
    мастер, остальные языки зеркалят его структуру."""
    ps = prose(md)
    for n in nums:
        assert n <= len(ps), (
            u'в мастере %s (%s) всего %d абзацев прозы, а лид просит №%d'
            % (where, lang, len(ps), n))
    if lang == 'ru':
        got = ps[nums[0] - 1]
        assert got.startswith(anchor), (
            u'лид главной разошёлся с мастером %s: абзац №%d начинается на '
            u'%r, а ожидалось %r. Мастер правили - проверьте номера абзацев в '
            u'BANDS и выберите заново.' % (where, nums[0], got[:40], anchor))
    return [ps[n - 1] for n in nums]


def md_inline(s):
    u"""Разметка внутри абзаца: жирный, курсив, ссылки, код. Того же набора
    хватает и корпусу - главная набрана тем же, чем документы."""
    s = C.esc(s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'&lt;(https?://[^&]+)&gt;', r'<a href="\1">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s


def doc_master(num, lang):
    return read_master(os.path.join(md_dir(lang), corpus_file(num, lang)))


# ------------------------------------------------------------------ страница

def head(lang, url, title, desc, path, extra_css=()):
    # path(код языка) -> адрес ЭТОЙ ЖЕ страницы на другом языке. Без него
    # hreflang на странице Манифеста вёл бы на главные других языков, то есть
    # объявлял бы переводом не тот документ.
    langs = [l for l in ALL_LANGS if os.path.isfile(
        os.path.join(MANIFEST_DIR, '%s-manifest.md' % l))]
    alts = ''.join(
        '<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, ORIGIN, path(l))
        for l in langs)
    xdef = 'en' if 'en' in langs else langs[0]
    alts += ('<link rel="alternate" hreflang="x-default" href="%s%s">\n'
             % (ORIGIN, path(xdef)))
    ld = {'@context': 'https://schema.org', '@type': 'WebPage',
          'name': title, 'description': desc, 'inLanguage': lang, 'url': url,
          'publisher': {'@type': 'Organization', 'name': 'Earthlings',
                        'url': ORIGIN}}
    css = ['<link rel="stylesheet" href="/css/tokens.css">',
           '<link rel="stylesheet" href="/css/chrome.css">',
           '<link rel="stylesheet" href="/css/doc.css">'] + list(extra_css)
    return '\n'.join([
        '<!DOCTYPE html>',
        '<html lang="%s"%s>' % (lang, ' dir="rtl"' if lang in C.RTL else ''),
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % C.esc(title),
        '<meta name="description" content="%s">' % C.esc(desc),
    ] + css + [
        '<script defer src="/js/chrome.js"></script>',
        '<meta name="robots" content="index, follow">',
        '<meta property="og:type" content="website">',
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % C.esc(title),
        '<meta property="og:description" content="%s">' % C.esc(desc),
        '<meta property="og:image" content="%s/images/og-image.jpg">' % ORIGIN,
        '<meta property="og:site_name" content="Earthlings">',
        '<meta property="og:locale" content="%s">' % lang,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % C.esc(title),
        '<meta name="twitter:image" content="%s/images/og-image.jpg">' % ORIGIN,
        '<link rel="canonical" href="%s">' % url,
        '<script type="application/ld+json">',
        json.dumps(ld, ensure_ascii=False, separators=(',', ':')),
        '</script>',
        alts.rstrip(),
        '</head>',
    ])


def wrap(lang, inner, url, title, desc, path, extra_css=()):
    href = lambda n: doc_href(n, lang)                     # noqa: E731
    have = lambda n: has_doc(n, lang)                      # noqa: E731
    return '\n'.join([
        head(lang, url, title, desc, path, extra_css),
        '<body>',
        C.header_html(lang, doc_href=href, lang_url=path,
                      home_url='/%s/' % lang, has_doc=have),
        inner,
        C.footer_html(lang, doc_href=href, has_doc=have),
        '</body>', '</html>', '',
    ])


# ------------------------------------------------------------------ полосы

def band(theme, first, title, lead, more=None, items=None, cta=None):
    o = ['<section class="band band--%s%s"><div class="band-in">'
         % (theme, ' band--first' if first else '')]
    tag = 'h1' if first else 'h2'
    o.append('<%s class="band-title">%s</%s>' % (tag, C.esc(title), tag))
    o.append('<div class="band-lead">%s</div>'
             % ''.join('<p>%s</p>' % md_inline(p) for p in lead))
    if items:
        o.append('<ul class="band-list">%s</ul>'
                 % ''.join('<li><a href="%s">%s</a></li>' % (C.esc(h), C.esc(t))
                           for t, h in items))
    if more:
        o.append('<a class="band-more" href="%s">%s</a>' % (C.esc(more[1]),
                                                            C.esc(more[0])))
    if cta:
        o.append('<a class="band-cta" href="%s">%s</a>' % (C.esc(cta[1]),
                                                           C.esc(cta[0])))
    o.append('</div></section>')
    return '\n'.join(o)


def build_index(lang):
    manifest = read_master(os.path.join(MANIFEST_DIR, '%s-manifest.md' % lang))
    more = C.x(lang, 'read_more')
    bands = []

    for i, (theme, what, nums, anchor) in enumerate(BANDS):
        first = (i == 0)
        if what == 'manifest':
            bands.append(band(theme, first, title_of(manifest),
                              lead(manifest, nums, anchor, lang, u'Манифест'),
                              more=(more, '/%s/manifest.html' % lang)))
        elif what == 'legal':
            md = doc_master(LEGAL_LEAD_DOC, lang)
            items = [(title_of(doc_master(d, lang)), doc_href(d, lang))
                     for d in LEGAL_DOCS if has_doc(d, lang)]
            assert items, u'ни один правовой документ не доступен на %s' % lang
            bands.append(band(theme, first, C.t(lang, 'nav.legal_base'),
                              lead(md, nums, anchor, lang, LEGAL_LEAD_DOC),
                              items=items))
        else:
            num = what.split(':')[1]
            assert has_doc(num, lang), u'документа %s нет на языке %s' % (num, lang)
            md = doc_master(num, lang)
            cta = ((C.t(lang, 'nav.become_earthling'), C.CTA_URL % lang)
                   if num == '14' else None)
            bands.append(band(theme, first, title_of(md),
                              lead(md, nums, anchor, lang, num),
                              more=(more, doc_href(num, lang)), cta=cta))

    title = C.t(lang, 'page.title')
    desc = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '',
                  md_inline(prose(manifest)[0])))[:300]
    inner = '<main id="main">%s</main>' % '\n'.join(bands)
    return wrap(lang, inner, '%s/%s/' % (ORIGIN, lang), title, desc,
                lambda c: '/%s/' % c,
                ['<link rel="stylesheet" href="/css/home.css">'])


def build_manifest(lang):
    md = read_master(os.path.join(MANIFEST_DIR, '%s-manifest.md' % lang))
    doc = md2doc.parse(md)
    assert doc['title'], u'в Манифесте не найден заголовок H1'
    body = md2doc.render_body(doc)

    o = ['<main class="%s" id="main"><div class="sheet">' % ROOT,
         '<header class="doc-head"><h1 class="doc-title">%s</h1>'
         '<div class="rule-double"></div></header>' % C.esc(doc['title']),
         body]
    assert lang in SIGN, u'нет подписи под Манифестом для языка %s' % lang
    o.append('<p class="sign">%s</p>' % C.esc(SIGN[lang]))
    if lang in PDF:
        href, label = PDF[lang]
        assert os.path.isfile(os.path.join(SITE, href.lstrip('/'))), (
            u'нет файла %s - ссылка на PDF была бы битой' % href)
        o.append('<p><a class="pdf-link" href="%s">%s</a></p>'
                 % (href, C.esc(label)))
    o.append('</div></main>')

    desc = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '',
                  md_inline(prose(md)[0])))[:300]
    return wrap(lang, '\n'.join(o),
                '%s/%s/manifest.html' % (ORIGIN, lang),
                '%s | Earthlings' % doc['title'], desc,
                lambda c: '/%s/manifest.html' % c,
                ['<link rel="stylesheet" href="/css/home.css">'])


def main():
    dry = '--dry' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    langs = args or [l for l in ALL_LANGS if os.path.isfile(
        os.path.join(MANIFEST_DIR, '%s-manifest.md' % l))]
    assert langs, u'нет ни одного мастера Манифеста'

    for lang in langs:
        assert lang in SLUGS, (
            u'для языка %r не заданы слаги: ссылки с главной на документы '
            u'легли бы мимо' % lang)
        d = os.path.join(OUT, lang)
        if not os.path.isdir(d) and not dry:
            os.makedirs(d)
        for name, page in (('index.html', build_index(lang)),
                           ('manifest.html', build_manifest(lang))):
            if not dry:
                io.open(os.path.join(d, name), 'w', encoding='utf-8',
                        newline='\n').write(page)
            text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ',
                          page.split('<body', 1)[1])).strip()
            print('OK   _v2/%s/%-14s %3d КБ, текста без JS: %5d знаков'
                  % (lang, name, len(page.encode('utf-8')) // 1024, len(text)))


if __name__ == '__main__':
    main()
