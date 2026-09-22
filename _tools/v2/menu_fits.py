# -*- coding: utf-8 -*-
u"""Помещается ли строка меню в шапку - измерением, а не на глаз.

«Должно влезть» здесь не аргумент: строка либо переносится на вторую, либо
вылезает за край. Ширина считается по настоящим файлам шрифтов, по таблицам
cmap и hmtx: Verdana для пунктов меню, Cormorant для слова «Earthlings» рядом
со значком, Montserrat для кнопки. Величины - кегли, просветы, ширина
контейнера - читаются из живого tokens.css, а не переписываются сюда: копия
разошлась бы с оригиналом при первой правке, и проверка начала бы мерить не то,
что показывается.

Первая версия этой проверки опровергла прикидку на глаз сразу дважды: самым
широким оказался не русский, а французский, и он не помещался даже на широком
экране, потому что кегль рос дальше, чем росло место.

Арабский, хинди, китайский и грузинский Verdana не покрывает - там работает
подстановка Noto, ширину которой этот скрипт не знает и честно об этом говорит,
а не выдаёт выдуманное число. Пункты меню там короткие (в китайском 2-4 знака),
так что риск низкий, но проверен он глазами, а не здесь.

Запуск:  python _v2/tools/menu_fits.py
Выход:   0 - все измеримые языки помещаются, 1 - какой-то нет.
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
V2 = os.path.join(SITE, '_v2')
# Величины берутся из ИСХОДНИКА стилей, а не из выдачи: выдача
# порождается снятием комментариев, и мерить надо то, что написано.
TOKENS = os.path.join(os.path.dirname(HERE), 'css', 'tokens.css')
FONTS = os.path.join(V2, 'fonts')

import chrome as C                        # noqa: E402
from fontTools.ttLib import TTFont        # noqa: E402
from fontTools.varLib import instancer    # noqa: E402

# Пункты меню набраны Verdana - см. --sans-nav. Слово «Earthlings» с
# 2026-08-22 набрано Montserrat 800, а не Cormorant, и это меняет счёт: при
# одном кегле оно шире в 1.38 раза. Montserrat здесь переменный, поэтому
# начертание надо закрепить на 800: без этого fontTools вернёт ширины
# начертания по умолчанию, то есть 400, и проверка занизит слово.
BRAND_WEIGHT = 800
BRAND_TRACKING = -0.016   # letter-spacing из chrome.css, в em на знак
FACES = {
    'nav':   [(r'C:\Windows\Fonts\verdanab.ttf', None)],
    'brand': [(os.path.join(FONTS, 'Montserrat-latin.woff2'), BRAND_WEIGHT)],
}

# Точки проверки. Первая - порог, ниже которого показывается бургер.
VIEWPORTS = (1248, 1280, 1366, 1440, 1600, 1920, 2560)

PAD = 32          # clamp(1.25rem, 5vw, 2rem), максимум
GAP_MARK = 0.6 * 16   # просвет между словом и значком, .6rem из chrome.css
# Переключатель языка - кнопка с заливкой (с 2026-08-22), а не голый текст:
# к ширине надписи прибавляются её поля, .9rem с каждой стороны.
LANG_BTN = 2 * 0.9 * 16
ROOT = 16.0


def tokens():
    src = io.open(TOKENS, encoding='utf-8').read()
    body = src[src.index(':root'):]
    raw = dict((k, v.split('/*')[0].strip())
               for k, v in re.findall(r'--([a-z0-9-]+)\s*:\s*([^;]+);', body))
    assert raw, u'в %s не нашлось ни одной переменной' % TOKENS
    return raw


def px(raw, name, vw):
    u"""Значение токена в пикселях. Понимает Npx, Nrem и clamp(a, b + cvw, d)."""
    v = raw.get(name)
    assert v is not None, u'нет переменной --%s' % name
    m = re.match(r'^clamp\(\s*([\d.]+)rem\s*,\s*([\d.]+)rem\s*\+\s*'
                 r'([\d.]+)vw\s*,\s*([\d.]+)rem\s*\)$', v)
    if m:
        lo, base, slope, hi = (float(g) for g in m.groups())
        return min(max(lo * ROOT, base * ROOT + slope / 100.0 * vw), hi * ROOT)
    m = re.match(r'^clamp\(\s*([\d.]+)rem\s*,\s*([\d.]+)vw\s*,\s*([\d.]+)rem\s*\)$', v)
    if m:
        lo, slope, hi = (float(g) for g in m.groups())
        return min(max(lo * ROOT, slope / 100.0 * vw), hi * ROOT)
    m = re.match(r'^([\d.]+)rem$', v)
    if m:
        return float(m.group(1)) * ROOT
    m = re.match(r'^([\d.]+)px$', v)
    assert m, u'не умею читать --%s: %r' % (name, v)
    return float(m.group(1))


def load(paths):
    faces = []
    for p, wght in paths:
        assert os.path.isfile(p), u'нет файла шрифта %s' % p
        f = TTFont(p, fontNumber=0)
        if wght is not None:
            assert 'fvar' in f, u'%s не переменный, начертание не закрепить' % p
            f = instancer.instantiateVariableFont(f, {'wght': wght},
                                                  inplace=True)
        faces.append((f['head'].unitsPerEm, f.getBestCmap(), f['hmtx']))
    return faces


def em(s, faces):
    u"""Ширина строки в em. None, если знак не покрыт ни одним подмножеством."""
    total = 0
    for ch in s:
        for upm, cmap, hmtx in faces:
            g = cmap.get(ord(ch))
            if g is not None:
                total += hmtx[g][0] / float(upm)
                break
        else:
            return None
    return total


def main():
    raw = tokens()
    faces = dict((k, load(v)) for k, v in FACES.items())

    brand_em = em(u'Earthlings', faces['brand'])
    assert brand_em, u'Montserrat не покрывает слово Earthlings - это уже беда'
    # Разрядка отрицательная и стоит после каждого знака, включая последний.
    brand_em += BRAND_TRACKING * len(u'Earthlings')

    rows, bad, skipped = [], 0, []
    rows.append(u'контейнер %.0f px, значок со словом «Earthlings» %.0f px'
                % (px(raw, 'container', 1920),
                   px(raw, 'logo-size', 1920) + GAP_MARK
                   + brand_em * px(raw, 'fs-brand', 1920)))
    rows.append(u'')
    rows.append(u'%-3s %6s %8s %9s %9s %8s' % (u'яз', u'окно', u'меню',
                                               u'действия', u'доступно', u'запас'))
    rows.append(u'-' * 62)

    for lang in C.ALL_LANGS:
        ems = [em(C.t(lang, key).upper(), faces['nav'])
               for key, _num, _sub in C.SECTIONS]
        code_em = em(lang.upper(), faces['nav'])
        if any(e is None for e in ems) or code_em is None:
            skipped.append(lang)
            continue
        for vw in VIEWPORTS:
            fs = px(raw, 'fs-nav-bar', vw)
            # Значок теперь тоже текучий, поэтому читается из токенов, а не
            # стоит здесь числом: списанная копия разошлась бы с оригиналом.
            brand = (px(raw, 'logo-size', vw) + GAP_MARK
                     + brand_em * px(raw, 'fs-brand', vw))
            # Поля под плюсик больше нет: значок снят 2026-08-22, пункты
            # разделяет только просвет.
            menu = (sum(e * fs for e in ems)
                    + (len(ems) - 1) * px(raw, 'gap-nav', vw))
            # Кнопки «Вступить» в шапке тоже нет - справа остался один
            # переключатель языка.
            acts = code_em * fs + LANG_BTN
            # Между группами шапки стоит --gap-group, а не --gap-sm: их два,
            # логотип-меню и меню-язык. Модель обязана считать тот же
            # просвет, что рисуется, иначе проверка мерит не ту шапку.
            avail = (min(px(raw, 'container', vw), vw - 2 * PAD) - brand
                     - 2 * px(raw, 'gap-group', vw))
            ok = menu + acts <= avail
            bad += 0 if ok else 1
            rows.append(u'%-3s %6d %8.0f %9.0f %9.0f %8.0f  %s'
                        % (lang, vw, menu, acts, avail,
                           avail - menu - acts, u'' if ok else u'НЕ ПОМЕЩАЕТСЯ'))
        rows.append(u'')

    if skipped:
        rows.append(u'не измерялись (знаков нет в Verdana, работает подстановка '
                    u'Noto): %s' % u', '.join(skipped))
    rows.append(u'кегль пункта: %.1f px при %d, %.1f px при %d'
                % (px(raw, 'fs-nav-bar', VIEWPORTS[0]), VIEWPORTS[0],
                   px(raw, 'fs-nav-bar', VIEWPORTS[-1]), VIEWPORTS[-1]))
    rows.append(u'не помещается: %d' % bad)
    io.open(os.path.join(HERE, 'menu-fits-report.txt'), 'w',
            encoding='utf-8').write(u'\n'.join(rows) + u'\n')
    sys.stdout.write('menu fits: failed=%d -> %s\n'
                     % (bad, os.path.join(HERE, 'menu-fits-report.txt')))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
