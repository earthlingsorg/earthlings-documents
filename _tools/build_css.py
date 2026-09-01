# -*- coding: utf-8 -*-
u"""Стили: исходник с объяснениями - разработчику, выдача без них - читателю.

Зачем. Замер по живому дереву: комментарии составляют 80% веса стилей после
сжатия.

    лист            с комментариями   без них
    tokens.css            8 635         1 321
    chrome.css            8 169         2 129
    home.css             17 277         3 252
    ---------------------------------------------
    языковая главная     35 668         7 081
    страница документа   20 041         4 603

Впятеро. И это на КАЖДОЙ странице сайта, а не только на главных.

Комментарии в этих файлах ценные: в них записано, почему меню собрано на
<details>, откуда взяты величины epic.org, какой замер стоит за весом 500 у
заголовка. Выбрасывать их нельзя. Но и возить их читателю незачем - он их
не прочтёт.

Отсюда разделение, которое в этом проекте уже действует для документов:
исходник живёт в репозитории сборки, выдача порождается. `_v2/documents/`
порождается из мастеров корпуса; теперь `_v2/css/` порождается отсюда.

Почему НЕ минификатор. Полноценный минификатор переписывает селекторы,
сливает правила и меняет порядок - и ошибается редко, но молча. Здесь
снимаются только комментарии и лишние пустые строки: это даёт 80% выигрыша
и не может изменить смысл ни одного правила. Ни одной внешней зависимости,
ни одного шага npx в выкатке.

Схема выкатки не меняется: сервер как отдавал дерево репозитория, так и
отдаёт. Порождённые листы лежат в нём рядом со страницами.

Запуск:
    python _tools/build_css.py            собрать
    python _tools/build_css.py --check    сверить, не собирая (для приёмки)
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import site_guard as guard                       # noqa: E402
from build_site_docs import SITE                 # noqa: E402

SRC = os.path.join(HERE, 'css')
OUT = os.path.join(SITE, '_v2', 'css')

# Шапка выдачи. Нужна затем, чтобы человек, открывший файл в браузере или в
# отладчике, не начал править его и не потерял правку при следующей сборке.
BANNER = (u'/* Порождено _tools/build_css.py из _tools/css/%s.\n'
          u'   Правьте ИСХОДНИК: здесь правка живёт до следующей сборки.\n'
          u'   Комментарии сняты намеренно - они составляют 80%% веса. */\n')


def strip(css):
    u"""Снимает комментарии и лишние пустые строки. Больше ничего.

    Кавычки уважаются: `content: "/* не комментарий */"` в наших листах не
    встречается, но правило, которое сломается на нём молча, - плохое
    правило. Разбор идёт посимвольно, а не регуляркой по всему файлу.
    """
    out = []
    i, n = 0, len(css)
    quote = None
    while i < n:
        c = css[i]
        if quote:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(css[i + 1]); i += 2; continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in '"\'':
            quote = c; out.append(c); i += 1; continue
        if c == '/' and i + 1 < n and css[i + 1] == '*':
            j = css.find('*/', i + 2)
            i = n if j < 0 else j + 2
            continue
        out.append(c); i += 1
    s = ''.join(out)
    # Хвостовые пробелы, отступы и пустые строки, оставшиеся от комментариев.
    s = re.sub(r'[ \t]+\n', '\n', s)
    s = re.sub(r'\n{2,}', '\n', s)
    return s.strip() + '\n'


def sources():
    files = sorted(glob.glob(os.path.join(SRC, '*.css')))
    assert files, u'исходников стилей не найдено: %s' % SRC
    return files


def build(check=False):
    guard.makedirs(OUT)
    stale, total_src, total_out = [], 0, 0
    for p in sources():
        name = os.path.basename(p)
        src = io.open(p, encoding='utf-8').read()
        assert src.strip(), u'пустой исходник: %s' % p
        want = BANNER % name + strip(src)
        dst = os.path.join(OUT, name)
        have = io.open(dst, encoding='utf-8').read() if os.path.isfile(dst) else None
        total_src += len(src.encode('utf-8'))
        total_out += len(want.encode('utf-8'))
        if have != want:
            stale.append(name)
            if not check:
                guard.write(dst, want)
    # Лист, оставшийся в выдаче без исходника, - тоже расхождение: он
    # отдаётся читателю, а починить его негде.
    names = {os.path.basename(p) for p in sources()}
    orphan = sorted(os.path.basename(p) for p in glob.glob(os.path.join(OUT, '*.css'))
                    if os.path.basename(p) not in names)
    return stale, orphan, total_src, total_out


def main():
    check = '--check' in sys.argv
    stale, orphan, a, b = build(check)
    print(u'листов %d, исходник %d КБ, выдача %d КБ (-%.0f%%)'
          % (len(sources()), a // 1024, b // 1024, 100.0 * (a - b) / a))
    if orphan:
        print(u'В ВЫДАЧЕ БЕЗ ИСХОДНИКА: %s' % ', '.join(orphan))
    if check:
        if stale:
            print(u'УСТАРЕЛО: %s' % ', '.join(stale))
        else:
            print(u'выдача соответствует исходникам')
        return len(stale) + len(orphan)
    print(u'пересобрано: %s' % (', '.join(stale) if stale else u'ничего, всё свежее'))
    return len(orphan)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
