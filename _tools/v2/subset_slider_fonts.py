# -*- coding: utf-8 -*-
u"""Подрезает шрифты письменностей под слайдер девяти языков.

Слайдер показывает название Декларации на девяти языках, и весь его смысл в
том, что письменности видно. Значит арабская вязь, деванагари, иероглифы и
мхедрули обязаны нарисоваться у любого читателя, а не только у того, у кого
эти шрифты стоят в системе.

Возить ради этого полное самохостинг-хозяйство боевого сайта нельзя: только
объявления для китайского там 737 КБ, а сами файлы Noto весят 14 МБ. Здесь
берётся ровно то, что нужно: знаки девяти заголовков и ничего сверх.

Семейства называются своими именами - «Slide Arabic» и так далее, - а не
«Noto Naskh Arabic». Это принципиально: подрезанный шрифт под своим именем
подхватился бы браузером для ВСЕГО арабского текста на странице и молча
потерял бы знаки, которых в подрезке нет. Под отдельным именем он работает
только там, где им пользуются намеренно.

Полное самохостинг-покрытие для zh, ar, hi и ka - отдельная задача; она
понадобится, когда эти языки приедут в новое дерево.

Запуск:  python _v2/tools/subset_slider_fonts.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# TOOLS - родительский каталог: этот файл лежит в _tools/v2/. Путь к
# сайту берётся у build_site_docs, а не считается «на два уровня вверх»:
# так было, пока инструмент лежал в earth-lings-site/_v2/tools, и после
# переезда сюда счёт стал указывать в earthlings-documents - проверка
# падала на «нет файла шрифта». У build_site_docs резолвер один и он
# понимает EARTHLINGS_SITE.
TOOLS = os.path.dirname(HERE)
assert os.path.isdir(TOOLS), u'нет каталога %s' % TOOLS
sys.path.insert(0, TOOLS)

from build_site_docs import SITE        # noqa: E402
SRC = os.path.join(SITE, 'fonts')
DST = os.path.join(SITE, '_v2', 'fonts')

import chrome as C                                     # noqa: E402
from fontTools.ttLib import TTFont                     # noqa: E402
from fontTools.subset import Subsetter, Options        # noqa: E402

DOCS = os.path.join(SITE, 'documents')

# Какая письменность каким семейством закрывается. Файлы боевого дерева
# нарезаны Google по подмножествам и названы по хешу, поэтому ищем по префиксу
# и берём тот файл, который реально покрывает нужные знаки.
SCRIPTS = [
    ('arabic',     'ar', 'noto-naskh-arabic'),
    ('devanagari', 'hi', 'noto-sans-devanagari'),
    ('han',        'zh', 'noto-serif-sc'),
    ('georgian',   'ka', 'noto-serif-georgian'),
]


def decl_title(lang):
    import glob
    f = glob.glob(os.path.join(DOCS, lang, '%s01*.html' % lang))
    assert f, u'нет собранной страницы %s01' % lang
    s = io.open(f[0], encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    assert m, u'в %s нет заголовка h1' % f[0]
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip()


def needed(lang):
    u"""Знаки, которые слайд обязан нарисовать: название Декларации и подпись
    языка на нём же."""
    return set(decl_title(lang)) | set(C.LANG_LABEL[lang])


def covering(prefix, chars):
    u"""Набор файлов семейства, вместе покрывающих все нужные знаки.

    Одним файлом обойтись удаётся не всегда: китайские шрифты Google режет на
    сотню подмножеств, и четыре иероглифа названия расходятся по разным.
    Поэтому берём столько файлов, сколько нужно, - каждый подрежется до своей
    доли, а объявлены они будут одним семейством, как и у Google.
    """
    files = sorted(f for f in os.listdir(SRC)
                   if f.startswith(prefix) and f.endswith('.woff2'))
    assert files, u'в %s нет файлов с началом %r' % (SRC, prefix)
    cover = {}
    for f in files:
        cmap = TTFont(os.path.join(SRC, f), fontNumber=0).getBestCmap()
        got = {c for c in chars if ord(c) in cmap}
        if got:
            cover[f] = got
    picked, left = [], set(chars)
    while left and cover:
        f = max(cover, key=lambda k: len(cover[k] & left))
        got = cover.pop(f) & left
        if not got:
            break
        picked.append((f, got))
        left -= got
    return picked, left


def main():
    if not os.path.isdir(DST):
        os.makedirs(DST)
    rows, bad = [], 0
    for name, lang, prefix in SCRIPTS:
        chars = needed(lang)
        # латиница и пробелы приедут из Cormorant, подрезать их незачем
        chars = {c for c in chars if ord(c) > 0x2FF}
        assert chars, u'для %s не осталось ни одного знака - проверьте заголовок' % lang
        picked, miss = covering(prefix, chars)
        if miss:
            bad += 1
            rows.append(u'%-11s ПРОВАЛ: файлы %s* не покрывают знаки %s'
                        % (name, prefix, u' '.join(sorted(miss))))
            continue
        for i, (src, got) in enumerate(picked):
            opts = Options()
            opts.layout_features = ['*']      # арабской вязи нужны лигатуры
            opts.notdef_outline = True
            opts.flavor = 'woff2'
            f = TTFont(os.path.join(SRC, src), fontNumber=0)
            sub = Subsetter(options=opts)
            sub.populate(text=u''.join(sorted(got)))
            sub.subset(f)
            out = os.path.join(DST, 'slide-%s%s.woff2'
                               % (name, '' if i == 0 else '-%d' % (i + 1)))
            f.save(out)
            rows.append(u'%-11s %-34s %3d знаков -> %5d байт'
                        % (name if i == 0 else '', src, len(got),
                           os.path.getsize(out)))
    rows.append(u'')
    rows.append(u'письменностей: %d, провалов: %d' % (len(SCRIPTS), bad))
    io.open(os.path.join(HERE, 'slider-fonts-report.txt'), 'w',
            encoding='utf-8').write(u'\n'.join(rows) + u'\n')
    sys.stdout.write('slider fonts: failed=%d -> %s\n'
                     % (bad, os.path.join(HERE, 'slider-fonts-report.txt')))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
