# -*- coding: utf-8 -*-
u"""Сверяет дерево меню нового сайта (chrome.SECTIONS) с деревом боевого
(NAVIGATION_DATA в js/modern/shared/constants.js).

Пока живут оба сайта, дерево меню существует в двух местах. Ровно так 17
августа 2026 разъехался список языков документа: сборщик знал про немецкий,
меню нет, и немецкий читатель не мог дойти до документов 17, 20 и 32, хотя все
три страницы отдавали 200. Двум источникам нельзя верить на слово - их надо
сверять машиной.

СВЕРКА ВЫКЛЮЧЕНА 2026-08-25. Боевое дерево заморожено решением Артура: оно
заменяется новым сайтом и больше не правится ничем. Значит расхождение меню
перестало быть дефектом и стало ожидаемым - меню нового сайта развивается,
а боевое остаётся таким, каким его застали. Первым же таким расхождением
стали правки того дня: «Гражданский голос» в правовой базе, SBT-паспорт в
устройстве, «Частые вопросы» в подвале.

Скрипт не удалён и продолжает печатать обе стороны: в день подмены полезно
видеть, что именно было в боевом меню. Но код возврата теперь всегда 0, и в
предкоммитном прогоне ему делать нечего.

Включить сверку обратно - `EARTHLINGS_NAV_SYNC=1`. Понадобится, только если
решение о заморозке отменят.

Запуск:  python earthlings-documents/_tools/check_nav_sync.py
Выход:   0 всегда, если не задан EARTHLINGS_NAV_SYNC=1.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import chrome as C   # noqa: E402

CONSTANTS = os.path.join(C.SITE, 'js', 'modern', 'shared', 'constants.js')

TOKEN = re.compile(r'(title|key|doc):"([^"]+)"')


def parse_constants(path):
    u"""Достаёт из минифицированного constants.js порядок пунктов меню.

    Возвращает тот же вид, что chrome.SECTIONS: [(ключ, номер|None, [(ключ,
    номер), ...]), ...]. Разбор идёт по порядку лексем: `title:` начинает
    раздел, `doc:` сразу за ним - это раздел-документ, `key:` открывает пункт,
    а следующий за ним `doc:` его закрывает.
    """
    src = io.open(path, encoding='utf-8').read()
    i = src.index('NAVIGATION_DATA=')
    j = src.index('export const LANGUAGES', i)
    body = src[i:j]
    assert body.count('title:') >= 3, u'в NAVIGATION_DATA подозрительно мало разделов'

    out, cur, pending = [], None, None
    for kind, val in TOKEN.findall(body):
        if kind == 'title':
            if cur:
                out.append(cur)
            cur = [val, None, []]
            pending = None
        elif kind == 'key':
            pending = val
        elif kind == 'doc':
            assert cur, u'номер документа встретился раньше первого раздела'
            if pending:
                cur[2].append((pending, val))
                pending = None
            else:
                cur[1] = val
    if cur:
        out.append(cur)
    return [(a, b, c) for a, b, c in out]


def main():
    assert os.path.isfile(CONSTANTS), u'нет файла %s' % CONSTANTS
    old = parse_constants(CONSTANTS)
    new = [(k, n, list(items)) for k, n, items in C.SECTIONS]
    assert new, u'chrome.SECTIONS пуст - сверять нечего'

    lines, bad = [], 0
    lines.append(u'разделов: constants.js %d, chrome.py %d' % (len(old), len(new)))
    if len(old) != len(new):
        bad += 1
        lines.append(u'  ПРОВАЛ: разное число разделов')
        lines.append(u'  constants.js: %s' % ', '.join(k for k, _, _ in old))
        lines.append(u'  chrome.py:    %s' % ', '.join(k for k, _, _ in new))

    for a, b in zip(old, new):
        if a[0] != b[0]:
            bad += 1
            lines.append(u'ПРОВАЛ: раздел %r против %r' % (a[0], b[0]))
            continue
        if a[1] != b[1]:
            bad += 1
            lines.append(u'ПРОВАЛ: %s - документ раздела %r против %r'
                         % (a[0], a[1], b[1]))
        if a[2] != b[2]:
            bad += 1
            lines.append(u'ПРОВАЛ: %s - состав пунктов разошёлся' % a[0])
            lines.append(u'  constants.js: %s'
                         % ', '.join('%s=%s' % kv for kv in a[2]))
            lines.append(u'  chrome.py:    %s'
                         % ', '.join('%s=%s' % kv for kv in b[2]))

    # Подписи всех пунктов обязаны быть в переводах КАЖДОГО языка, на котором
    # пункт показывается. Иначе меню соберётся на чужом языке - ровно та
    # поломка, из-за которой немцу месяц показывали «Учредительный период».
    site_docs = os.path.join(C.SITE, 'documents')
    for key, num, items in C.SECTIONS:
        for k, n in ([(key, num)] if num else []) + list(items):
            for lang in C.ALL_LANGS:
                have = os.path.isdir(os.path.join(site_docs, lang))
                if not have:
                    continue
                pages = os.listdir(os.path.join(site_docs, lang))
                if not any(p.startswith('%s%s' % (lang, n)) for p in pages):
                    continue          # документа на этом языке нет - и пункта нет
                try:
                    C.t(lang, k)
                except AssertionError as e:
                    bad += 1
                    lines.append(u'ПРОВАЛ: %s' % e)

    on = os.environ.get('EARTHLINGS_NAV_SYNC') == '1'
    lines.append(u'')
    lines.append(u'расхождений: %d' % bad)
    if not on:
        lines.append(u'')
        lines.append(u'Сверка выключена 2026-08-25: боевое дерево заморожено и '
                     u'заменяется новым сайтом,')
        lines.append(u'поэтому расхождение меню ожидаемо, а не дефектно. '
                     u'Включить: EARTHLINGS_NAV_SYNC=1.')
    io.open(os.path.join(HERE, 'nav-sync-report.txt'), 'w',
            encoding='utf-8').write(u'\n'.join(lines) + u'\n')
    sys.stdout.write('nav sync: расхождений=%d%s -> %s\n'
                     % (bad, u'' if on else u' (сверка выключена, боевое дерево заморожено)',
                        os.path.join(HERE, 'nav-sync-report.txt')))
    return 1 if (bad and on) else 0


if __name__ == '__main__':
    sys.exit(main())
