# -*- coding: utf-8 -*-
u"""Типографика ЖИВОГО дерева сайта: запрещённые знаки по девяти языкам.

Зачем отдельный прибор. `earth-lings-site/tools/punct_audit.py` живое дерево не
проверяет вовсе, и это выяснилось 2026-11-02:

- он смотрит `documents/<язык>/<язык>NN.html`, то есть ЗАМОРОЖЕННОЕ дерево после
  подмены 2026-09-06, а не `_v2/`, откуда сайт отдаётся;
- его автоопределение корня ищет образец `documents/en/en01.html`, а файлы давно
  называются `en01-declaration.html`, поэтому без `--root` он просто не
  запускается;
- и он лежит в `earth-lings-site/tools/`, целиком закрытой `.gitignore`, то есть
  существует на одной машине.

Из-за этого «Replaceable total: 0» два месяца значил «на мёртвом дереве чисто».
Проверка, которая смотрит не туда, хуже отсутствующей: она выдаёт тишину за
порядок.

Что считается законным, а не дефектом. Родная норма языка сохраняется:
китайские `——` и полноширинные кавычки, немецкие и грузинские `„..."`, русские
ёлочки `«»`. Остальное - дефект, независимо от того, кто его внёс.

Запуск из C:/local_git_vps/earthlings-documents:
    PYTHONIOENCODING=utf-8 python _tools/tipografika_sajta.py
    PYTHONIOENCODING=utf-8 python _tools/tipografika_sajta.py --check
    PYTHONIOENCODING=utf-8 python _tools/tipografika_sajta.py --files

`--check` возвращает 1 на любом дефекте. Умолчание - запрет: проверка, которая
не останавливает действие, не проверка.
"""
import io
import os
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
# Репозиторий сайта - соседняя папка, как у build_site_docs.py. Захардкоженный
# путь одной машины в публичном репозитории ломает скрипт у всех остальных.
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
# 🚨 Смотрим ЖИВОЕ дерево. `topics/` и `documents/` в корне сайта - копии для
# откатa после подмены 2026-09-06, править их нельзя, и мерить их типографику
# смысла нет.
LIVE = os.path.join(SITE, '_v2')
assert os.path.isdir(LIVE), (
    u'не найдено живое дерево сайта: %s\n'
    u'Ожидается earth-lings-site рядом с этим репозиторием. Если он лежит в '
    u'другом месте - EARTHLINGS_SITE=/путь/к/earth-lings-site' % LIVE)

LANGS = ('ru', 'en', 'es', 'de', 'fr', 'zh', 'ar', 'hi', 'ka')

# Словарь строим из ЧИСЛОВЫХ кодпойнтов: литералы в этом файле молча портятся
# при передаче через heredoc, и проверка «проходит» на сломанном словаре.
FORBIDDEN = {
    0x2014: u'em-dash', 0x2013: u'en-dash', 0x2212: u'minus',
    0x2026: u'ellipsis', 0x201c: u'ldquo', 0x201d: u'rdquo',
    0x201e: u'bdquo', 0x2018: u'lsquo', 0x2019: u'rsquo',
    0x00a0: u'nbsp', 0x202f: u'nnbsp', 0x200b: u'zwsp',
    0x2060: u'wj', 0xfeff: u'bom',
}
assert len(FORBIDDEN) == 14, u'словарь урезан'

# Родная норма языка. Сохраняется, а не вычитается молча.
NATIVE = {
    'zh': (0x2014, 0x201c, 0x201d),   # —— и полноширинные кавычки
    'de': (0x201e, 0x201c),           # „..."
    'ka': (0x201e, 0x201c),
}

# Отрицательный контроль прибора: обязан поймать подсунутое...
assert any(chr(cp) in u'x' + chr(0x2014) for cp in FORBIDDEN), u'контроль не сработал'
# ...и НЕ считать дефектом русские ёлочки и родные буквы.
assert not [cp for cp in FORBIDDEN
            if chr(cp) in u'\u00ab\u00bb\u00e9\u00e0\u0259'], u'ложная тревога'


def lang_of(path):
    u"""🚨 Папка проверяется ПЕРЕД именем файла.

    Обратный порядок давал `_v2/zh/index.html` язык `en`, и 18 китайских `——`
    на китайской главной докладывались как дефект. Правило «index.html - это
    английский» верно только в корне сайта, а не внутри языковой папки.
    """
    parts = path.replace(os.sep, u'/').split(u'/')
    for p in parts[:-1]:
        if p in LANGS:
            return p
    name = os.path.splitext(parts[-1])[0]
    if name in LANGS:
        return name
    if name == 'index':
        return 'en'
    return '?'


# Отрицательный контроль определения языка.
assert lang_of(u'x/_v2/zh/index.html') == 'zh'
assert lang_of(u'x/_v2/topics/belonging-by-choice/de.html') == 'de'
assert lang_of(u'x/_v2/index.html') == 'en'
assert lang_of(u'x/_v2/css/tokens.css') == '?'


def section_of(path):
    rel = os.path.relpath(path, LIVE).replace(os.sep, u'/')
    return rel.split(u'/')[0] if u'/' in rel else u'(корень)'


def pages():
    out = []
    for root, _, names in os.walk(LIVE):
        for n in sorted(names):
            if n.endswith('.html'):
                out.append(os.path.join(root, n))
    return sorted(out)


def main(argv):
    check = '--check' in argv
    by_files = '--files' in argv

    files = pages()
    assert files, u'пустой ввод: ни одной страницы в %s' % LIVE

    bad_sign = Counter()
    bad_section = Counter()
    bad_files = Counter()
    native = Counter()
    sample = {}
    for path in files:
        text = io.open(path, encoding='utf-8').read()
        lang = lang_of(path)
        own = 0
        for cp, name in FORBIDDEN.items():
            n = text.count(chr(cp))
            if not n:
                continue
            if cp in NATIVE.get(lang, ()):
                native[u'%s %s' % (lang, name)] += n
                continue
            bad_sign[name] += n
            own += n
            sample.setdefault(name, os.path.relpath(path, SITE))
        if own:
            bad_section[section_of(path)] += own
            bad_files[os.path.relpath(path, SITE)] = own

    out = sys.stdout
    out.write(u'живое дерево: %s\n' % os.path.relpath(LIVE, SITE))
    out.write(u'прочитано страниц: %d\n\n' % len(files))

    if bad_sign:
        out.write(u'ЗАПРЕЩЁННОЕ по разделам сайта (знаков / файлов):\n')
        for s, n in bad_section.most_common():
            cnt = len([f for f in bad_files if section_of(os.path.join(SITE, f)) == s])
            out.write(u'   %-16s %5d / %3d\n' % (s, n, cnt))
        out.write(u'\nпо знакам:\n')
        for name, n in bad_sign.most_common():
            out.write(u'   %-10s %5d   напр. %s\n' % (name, n, sample[name]))
        if by_files:
            out.write(u'\nпо файлам:\n')
            for f, n in bad_files.most_common():
                out.write(u'   %-58s %d\n' % (f, n))
    else:
        out.write(u'ЗАПРЕЩЁННОГО НЕТ ни на одной странице\n')

    out.write(u'\nРОДНАЯ НОРМА, не дефект:\n')
    for k, n in native.most_common():
        out.write(u'   %-18s %d\n' % (k, n))

    out.write(u'\nВСЕГО ЗАПРЕЩЁННЫХ: %d\n' % sum(bad_sign.values()))

    if not check:
        return 0
    if bad_sign:
        out.write(u'\nПРОВЕРКА НЕ ПРОШЛА: %d знаков в %d файлах\n'
                  % (sum(bad_sign.values()), len(bad_files)))
        return 1
    out.write(u'\nПРОВЕРКА ПРОШЛА\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
