# -*- coding: utf-8 -*-
u"""Один шрифт на письменность вместо нарезки по unicode-range.

Что было измерено на живом дереве до этой правки:

    страница                знаков  срезов   шрифтов
    zh01-declaration.html      906      48   2920 КБ
    zh02-civic-voice.html     1155      54   3311 КБ
    hi01-declaration.html        -      10    716 КБ
    ar01-declaration.html        -      16    537 КБ
    ka01-declaration.html        -       2    104 КБ

Откуда столько. Листы `fonts-<язык>.css` унаследованы от боевого сайта, а
тот брал нарезку у Google Fonts. Нарезка рассчитана на ПРОИЗВОЛЬНЫЙ текст:
браузер тянет каждый срез, в котором нашёлся хоть один знак страницы, и на
китайском это пятьдесят файлов по шестьдесят килобайт.

Наш текст не произвольный. Это закрытый корпус: двадцать пять документов,
главная и Обращение. Во всех китайских страницах вместе 1907 разных знаков.
Один субсет ровно по ним покрывает корпус целиком, скачивается ОДИН раз на
весь сайт и дальше берётся из кэша - вместо нового набора срезов на каждой
странице.

Сверх текста в субсет кладутся ASCII целиком и пунктуация письменности: они
стоят копейки по весу, а нехватка знака означала бы пустой квадрат посреди
фразы.

Исходные шрифты в репозитории не лежат и лежать не должны - переменный Noto
Sans SC весит 17 МБ. Путь передаётся аргументом; лицензия OFL, скачивается
у notofonts.

Запуск:
    python _tools/make_script_subset.py --lang zh \
        --face "Noto Sans SC=/путь/NotoSansSC-Regular.ttf" \
        --face "Noto Serif SC=/путь/NotoSerifSC-VF.otf"

Выход: _v2/fonts/<язык>-<n>.woff2 и переписанный _v2/css/fonts-<язык>.css.
"""
import argparse
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import site_guard as guard                       # noqa: E402
from build_site_docs import SITE                 # noqa: E402

V2 = os.path.join(SITE, '_v2')

# Диапазоны, которые кладутся в субсет всегда, сверх текста страниц.
# ASCII - латиница и цифры внутри иноязычного текста (Earthlings, даты,
# адреса) должны быть набраны тем же шрифтом, а не подстановкой.
COMMON = [(0x20, 0x7E), (0x2010, 0x2027), (0x00A0, 0x00BF)]

# Пунктуация письменности: её нехватка заметнее всего, а весит она ничто.
BY_SCRIPT = {
    'zh': [(0x3000, 0x303F), (0xFF01, 0xFF64)],
    'ar': [(0x0600, 0x061F), (0x0660, 0x066F), (0x06D4, 0x06ED)],
    'hi': [(0x0964, 0x0965), (0x0966, 0x096F), (0x0951, 0x0957)],
    'ka': [(0x10FB, 0x10FB)],
}


def corpus_chars(lang):
    u"""Знаки со всех страниц языка. Пустой набор - отказ, а не «готово»:
    проверка на нуле данных напечатала бы победу и испекла пустой шрифт."""
    files = sorted(glob.glob(os.path.join(V2, 'documents', lang, '*.html')))
    files += [os.path.join(V2, lang, 'index.html'),
              os.path.join(V2, lang, 'manifest.html')]
    files = [f for f in files if os.path.isfile(f)]
    assert files, u'страниц языка %r не найдено' % lang

    chars = set()
    for a, z in COMMON + BY_SCRIPT.get(lang, []):
        chars.update(chr(c) for c in range(a, z + 1))
    for f in files:
        s = io.open(f, encoding='utf-8').read()
        body = s.split('<body', 1)[1] if '<body' in s else s
        body = re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>', '', body)
        chars.update(re.sub(r'<[^>]+>', ' ', body))
    chars = {c for c in chars if ord(c) > 0x1F}
    assert len(chars) > 200, u'знаков всего %d - похоже, разбор сломался' % len(chars)
    return chars, len(files)


def bake(src, dst, chars, script_ranges):
    u"""Субсет одного начертания. Возвращает вес, недостающие знаки своей
    письменности и диапазон оси насыщенности, если исходник переменный."""
    from fontTools import subset
    from fontTools.ttLib import TTFont

    assert os.path.isfile(src), src
    have = set(TTFont(src, lazy=True).getBestCmap())

    # Из запроса выбрасывается то, чего в исходнике нет и быть не должно: в
    # переключателе языка на КАЖДОЙ странице стоят подписи на всех девяти
    # письменностях, и арабский шрифт не обязан нести деванагари.
    #
    # Тревогу поднимает только нехватка знаков СВОЕЙ письменности: вот она
    # означала бы пустой квадрат посреди фразы.
    def own(c):
        return any(a <= ord(c) <= z for a, z in script_ranges)

    missing = sorted(c for c in chars if ord(c) not in have and own(c))
    chars = {c for c in chars if ord(c) in have}

    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.desubroutinize = True
    opts.layout_features = ['*']          # лигатуры и огласовки обязательны
    opts.drop_tables += ['DSIG']
    opts.notdef_outline = True
    font = subset.load_font(src, opts)
    sub = subset.Subsetter(options=opts)
    sub.populate(text=''.join(sorted(chars)))
    sub.subset(font)

    # Переменный исходник остаётся переменным, и объявлять надо РЕАЛЬНЫЙ
    # диапазон его оси. Диапазон у статического шрифта - ловушка: браузер
    # решит, что семейство покрывает весь промежуток, и перестанет
    # синтезировать полужирное.
    axis = None
    if 'fvar' in font:
        for ax in font['fvar'].axes:
            if ax.axisTag == 'wght':
                axis = '%d %d' % (ax.minValue, ax.maxValue)

    guard.check(dst)
    subset.save_font(font, dst, opts)
    font.close()
    return os.path.getsize(dst), missing, axis


HEAD = u"""/* Письменность %s: по одному файлу на семейство вместо нарезки.

   Испечено _tools/make_script_subset.py по знакам, которые реально
   встречаются на страницах языка (%d знаков, %d страниц).
   Руками не править: правка переживёт до следующей сборки.

   Почему не нарезка по unicode-range. Она рассчитана на произвольный текст:
   браузер тянет каждый срез, где нашёлся хоть один знак страницы. Замер до
   этой правки - %s. Наш текст не произвольный, это закрытый корпус, и один
   файл покрывает его целиком, скачивается один раз и дальше берётся из кэша.

   font-display: swap - текст виден сразу, шрифт подменяется по приходе. */
"""

FACE = u"""@font-face {
  font-family: '%s';
  font-style: normal;
  font-weight: %s;
  font-display: swap;
  src: url(/fonts/%s) format('woff2');
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', required=True, choices=sorted(BY_SCRIPT))
    ap.add_argument('--face', action='append', required=True,
                    metavar='СЕМЕЙСТВО=путь',
                    help='можно повторять: --face "Noto Sans SC=/путь.ttf"')
    ap.add_argument('--was', default=u'см. историю правки',
                    help='что было по весу, для комментария в листе')
    a = ap.parse_args()

    chars, pages = corpus_chars(a.lang)
    ranges = BY_SCRIPT[a.lang] + [(0x0590, 0x08FF)] if a.lang == 'ar' else \
        BY_SCRIPT[a.lang] + {'zh': [(0x2E80, 0x9FFF), (0xF900, 0xFAFF)],
                             'hi': [(0x0900, 0x097F)],
                             'ka': [(0x10A0, 0x10FF), (0x1C90, 0x1CBF)]}[a.lang]
    print(u'знаков в корпусе %s: %d (страниц %d)' % (a.lang, len(chars), pages))

    fonts_dir = os.path.join(V2, 'fonts')
    guard.makedirs(fonts_dir)

    faces, total = [], 0
    for i, spec in enumerate(a.face, 1):
        family, _, src = spec.partition('=')
        assert src, u'ожидалось СЕМЕЙСТВО=путь, получено %r' % spec
        name = '%s-%d.woff2' % (a.lang, i)
        size, missing, axis = bake(src, os.path.join(fonts_dir, name),
                                   chars, ranges)
        total += size
        faces.append(FACE % (family, axis or '400', name))
        print(u'%-22s %-26s -> %6.0f КБ%s%s'
              % (family, os.path.basename(src), size / 1024.0,
                 u'  (переменный %s)' % axis if axis else u'  (статический)',
                 u', НЕ ХВАТАЕТ: %d (%s)' % (len(missing), ''.join(missing[:12]))
                 if missing else ''))

    assert faces, u'не испечено ни одного начертания'
    css = HEAD % (a.lang, len(chars), pages, a.was) + '\n' + '\n'.join(faces)
    guard.write(os.path.join(V2, 'css', 'fonts-%s.css' % a.lang), css)
    print(u'')
    print(u'css/fonts-%s.css: правил %d, шрифтов %.0f КБ на весь корпус'
          % (a.lang, len(faces), total / 1024.0))


if __name__ == '__main__':
    try:
        main()
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
