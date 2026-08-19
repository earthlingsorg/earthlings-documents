# -*- coding: utf-8 -*-
"""Предполёт языка: проверить письменность, шрифт и PDF ДО начала перевода.

Заводится после грузинской сессии, где полчаса ушло на открытие, которое надо
было сделать за пять минут до старта: готовая статика Noto Serif Georgian с
notofonts.github.io содержит 2 ASCII-символа из 95, и PDF Манифеста вышел бы с
пустыми квадратами вместо `Earthlings`, ёлочек и `earth-lings.org`. Латиница
есть только в сборке Google Fonts, а она вариативная, и reportlab вариативные
шрифты не открывает вовсе.

Для арабского и хинди цена ошибки другая и выясняться на восьмом часу не
должна: там дело не в шрифте. reportlab не делает ни переупорядочения строки
справа налево, ни соединения арабских форм, ни перестановки знаков
деванагари - он кладёт кодпойнты подряд. Текст получается нечитаемым, и
выглядит это правдоподобно ровно настолько, чтобы не заметить сразу.

Использование:
    python _tools/preflight_lang.py ka
    python _tools/preflight_lang.py ar --font _tools/fonts/NotoNaskhArabic.ttf

Что делает:
  1. Говорит, годится ли reportlab для этой письменности вообще.
  2. Проверяет покрытие шрифта по cmap - по ЗНАКАМ, которые реально стоят в
     корпусе, а не по обещанию имени файла.
  3. Ловит вариативный шрифт до того, как reportlab упадёт на нём.
  4. Собирает пробную страницу PDF и говорит, куда её положил.
"""
import os, sys, io

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(REPO, '_tools', 'fonts')
OUT = os.path.join(REPO, '_tools', 'preflight')

# Знаки, которые обязаны быть в шрифте у ЛЮБОГО языка корпуса. Список не
# теоретический: каждый из них стоит в Манифесте, и каждый выпадал бы в
# пустой квадрат молча.
COMMON = (
    'Earthlings earthling earth-lings.org 2026 0123456789 '
    '.,:;!?()[]{}"\'-/@%№ '
    + chr(0x00AB) + chr(0x00BB)          # ёлочки
)

# Письменности. Третье поле - годится ли reportlab: письменности, требующие
# перестановки и соединения знаков, он не отрисовывает.
SCRIPTS = {
    'en': ('латиница', (0x0020, 0x024F), True, 'Earthlings'),
    'de': ('латиница', (0x0020, 0x024F), True,
           'Das Volk der Earthlings ' + chr(0x201E) + 'Charta' + chr(0x201C)),
    'es': ('латиница', (0x0020, 0x024F), True,
           'El pueblo Earthlings ' + chr(0x00BF) + 'qui' + chr(0x00E9) + 'n?'),
    'fr': ('латиница', (0x0020, 0x024F), True,
           'Le peuple des Earthlings, la Charte'),
    'ka': ('мхедрули', (0x10D0, 0x10FA), True,
           'Earthlings-' + chr(0x10D8) + chr(0x10E1) + ' '
           + chr(0x10EE) + chr(0x10D0) + chr(0x10DA) + chr(0x10EE) + chr(0x10D8)),
    'zh': ('китайская', (0x4E00, 0x9FFF), True, 'Earthlings ' + chr(0x4EBA)),
    'ar': ('арабская', (0x0600, 0x06FF), False,
           'Earthlings ' + chr(0x0634) + chr(0x0639) + chr(0x0628)),
    'hi': ('деванагари', (0x0900, 0x097F), False,
           'Earthlings ' + chr(0x0932) + chr(0x094B) + chr(0x0917)),
}

WHY_NOT = {
    'ar': 'арабское письмо соединяет буквы и идёт справа налево. reportlab не '
          'делает ни того, ни другого: буквы лягут в изолированных формах '
          'слева направо. Нужен движок с шейпингом - HarfBuzz через '
          'uharfbuzz, либо сборка PDF через HTML (WeasyPrint, Playwright).',
    'hi': 'деванагари переставляет знаки при отрисовке: краткое «и» пишется '
          'ПЕРЕД согласной, к которой относится, а лигатуры сливают согласные. '
          'reportlab кладёт кодпойнты подряд, и слово выходит другим. Нужен '
          'шейпинг - см. арабский.',
}


def cmap_of(path):
    """Множество кодпойнтов шрифта плюс признак вариативности."""
    from fontTools.ttLib import TTFont
    f = TTFont(path, lazy=True)
    cps = set()
    for t in f['cmap'].tables:
        cps |= set(t.cmap.keys())
    variable = 'fvar' in f
    f.close()
    return cps, variable


def report_font(path, need):
    name = os.path.basename(path)
    try:
        cps, variable = cmap_of(path)
    except Exception as e:            # noqa: BLE001 - причина важнее типа
        print('  %-34s НЕ ЧИТАЕТСЯ: %s' % (name, e))
        return False
    missing = sorted(c for c in need if c not in cps)
    latin = sum(1 for c in list(range(0x41, 0x5B)) + list(range(0x61, 0x7B))
                if c in cps)
    print('  %-34s знаков %5d  латиницы %2d/52%s'
          % (name, len(cps), latin, '  ВАРИАТИВНЫЙ' if variable else ''))
    if variable:
        print('        reportlab вариативные шрифты не открывает. Запечь '
              'статику: fontTools.varLib.instancer, wght=400 и wght=700.')
    if missing:
        show = ''.join(chr(c) for c in missing[:40])
        print('        НЕ ХВАТАЕТ %d знаков: %s' % (len(missing), show))
        print('        Это и есть пустые квадраты в PDF. Молча.')
    return not missing and not variable


def try_pdf(lang, path, sample):
    """Собрать пробную страницу и вернуть путь либо None."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont as RLFont
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    out = os.path.join(OUT, 'preflight-%s.pdf' % lang)
    face = 'Preflight-%s' % lang
    pdfmetrics.registerFont(RLFont(face, path))
    c = canvas.Canvas(out, pagesize=A4)
    c.setFont(face, 16)
    y = A4[1] - 60
    for line in (sample, COMMON[:60], COMMON[60:]):
        c.drawString(50, y, line)
        y -= 34
    c.showPage()
    c.save()
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    assert args, 'укажи язык: python _tools/preflight_lang.py ka'
    lang = args[0]
    assert lang in SCRIPTS, 'неизвестный язык: %s (знаю %s)' % (
        lang, ', '.join(sorted(SCRIPTS)))
    title, (lo, hi), rl_ok, sample = SCRIPTS[lang]

    print('ПРЕДПОЛЁТ %s - %s, U+%04X..U+%04X' % (lang, title, lo, hi))
    print()

    print('1. ДВИЖОК PDF')
    if rl_ok:
        print('   reportlab годится: письменность не требует перестановки и '
              'соединения знаков.')
    else:
        print('   reportlab НЕ ГОДИТСЯ.')
        for line in WHY_NOT[lang].split('. '):
            if line.strip():
                print('   %s' % line.strip().rstrip('.') + '.')
        print('   Решать это ДО перевода, а не после: от выбора движка '
              'зависит, как собирается Манифест и все страницы.')

    # Проверяем покрытие по знакам, которые реально встретятся: общий набор
    # плюс образец языка. Полный диапазон письменности не требуем - в нём
    # есть архаика, которой в корпусе нет и не будет.
    need = set(ord(ch) for ch in COMMON + sample if ch != ' ')
    print()
    print('2. ШРИФТЫ В %s' % os.path.relpath(FONTS, REPO))
    ok = []
    if os.path.isdir(FONTS):
        for f in sorted(os.listdir(FONTS)):
            if f.lower().endswith(('.ttf', '.otf')):
                if report_font(os.path.join(FONTS, f), need):
                    ok.append(os.path.join(FONTS, f))
    if '--font' in sys.argv:
        extra = sys.argv[sys.argv.index('--font') + 1]
        if report_font(extra, need):
            ok.append(extra)
    if not ok:
        print()
        print('   ГОДНОГО ШРИФТА НЕТ. Пока он не появится, PDF не собирать.')
        print('   Проверять покрытие ПО CMAP, а не по имени файла: статика')
        print('   Noto с notofonts.github.io регулярно идёт без латиницы.')
        return

    print()
    print('3. ПРОБНАЯ СТРАНИЦА')
    if not rl_ok:
        print('   пропущена: движок для этой письменности другой.')
        return
    try:
        out = try_pdf(lang, ok[0], sample)
    except Exception as e:            # noqa: BLE001
        print('   НЕ СОБРАЛАСЬ: %s' % e)
        return
    print('   собрана: %s' % os.path.relpath(out, REPO))
    print('   ОТКРЫТЬ ГЛАЗАМИ. Проверка по cmap говорит, что знак в шрифте')
    print('   есть, но не говорит, что он отрисован правильно.')


if __name__ == '__main__':
    main()
