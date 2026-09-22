# -*- coding: utf-8 -*-
"""
Конвертер MD -> HTML для корпуса Earthlings.

Оформление: слоновая кость, тёмно-синие заголовки, золотые элементы,
тёмно-серый основной текст. Один самодостаточный файл на выходе.

Режимы:
  обычный  - документ: название, оглавление, части/статьи, текст
  --hero   - главная: тёмный герой сверху (как на текущей главной), дальше текст

Использование:
  python md2doc.py <input.md> <output.html> [--hero] [--no-toc]
"""
import sys, os, re, html, argparse
import site_guard as guard

# ---------------------------------------------------------------- инлайн

def inline(s):
    # Код прячем до всех прочих замен и возвращаем в конце: внутри адреса
    # контракта или имени функции звёздочка не выделение, а часть строки.
    code = []

    def stash(m):
        code.append(m.group(1))
        return '\x00%d\x00' % (len(code) - 1)

    s = re.sub(r'`([^`\n]+)`', stash, s)
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    # Markdown-экранирование снимаем последним: до этой строки обратный слэш
    # защищал звёздочку и подчёркивание от разметки, дальше он не нужен.
    # Раньше не снимали, и в статью 14 Декларации уезжало \_\_\_ вместо ___.
    s = re.sub(r'\\([!-/:-@\[-`{-~])', r'\1', s)
    s = re.sub(r'\x00(\d+)\x00',
               lambda m: '<code>%s</code>' % html.escape(code[int(m.group(1))], quote=False), s)
    return s.strip()


# ---------------------------------------------------------------- разбор

RE_PART = re.compile(r'^(ЧАСТЬ|РАЗДЕЛ|ГЛАВА)\s+([IVXLC]+|\d+)[.:]?\s*(.*)$', re.I)
RE_ART = re.compile(r'^(Статья|Этап|Раздел|Глава|Пункт|Приложение)\s+([IVXLC]+|\d+)[.:]\s*(.+)$')
SLUG = {'Статья': 'st', 'Этап': 'et', 'Раздел': 'sec', 'Глава': 'ch',
        'Пункт': 'cl', 'Приложение': 'app'}


def parse(md):
    lines = md.replace('\r\n', '\n').split('\n')
    doc = {'title': '', 'lead': [], 'parts': []}
    part = None
    art = None
    buf, ul, ol, quote, table = [], [], [], [], []

    def target():
        if art:  return art['blocks']
        if part: return part['intro']
        return doc['lead']

    def flush():
        nonlocal buf, ul, ol, quote, table
        t = target()
        if buf:
            t.append(('p', buf[:]));  buf = []
        if ul:
            t.append(('ul', ul[:]));  ul = []
        if ol:
            t.append(('ol', ol[:]));  ol = []
        if quote:
            t.append(('note', quote[:])); quote = []
        if table:
            t.append(('table', table[:])); table = []

    def ensure_part():
        nonlocal part
        if part is None:
            part = {'label': '', 'title': '', 'intro': [], 'articles': [],
                    'id': 'sec-%d' % (len(doc['parts']) + 1)}
            doc['parts'].append(part)
        return part

    for raw in lines:
        s = raw.strip()

        if s == '' or s == '---':
            flush()
            continue

        if s.startswith('|'):
            if buf or ul or ol or quote:
                flush()
            table.append(s)
            continue
        if table:
            flush()

        if s.startswith('>'):
            if buf or ul or ol:
                flush()
            q = s.lstrip('>').strip()
            quote.append(q)
            continue
        if quote:
            flush()

        if s.startswith('# '):
            flush()
            text = s[2:].strip()
            if not doc['title']:
                doc['title'] = text
                continue
            m = RE_PART.match(text)
            if m:
                label = ('%s %s' % (m.group(1), m.group(2)))
                title = m.group(3).strip()
            else:
                label, title = '', text
            part = {'label': label, 'title': title, 'intro': [], 'articles': [],
                    'id': 'sec-%d' % (len(doc['parts']) + 1)}
            doc['parts'].append(part)
            art = None
            continue

        if s.startswith('## '):
            flush()
            text = s[3:].strip()
            m = RE_ART.match(text)
            if m:
                label = '%s %s' % (m.group(1), m.group(2))
                title = m.group(3).strip()
                slug = SLUG.get(m.group(1), 'p') + '-' + m.group(2).lower()
            else:
                label, title = '', text
                slug = 'p%d' % (sum(len(p['articles']) for p in doc['parts']) + 1)
            ensure_part()
            art = {'label': label, 'title': title, 'id': slug, 'blocks': []}
            part['articles'].append(art)
            continue

        if s.startswith('#### '):
            flush()
            target().append(('h4', s[5:].strip()))
            continue

        if s.startswith('### '):
            flush()
            target().append(('h3', s[4:].strip()))
            continue

        if s.startswith('- ') or s.startswith('* '):
            if buf or ol:
                flush()
            ul.append(s[2:].strip())
            continue
        if ul:
            flush()

        m = re.match(r'^(\d+)\.\s+(.*)$', s)
        if m:
            if buf or ul:
                flush()
            ol.append(m.group(2).strip())
            continue
        if ol:
            flush()

        buf.append(s)

    flush()
    return doc


# ---------------------------------------------------------------- сборка

def render_table(rows):
    cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
    if len(cells) >= 2 and all(re.fullmatch(r':?-{2,}:?', c) for c in cells[1] if c):
        head, body = cells[0], cells[2:]
    else:
        head, body = None, cells
    out = ['<div class="tbl-wrap"><table>']
    if head:
        out.append('<thead><tr>%s</tr></thead>'
                   % ''.join('<th>%s</th>' % inline(c) for c in head))
    out.append('<tbody>')
    for r in body:
        out.append('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in r))
    out.append('</tbody></table></div>')
    return ''.join(out)


def render_note(lines):
    """Врезка: внутри цитаты бывают перечни, их нельзя склеивать в абзац."""
    out, para, items = [], [], []
    kind = None

    def flush_para():
        if para:
            out.append('<p>%s</p>' % inline(' '.join(para)))
            del para[:]

    def flush_items():
        nonlocal kind
        if items:
            out.append('<%s>%s</%s>'
                       % (kind, ''.join('<li>%s</li>' % inline(i) for i in items), kind))
            del items[:]
        kind = None

    for line in lines:
        m_ul = re.match(r'[-*]\s+(.*)$', line)
        m_ol = re.match(r'(?:\d+)\.\s+(.*)$', line)
        if m_ul or m_ol:
            new_kind = 'ul' if m_ul else 'ol'
            flush_para()
            if kind and kind != new_kind:
                flush_items()
            kind = new_kind
            items.append((m_ul or m_ol).group(1))
            continue
        flush_items()
        if line:
            para.append(line)
        else:
            flush_para()
    flush_items()
    flush_para()
    return ''.join(out)


def render_blocks(blocks):
    out = []
    for kind, val in blocks:
        if kind == 'h3':
            out.append('<h3>%s</h3>' % inline(val))
        elif kind == 'h4':
            out.append('<h4>%s</h4>' % inline(val))
        elif kind == 'p':
            out.append('<p>%s</p>' % inline(' '.join(val)))
        elif kind == 'ul':
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % inline(i) for i in val))
        elif kind == 'ol':
            out.append('<ol>%s</ol>' % ''.join('<li>%s</li>' % inline(i) for i in val))
        elif kind == 'note':
            out.append('<div class="note">%s</div>' % render_note(val))
        elif kind == 'table':
            out.append(render_table(val))
    return '\n'.join(out)


def is_flat(doc):
    labeled = [p for p in doc['parts'] if p['label'] or p['title']]
    arts = sum(len(p['articles']) for p in doc['parts'])
    return bool(labeled) and arts < 2 * len(labeled)


def render_toc(doc):
    flat = is_flat(doc)
    rows = []
    for p in doc['parts']:
        if p['label'] or p['title']:
            if flat:
                rows.append('<a class="toc-item%s" href="#%s"><span class="toc-no">%s</span>'
                            '<span class="toc-name">%s</span></a>'
                            % ('' if p['label'] else ' nolabel', p['id'],
                               html.escape(p['label']), inline(p['title'])))
            else:
                rows.append('<div class="toc-part">%s</div>'
                            % inline(' '.join(x for x in [p['label'] + '.' if p['label'] else '',
                                                          p['title']] if x).strip()))
        sub = ' sub' if flat else ''
        for a in p['articles']:
            if a['label']:
                rows.append('<a class="toc-item%s" href="#%s"><span class="toc-no">%s</span>'
                            '<span class="toc-name">%s</span></a>'
                            % (sub, a['id'], html.escape(a['label']), inline(a['title'])))
            else:
                rows.append('<a class="toc-item nolabel%s" href="#%s">'
                            '<span class="toc-name">%s</span></a>'
                            % (sub, a['id'], inline(a['title'])))
    return '\n'.join(rows)


def render_body(doc):
    """Части-баннеры (как ЧАСТЬ I в Декларации) - только если под каждой частью
    действительно лежат разделы. Иначе части сами и есть разделы: их заголовки
    ставим слева, как заголовки статей, чтобы не рвать текст полосами."""
    labeled = [p for p in doc['parts'] if p['label'] or p['title']]
    arts = sum(len(p['articles']) for p in doc['parts'])
    flat = bool(labeled) and arts < 2 * len(labeled)

    out = []
    if doc['lead']:
        out.append('<section class="lead col">%s</section>' % render_blocks(doc['lead']))
    for p in doc['parts']:
        if p['label'] or p['title']:
            head = ''
            if p['label']:
                head += '<div class="part-no">%s</div>' % html.escape(p['label'])
            if p['title']:
                head += '<h2 class="part-title">%s</h2>' % inline(p['title'])
            out.append('<section class="part%s" id="%s">%s</section>'
                       % (' flat' if flat else '', p['id'], head))
        if p['intro']:
            out.append('<div class="article">%s</div>' % render_blocks(p['intro']))
        for a in p['articles']:
            head = ''
            if a['label']:
                head += '<div class="art-no">%s</div>' % html.escape(a['label'])
            head += '<h2 class="art-title">%s</h2>' % inline(a['title'])
            out.append('<article class="article" id="%s"><header class="art-head">%s</header>%s</article>'
                       % (a['id'], head, render_blocks(a['blocks'])))
    return '\n'.join(out)


def render_hero(doc, hint=''):
    """Герой как на текущей главной: тёмная комната, триада строками, вопрос золотом."""
    lines, question = [], ''
    for kind, val in doc['lead']:
        if kind != 'p':
            continue
        joined = ' '.join(val).strip()
        if joined.startswith('**') and joined.endswith('**'):
            question = joined.strip('*')
        elif not lines:
            lines = val
    rest = []
    started = False
    for kind, val in doc['lead']:
        if kind == 'p':
            joined = ' '.join(val).strip()
            if not started and (val is lines or (joined.startswith('**') and joined.endswith('**'))):
                continue
        started = True
        rest.append((kind, val))

    hero = ['<header class="hero"><div class="hero-in">']
    hero.append('<p class="hero-mark">%s</p>' % html.escape(doc['title']))
    if lines:
        hero.append('<h1 class="hero-q">%s%s</h1>'
                    % (''.join('<span class="hero-l">%s</span>' % inline(l) for l in lines),
                       ('<em>%s</em>' % inline(question)) if question else ''))
    elif question:
        hero.append('<h1 class="hero-q"><em>%s</em></h1>' % inline(question))
    if hint:
        hero.append('<p class="hero-hint">%s</p>' % html.escape(hint))
    hero.append('</div></header>')
    return ''.join(hero), rest


TEMPLATE = u"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --page:  #ece5d6;
  --ivory: #fbf9f3;
  --navy:  #1d4163;
  --gold:  #8a6a2f;
  --ink:   #3a4046;
  --ink-soft: #5f6670;
  --rule:  rgba(138,106,47,.32);
  --rule-soft: rgba(138,106,47,.16);
  /* Мера строки задаётся в ch, а не в пикселях: колонка обязана расти
     вместе с кеглем, иначе при укрупнении шрифта строка становится
     короче принятых на сайте 66-70 знаков. Значение подобрано замером
     в браузере: в Georgia знак «0» узкий, поэтому ch тут мельче
     среднего символа кириллицы. */
  --measure: 78ch;
  --serif: Georgia, "PT Serif", "Times New Roman", "Liberation Serif", serif;
  --mono:  ui-monospace, "JetBrains Mono", Consolas, "Courier New", monospace;
  --hero-1: #17334c; --hero-2: #10263a; --hero-3: #0c1c29;
  --hero-gold: #c7a56a; --hero-mut: rgba(233,238,242,.62);
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }}
body {{
  margin: 0; background: var(--page); color: var(--ink);
  font: 400 18px/1.78 var(--serif);
}}
a {{ color: var(--gold); }}
a:hover {{ text-decoration: none; }}

/* ------------------------------------------------ герой (только главная) */
.hero {{
  background: radial-gradient(120% 100% at 20% -10%, var(--hero-1) 0%, var(--hero-2) 45%, var(--hero-3) 100%);
  color: #e9eef2; padding: clamp(4.5rem,10vw,8rem) 0 clamp(4rem,9vw,7rem);
}}
.hero-in {{ max-width: 1040px; margin: 0 auto; padding: 0 clamp(1.4rem,5vw,4rem); }}
.hero-mark {{
  margin: 0; font-family: var(--mono); font-size: .8rem; font-weight: 600;
  letter-spacing: .42em; text-transform: uppercase; color: var(--hero-gold);
}}
.hero-q {{
  margin: 2.6rem 0 0; color: #fff; font-weight: 500;
  font-size: clamp(1.45rem,3vw,2.5rem); line-height: 1.3; max-width: 44ch;
}}
.hero-l {{ display: block; text-wrap: balance; }}
.hero-q em {{
  display: block; margin-top: .6em; font-style: italic;
  color: var(--hero-gold); text-wrap: balance;
}}
.hero-hint {{
  margin: 3.2rem 0 0; font-family: var(--mono); font-size: .74rem;
  letter-spacing: .28em; text-transform: uppercase; color: var(--hero-mut);
}}

/* ------------------------------------------------ лист */
.sheet {{
  max-width: 1040px; margin: 0 auto; background: var(--ivory);
  border-left: 1px solid var(--rule-soft); border-right: 1px solid var(--rule-soft);
  box-shadow: 0 0 44px rgba(20,41,58,.08);
  padding: clamp(40px,7vw,84px) 0 96px;
}}
.col, .article {{ max-width: var(--measure); margin: 0 auto; padding: 0 clamp(20px,5vw,40px); }}

/* ------------------------------------------------ шапка документа */
.doc-head {{ text-align: center; }}
.doc-title {{
  margin: 0; color: var(--navy); font-weight: 600;
  font-size: clamp(1.9rem,5vw,2.8rem); line-height: 1.2;
}}
.rule-double {{
  margin: 2.6rem auto 0; height: 5px; max-width: 220px;
  border-top: 2px solid var(--gold); border-bottom: 1px solid var(--rule);
}}

/* ------------------------------------------------ оглавление */
.toc {{ margin: 3.6rem auto 0; }}
.toc-title {{
  text-align: center; font-size: .74rem; letter-spacing: .28em; text-transform: uppercase;
  color: var(--gold); margin: 0 0 1.8rem; font-weight: 400;
}}
.toc-part {{
  margin: 1.9rem 0 .9rem; color: var(--navy); font-size: .78rem;
  letter-spacing: .16em; text-transform: uppercase;
  padding-bottom: .5rem; border-bottom: 1px solid var(--rule-soft);
}}
.toc-part:first-child {{ margin-top: 0; }}
.toc-item {{
  display: grid; grid-template-columns: 6.4rem 1fr; column-gap: .8rem;
  padding: .34rem 0; color: var(--ink); text-decoration: none;
}}
.toc-item.nolabel {{ grid-template-columns: 1fr; }}
.toc-item.sub {{ padding-left: 1.4rem; font-size: .95rem; }}
.toc-no {{ color: var(--gold); font-size: .88rem; white-space: nowrap; }}
.toc-name {{ border-bottom: 1px solid transparent; }}
.toc-item:hover .toc-name {{ border-bottom-color: var(--rule); }}
@media (max-width: 600px) {{
  .toc-item {{ grid-template-columns: 4.4rem 1fr; column-gap: .6rem; }}
  .toc-no {{ font-size: .8rem; }}
}}

/* ------------------------------------------------ вступление */
.lead {{ margin: 3.4rem auto 0; }}
.lead p:first-of-type {{ margin-top: 0; }}

/* ------------------------------------------------ части */
.part {{
  position: relative; text-align: center; max-width: var(--measure);
  margin: 5.4rem auto 3.4rem; padding: 1.7rem 0;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
}}
.part::before {{
  content: ""; position: absolute; top: -4px; left: 50%;
  width: 7px; height: 7px; margin-left: -3.5px;
  background: var(--ivory); border: 1px solid var(--gold); transform: rotate(45deg);
}}
.part-no {{
  font-size: .72rem; letter-spacing: .3em; text-transform: uppercase;
  color: var(--gold); margin-bottom: .7rem;
}}
.part-title {{
  margin: 0; color: var(--navy); font-weight: 600;
  font-size: clamp(1.1rem,2.6vw,1.35rem); letter-spacing: .08em;
  text-transform: uppercase; line-height: 1.4;
}}
/* части, которые сами являются разделами: заголовок слева, без полос */
.part.flat {{
  text-align: left; margin: 4.2rem auto 1.8rem; padding: 1.6rem 0 0;
  border-bottom: 0; border-top: 1px solid var(--rule-soft);
  padding-left: clamp(20px,5vw,40px); padding-right: clamp(20px,5vw,40px);
  max-width: var(--measure);
}}
.part.flat::before {{ display: none; }}
.part.flat .part-no {{ margin-bottom: .5rem; }}
.part.flat .part-title {{
  text-transform: none; letter-spacing: 0;
  font-size: clamp(1.4rem,3.4vw,1.75rem); line-height: 1.28;
}}

/* ------------------------------------------------ статьи и текст */
.article {{ margin-bottom: 3.6rem; }}
.art-head {{ margin: 3.2rem 0 1.9rem; }}
.art-no {{
  font-size: .74rem; letter-spacing: .24em; text-transform: uppercase;
  color: var(--gold); margin-bottom: .55rem;
}}
.art-title {{
  margin: 0; color: var(--navy); font-weight: 600;
  font-size: clamp(1.32rem,3.2vw,1.62rem); line-height: 1.32;
}}
.article h3 {{
  margin: 2.6rem 0 .9rem; color: var(--navy);
  font-size: 1.06rem; font-weight: 600; line-height: 1.45;
}}
.article h3::after {{
  content: ""; display: block; width: 26px; height: 2px;
  background: var(--gold); opacity: .6; margin-top: .55rem;
}}
.article h4 {{
  margin: 2rem 0 .6rem; color: var(--navy);
  font-size: .98rem; font-weight: 600; letter-spacing: .02em; line-height: 1.45;
}}
p {{ margin: 0 0 1.2rem; }}
strong {{ color: var(--navy); font-weight: 700; }}
code {{
  font-family: Consolas, "SF Mono", Menlo, monospace;
  font-size: .88em; word-break: break-all;
  padding: .1em .3em; border-radius: 2px;
  background: rgba(138, 106, 47, .09); color: var(--navy);
}}

ul, ol {{ margin: 1.2rem 0 1.5rem; padding-left: 1.5rem; }}
li {{ margin-bottom: .7rem; padding-left: .3rem; }}
li::marker {{ color: var(--gold); }}

/* вводная врезка */
.note {{
  margin: 1.8rem 0 2rem; padding-left: 1.5rem;
  border-left: 2px solid var(--gold); color: var(--ink-soft);
}}
.note p:last-child, .note ul:last-child, .note ol:last-child {{ margin-bottom: 0; }}
.note ul, .note ol {{ margin: 1rem 0 1.2rem; }}

/* ------------------------------------------------ таблицы */
.tbl-wrap {{ overflow-x: auto; margin: 1.8rem 0 2rem; }}
table {{ border-collapse: collapse; width: 100%; font-size: .95rem; line-height: 1.6; }}
thead th {{
  text-align: left; vertical-align: bottom; color: var(--navy);
  font-size: .78rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase;
  padding: 0 1.2rem .6rem 0; border-bottom: 2px solid var(--gold);
}}
tbody td {{
  padding: .75rem 1.2rem .75rem 0; vertical-align: top;
  border-bottom: 1px solid var(--rule-soft);
}}
tbody tr:last-child td {{ border-bottom: 1px solid var(--rule); }}
th:last-child, td:last-child {{ padding-right: 0; }}

/* ------------------------------------------------ печать */
@media print {{
  body {{ background: #fff; font-size: 11.5pt; }}
  .sheet {{ box-shadow: none; border: 0; max-width: none; padding: 0; }}
  .hero {{ background: #fff; color: #000; padding: 0 0 2rem; }}
  .hero-q, .hero-q em, .hero-mark {{ color: #000; }}
  .part {{ page-break-before: always; }}
  .art-head, h3 {{ page-break-after: avoid; }}
  .tbl-wrap, tr {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body>
{hero}
<div class="sheet">
{head}
{toc}
{body}
</div>
</body>
</html>
"""


def render(doc, lang='ru', hero=False, toc=True, hero_hint=''):
    hero_html, body_blocks = '', None
    if hero:
        hero_html, rest = render_hero(doc, hero_hint)
        doc = dict(doc, lead=rest)
        head_html = ''
        toc_html = ''
    else:
        title_html = html.escape(doc['title'])
        if ' о ' in title_html:
            title_html = title_html.replace(' о ', '<br>о ', 1)
        head_html = ('<header class="doc-head col"><h1 class="doc-title">%s</h1>'
                     '<div class="rule-double"></div></header>' % title_html)
        n_head = (sum(len(p['articles']) for p in doc['parts'])
                  + len([p for p in doc['parts'] if p['label'] or p['title']]))
        toc_html = ('<nav class="toc col" aria-label="Содержание">'
                    '<h2 class="toc-title">Содержание</h2>%s</nav>' % render_toc(doc)
                    ) if (toc and n_head >= 5) else ''

    return TEMPLATE.format(lang=lang, title=html.escape(doc['title']),
                           hero=hero_html, head=head_html, toc=toc_html,
                           body=render_body(doc))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--hero', action='store_true')
    ap.add_argument('--hero-hint', default='')
    ap.add_argument('--no-toc', action='store_true')
    ap.add_argument('--lang', default='ru')
    a = ap.parse_args()

    assert os.path.isfile(a.src), a.src
    md = open(a.src, encoding='utf-8').read()
    assert md.strip(), 'пустой исходник'

    doc = parse(md)
    assert doc['title'], 'не найден заголовок H1'

    out = render(doc, a.lang, hero=a.hero, toc=not a.no_toc, hero_hint=a.hero_hint)
    guard.write(a.dst, out)

    arts = sum(len(p['articles']) for p in doc['parts'])
    print('OK  %-46s -> %-14s частей: %d, разделов: %d, %d КБ'
          % (os.path.basename(a.src)[:46], os.path.basename(a.dst),
             len([p for p in doc['parts'] if p['label'] or p['title']]), arts,
             len(out.encode('utf-8')) // 1024))


if __name__ == '__main__':
    # Отказ замка печатается человеку, а не трассировкой: произошло
    # ровно то, ради чего он поставлен, и это не поломка скрипта.
    try:
        main()
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
