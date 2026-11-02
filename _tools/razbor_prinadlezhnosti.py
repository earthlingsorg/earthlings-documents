# -*- coding: utf-8 -*-
u"""Разбор слова "членство" на тематических страницах: три кучи.

Прибор ничего не правит. Он выписывает КАЖДОЕ вхождение семьи слов с
окрестностью в +-120 знаков, говорит, стоит оно в шапке страницы или в теле,
и раскладывает находки на три кучи.

Три кучи, и ровно три - описание и код обязаны сходиться, иначе по описанию
правят не глядя:

    ЗАКОННОЕ - рядом признак законности: государства-члены, членство в
        международных организациях, члены Совета и Core Nodes (это орган, а
        не народ), цитата статьи 33(1) UNDRIP, племенные реестры США,
        притязание рома 2000 года, формула по церковным метрическим книгам.
        Не трогать.

    ДРЕЙФ - признака законности нет, слово стоит в утверждающей половине
        фразы и говорит о принадлежности к народу Earthlings. Править.

    СПОРНОЕ - признака законности нет, НО слово стоит в заголовке или в
        отрицаемой половине фразы ("субъект, а не член", "a subject, not a
        member"). Там слово может нести само различение, и убрать его -
        значит убрать мысль. Решается глазами, по одному, с чтением всего
        абзаца.

Регистр считается в Python с re.IGNORECASE | re.UNICODE: `grep -i` в Git Bash
на этой машине НЕ складывает регистры кириллицы.

Запуск:
    python _tools/razbor_prinadlezhnosti.py                 все девять языков
    python _tools/razbor_prinadlezhnosti.py en ru            только эти языки
    python _tools/razbor_prinadlezhnosti.py --tree _v2       только это дерево
    python _tools/razbor_prinadlezhnosti.py --pile sporn     только эта куча
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
assert os.path.isdir(SITE), (
    u'не найден репозиторий сайта: %s\n'
    u'Ожидается earth-lings-site рядом с этим репозиторием. Если он лежит в '
    u'другом месте - EARTHLINGS_SITE=/путь/к/earth-lings-site' % SITE)

sys.path.insert(0, HERE)
from zamer_prinadlezhnosti import (FAMILY, LANGS, TREES,  # noqa: E402
                                   lang_of, pages_of)

WINDOW = 120

# Признак законности: слово рядом, по которому видно, что речь не о народе
# Earthlings. Ищется в окрестности находки, без учёта регистра.
LEGIT_MARKS = [
    u'member state', u'member-state', u'member states',
    u'государств-член',
    u'государства-член',
    u'государство-член',
    u'Mitgliedstaat', u'état membre', u'estado miembro',
    u'United Nations', u'UNDRIP', u'33(1)', u'Declaration on the Rights of',
    u'ООН', u'Декларация ООН',
    u'Core Node', u'Core Nodes', u'Council', u'Совета',
    u'Совет ', u'tribal', u'enrollment',
    u'племен', u'Roma', u'рома',
    u'parish', u'метрическ',
    u'NATO', u'НАТО', u'European Union',
    u'Евросоюз',
]

# Отрицаемая половина фразы: слово стоит после отрицания, и там оно может
# нести само различение. Ищется в той же окрестности.
NEGATED_MARKS = [
    u', not a member', u', not members', u'not a member',
    u'not a membership', u'rather than a member', u'is not a member',
    u'а не член',          # а не член
    u'не член',                 # не член
    u'не в член',          # не в членстве
    u'никакого член',
]

# Шапка страницы: всё до </head>, плюс теги заголовков в теле.
HEAD_TAGS = ['<title>', 'name="description"', 'og:description',
             'twitter:description', 'og:title', 'twitter:title',
             'application/ld+json']
HEADING_RX = re.compile(r'<(h1|h2|h3|h4)\b[^>]*>(.*?)</\1>',
                        re.S | re.IGNORECASE)


def ranges_of_headings(text):
    return [(m.start(2), m.end(2)) for m in HEADING_RX.finditer(text)]


def find_all(text, lang):
    u"""Все вхождения семьи слов. Длинный корень съедает короткий."""
    taken = []
    s = text
    for w in FAMILY.get(lang, []):
        rx = re.compile(re.escape(w), re.IGNORECASE | re.UNICODE)
        for m in rx.finditer(s):
            taken.append((m.start(), m.end(), m.group(0), w))
        s = rx.sub(lambda m: u' ' * len(m.group(0)), s)
    taken.sort()
    return taken


def classify(text, start, end, head_end, headings):
    u"""Куча и место. Три кучи, ровно три."""
    lo = max(0, start - WINDOW)
    hi = min(len(text), end + WINDOW)
    ctx = text[lo:hi]
    low = ctx.lower()

    if start < head_end:
        where = u'шапка'
    elif any(a <= start < b for a, b in headings):
        where = u'заголовок'
    else:
        where = u'тело'

    for mark in LEGIT_MARKS:
        if mark.lower() in low:
            return u'ЗАКОННОЕ', where, ctx, mark

    # Отрицание ищется в узкой окрестности, а не во всех +-120 знаках:
    # иначе отрицание из заголовка пометит соседнее вхождение абзацем ниже,
    # и в третью кучу попадёт то, что надо просто править.
    near = text[max(0, start - 40):end + 10].lower()
    for mark in NEGATED_MARKS:
        if mark.lower() in near:
            return u'СПОРНОЕ', where, ctx, u'отрицаемая половина: %s' % mark

    if where in (u'заголовок', u'шапка'):
        return u'СПОРНОЕ', where, ctx, u'слово в %s' % where

    return u'ДРЕЙФ', where, ctx, u''


def one_line(s):
    return re.sub(r'\s+', u' ', s).strip()


def scan(langs, trees, piles):
    rows = []
    for tree, root in TREES:
        if trees and tree not in trees and not any(t in tree for t in trees):
            continue
        pages = pages_of(root)
        assert pages, u'пустой ввод: в дереве %s нет страниц' % tree
        for topic, path in pages:
            lang = lang_of(path)
            if langs and lang not in langs:
                continue
            text = io.open(path, encoding='utf-8').read()
            assert text.strip(), u'пустой ввод: %s' % path
            head_end = text.find('</head>')
            if head_end < 0:
                head_end = 0
            headings = ranges_of_headings(text)
            for start, end, hit, root_w in find_all(text, lang):
                pile, where, ctx, why = classify(text, start, end,
                                                 head_end, headings)
                if piles and not any(p.lower() in pile.lower() for p in piles):
                    continue
                rows.append({'tree': tree, 'topic': topic or u'(хаб)',
                             'lang': lang, 'path': path, 'pile': pile,
                             'where': where, 'hit': hit, 'root': root_w,
                             'why': why, 'ctx': one_line(ctx),
                             'line': text.count(u'\n', 0, start) + 1})
    return rows


def selftest():
    chlen = u'член'
    doc = (u'<html><head><title>Народ</title></head>'
           u'<body><h3>Субъект, а '
           u'не %s</h3><p>%s</p><p>%s решает'
           u'</p></body></html>' % (chlen, u'слово ' * 12,
                                    chlen.capitalize()))
    hits = find_all(doc, 'ru')
    assert len(hits) == 2, u'не оба регистра: %r' % (hits,)
    head_end = doc.find('</head>')
    headings = ranges_of_headings(doc)
    piles = [classify(doc, s, e, head_end, headings)[0] for s, e, _h, _r in hits]
    assert piles == [u'СПОРНОЕ', u'ДРЕЙФ'], u'кучи разошлись: %r' % (piles,)

    legit = u'<p>UNDRIP: member states shall</p>'
    h = find_all(legit, 'en')
    assert h, u'законное не найдено вовсе'
    assert classify(legit, h[0][0], h[0][1], 0, [])[0] == u'ЗАКОННОЕ'

    clean = (u'<p>принадлеж'
             u'ность</p>')
    assert find_all(clean, 'ru') == [], u'замена поймана как дефект'


def main(argv):
    selftest()
    langs, trees, piles = [], [], []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--tree':
            i += 1
            trees.append(argv[i])
        elif a == '--pile':
            i += 1
            piles.append(argv[i])
        elif a in LANGS:
            langs.append(a)
        else:
            sys.stderr.write(u'не понял довод: %s\n' % a)
            return 2
        i += 1

    rows = scan(langs, trees, piles)
    out = sys.stdout
    counts = {}
    for r in rows:
        counts[r['pile']] = counts.get(r['pile'], 0) + 1

    for pile in (u'ЗАКОННОЕ', u'СПОРНОЕ', u'ДРЕЙФ'):
        sel = [r for r in rows if r['pile'] == pile]
        out.write(u'\n=== %s: %d ===\n' % (pile, len(sel)))
        for r in sel:
            out.write(u'\n%s / %s / %s : %s  [%s]%s\n' % (
                r['tree'], r['topic'], r['lang'], r['hit'], r['where'],
                u'  <- ' + r['why'] if r['why'] else u''))
            out.write(u'    %s:%d\n' % (r['path'], r['line']))
            out.write(u'    ...%s...\n' % r['ctx'])

    out.write(u'\nИТОГО: %d вхождений; %s\n' % (
        len(rows),
        u', '.join(u'%s %d' % (k, counts[k]) for k in sorted(counts))))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
