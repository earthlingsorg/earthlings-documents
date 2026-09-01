# -*- coding: utf-8 -*-
u"""Один шрифт вместо ста одного среза - для китайских страниц сайта.

Что было измерено. Китайские страницы подключают `css/fonts-zh.css`: 202
правила @font-face, 185 КБ разметки, 62 КБ после сжатия - и всё это держит
отрисовку. Но лист не главная беда. Нарезка по `unicode-range` заставляет
браузер тянуть каждый срез, в котором нашёлся хоть один знак страницы:

    zh01-declaration.html   906 знаков, 48 срезов, 2920 КБ
    zh02-civic-voice.html  1155 знаков, 54 среза,  3311 КБ
    zh/index.html           622 знака,  42 среза,  2581 КБ

Около трёх мегабайт шрифтов на страницу. Срезы у Google нарезаны под
произвольный текст в вебе; у нас текст не произвольный - это закрытый
корпус, и во всех китайских страницах вместе 1740 разных знаков.

Что делает этот скрипт. Собирает знаки со ВСЕХ китайских страниц разом и
печёт по одному файлу на семейство. Разом, а не постранично, намеренно: один
файл на весь корпус читатель скачивает один раз и дальше берёт из кэша, а
постраничные субсеты заставляли бы качать заново на каждой странице.

Сверх текста добавлены ASCII целиком (адрес сайта, номера, слово Earthlings)
и китайская пунктуация: она стоит копейки по весу, а её нехватка означала бы
пустой квадрат посреди фразы.

Исходные шрифты в репозитории сайта не лежат и лежать не должны - Noto Sans
SC весит 17 МБ. Путь к ним передаётся аргументом.

Запуск:
    python _tools/make_zh_subset.py --sans <NotoSansSC-Regular.ttf> \
                                    --serif <NotoSerifSC-Regular.ttf>

Выход: _v2/fonts/zh-sans.woff2, _v2/fonts/zh-serif.woff2 и новый
       _v2/css/fonts-zh.css на два правила вместо двухсот двух.
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

# Знаки, которые добавляются к тексту всегда. Пунктуация - потому что её
# нехватка видна как пустой квадрат; ASCII - потому что латиница и цифры
# встречаются в китайском тексте (Earthlings, даты, адреса) и должны быть
# набраны тем же шрифтом, а не подстановкой.
ALWAYS = (
    [chr(c) for c in range(0x20, 0x7F)] +
    [chr(c) for c in range(0x3000, 0x3040)] +      # CJK-пунктуация
    [chr(c) for c in range(0xFF01, 0xFF65)] +      # полноширинные формы
    ['‘', '’', '“', '”', '—', '…', '·']
)


def corpus_chars():
    u"""Знаки со всех китайских страниц. Пустой набор - отказ, а не «готово»:
    проверка на нуле данных напечатала бы победу и испекла пустой шрифт."""
    files = sorted(glob.glob(os.path.join(V2, 'documents', 'zh', '*.html')))
    files += [os.path.join(V2, 'zh', 'index.html'),
              os.path.join(V2, 'zh', 'address.html')]
    files = [f for f in files if os.path.isfile(f)]
    assert files, u'китайских страниц не найдено - печь субсет не из чего'

    chars = set(ALWAYS)
    for f in files:
        s = io.open(f, encoding='utf-8').read()
        body = s.split('<body', 1)[1] if '<body' in s else s
        body = re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>', '', body)
        text = re.sub(r'<[^>]+>', ' ', body)
        chars.update(text)
    chars = {c for c in chars if ord(c) > 0x1F}
    assert len(chars) > 500, u'знаков всего %d - похоже, разбор сломался' % len(chars)
    return chars


def bake(src, dst, chars):
    u"""Субсет одного семейства. Недостающие знаки перечисляются, а не
    замалчиваются: пустой квадрат посреди иероглифов заметит читатель, а не
    сборка."""
    from fontTools import subset
    from fontTools.ttLib import TTFont

    assert os.path.isfile(src), src
    have = set(TTFont(src, lazy=True).getBestCmap())

    # Из запроса выбрасывается то, чего в исходнике нет и быть не должно:
    # в переключателе языка на КАЖДОЙ странице стоят арабские и деванагари
    # подписи, а китайский шрифт их не покрывает и покрывать не обязан - на
    # китайской странице они и сегодня набираются подстановкой.
    #
    # Тревогу поднимают только недостающие иероглифы и кана: их отсутствие
    # означало бы пустой квадрат посреди китайской фразы.
    def cjk(c):
        o = ord(c)
        return (0x2E80 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF
                or 0x3000 <= o <= 0x30FF or 0xFF00 <= o <= 0xFFEF)

    missing = sorted(c for c in chars if ord(c) not in have and cjk(c))
    chars = {c for c in chars if ord(c) in have}

    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.desubroutinize = True
    opts.layout_features = ['*']
    opts.drop_tables += ['DSIG']
    opts.notdef_outline = True
    font = subset.load_font(src, opts)
    subsetter = subset.Subsetter(options=opts)
    subsetter.populate(text=''.join(sorted(chars)))
    subsetter.subset(font)
    guard.check(dst)
    # Переменный исходник остаётся переменным: один файл покрывает весь
    # промежуток насыщенности, и второй для полужирного не нужен.
    # Переменный исходник остаётся переменным, и объявлять надо РЕАЛЬНЫЙ
    # диапазон его оси, а не выдуманный: если написать 400-700 там, где ось
    # идёт от 100, браузер не выйдет за объявленное, а если написать
    # диапазон у статического шрифта - перестанет синтезировать полужирное.
    axis = None
    if 'fvar' in font:
        for ax in font['fvar'].axes:
            if ax.axisTag == 'wght':
                axis = '%d %d' % (ax.minValue, ax.maxValue)
    subset.save_font(font, dst, opts)
    font.close()
    return os.path.getsize(dst), missing, axis


CSS_HEAD = u"""/* Письменность zh: один файл на семейство вместо ста одного среза.

   Испечено _tools/make_zh_subset.py по знакам, которые реально встречаются
   в китайском корпусе (%d штук). Руками не править: правка переживёт до
   следующей сборки.

   Почему не нарезка по unicode-range, как у Google. Их нарезка рассчитана
   на произвольный текст: браузер тянет каждый срез, в котором нашёлся хоть
   один знак страницы. Замер до этой правки: 42-54 среза и 2.6-3.3 МБ
   шрифтов НА КАЖДУЮ китайскую страницу. Наш текст не произвольный - это
   закрытый корпус, и один файл на всё покрывает его целиком, скачивается
   один раз и дальше берётся из кэша.

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
    ap.add_argument('--sans', required=True, help='NotoSansSC-Regular.ttf')
    ap.add_argument('--sans-bold', help='NotoSansSC-Bold.ttf')
    ap.add_argument('--serif', help='NotoSerifSC-VF.otf или -Regular.ttf')
    ap.add_argument('--serif-bold', help='NotoSerifSC-Bold.ttf, если исходник не VF')
    a = ap.parse_args()

    chars = corpus_chars()
    print(u'знаков в китайском корпусе: %d' % len(chars))

    fonts_dir = os.path.join(V2, 'fonts')
    guard.makedirs(fonts_dir)

    # Начертания объявляются по отдельности, а не диапазоном 400-700.
    # Диапазон на СТАТИЧЕСКОМ шрифте - ловушка: он говорит браузеру, что
    # семейство покрывает весь промежуток, и тот перестаёт синтезировать
    # полужирное. Заголовки статей и <strong> в китайском вышли бы обычным
    # весом. У переменного исходника диапазон законен, и он объявляется
    # только для него.
    plan = [('Noto Sans SC', 400, a.sans, 'zh-sans.woff2'),
            ('Noto Sans SC', 700, a.sans_bold, 'zh-sans-bold.woff2'),
            ('Noto Serif SC', 400, a.serif, 'zh-serif.woff2'),
            ('Noto Serif SC', 700, a.serif_bold, 'zh-serif-bold.woff2')]

    faces = []
    total = 0
    for family, weight, src, name in plan:
        if not src:
            print(u'%-14s %d - исходника нет, начертание пропущено'
                  % (family, weight))
            continue
        size, missing, axis = bake(src, os.path.join(fonts_dir, name), chars)
        if axis and weight == 700:
            # Переменный файл этого семейства уже испечён и покрывает всю
            # ось - второй нужен только статическим исходникам.
            os.remove(os.path.join(fonts_dir, name))
            print(u'%-14s 700 - покрыт переменным файлом, пропущен' % family)
            continue
        total += size
        faces.append(FACE % (family, axis or str(weight), name))
        print(u'%-14s %3d  %-26s -> %6.0f КБ%s%s'
              % (family, weight, os.path.basename(src), size / 1024.0,
                 u'  (переменный %s)' % axis if axis else '',
                 u', НЕ ХВАТАЕТ: %d (%s)'
                 % (len(missing), ''.join(missing[:12])) if missing else ''))

    assert faces, u'не испечено ни одного семейства'
    css = CSS_HEAD % len(chars) + '\n' + '\n'.join(faces)
    guard.write(os.path.join(V2, 'css', 'fonts-zh.css'), css)
    print(u'')
    print(u'css/fonts-zh.css: правил %d, шрифтов %.0f КБ на весь корпус'
          % (len(faces), total / 1024.0))


if __name__ == '__main__':
    try:
        main()
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
