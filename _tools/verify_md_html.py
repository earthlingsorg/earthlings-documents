# -*- coding: utf-8 -*-
"""Сверка: весь ли текст .md-мастера дошёл до собранной страницы.

Сравниваются последовательности слов, а не байты: разметка, пунктуация и
переносы строк роли не играют, важно только, что ни одно слово не потерялось
и ни одно не появилось из ниоткуда.

Из HTML при этом выбрасывается всё, что не является телом документа:
оглавление (оно задваивает заголовки), навигация по корпусу, скрипты, стили.

Использование:
  python verify_md_html.py 05         один документ, русский
  python verify_md_html.py all        весь корпус, русский
  python verify_md_html.py de 05      один документ на языке
  python verify_md_html.py de all     весь корпус на языке
  python verify_md_html.py all all    все документы на всех девяти языках

Языки, на которых документа нет, пропускаются молча: состав по языкам знает
сам сборщик (`has_doc`), второго списка здесь нет.
"""
import io, os, re, sys, html, difflib, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Мастера переехали 2026-08-14 из общей папки в `<репозиторий>/<язык>/`, и
# страницы получили смысловые адреса вместо числовых. Прежние `CORPUS`, `MD_DIR`
# и `DOCS` были русскими константами и исчезли вместе с переездом - проверка
# падала на импорте, то есть молча не работала. Теперь путь считается теми же
# функциями, которыми его считает сборщик: расходиться нечему.
import build_site_docs
from build_site_docs import (ALL_LANGS, CHAIN, SLUGS, corpus_file, doc_file,
                             docs_dir, has_doc, load_fragments, md_dir)

# Сверяем с деревом НОВОГО сайта, а не боевого. Боевой заменяется и с
# 2026-08-25 не пересобирается (решение Артура), поэтому его страницы будут
# отставать от мастеров всё сильнее, и проверка против них показывала бы
# расхождения, которых в работе нет. `docs_dir` смотрит на этот флаг.
#
# Проверить боевое дерево при нужде: python verify_md_html.py --legacy ...
if '--legacy' in sys.argv:
    sys.argv.remove('--legacy')
else:
    build_site_docs.THEME = 'v2'

WORD = re.compile(r'[0-9A-Za-zЀ-ӿ]+', re.U)


def words(text):
    return WORD.findall(unicodedata.normalize('NFC', text).lower())


# ---------------------------------------------------------------- из .md

def md_text(path):
    out = []
    for raw in io.open(path, encoding='utf-8'):
        s = raw.strip()
        if not s or s == '---':
            continue
        if s.startswith('|') and re.fullmatch(r'\|[\s:|-]+\|?', s):
            continue                                  # разделитель таблицы
        def clean(x):
            x = x.replace('|', ' ')                   # ячейки таблицы
            return re.sub(r'\[([^\]]+)\]\([^)\s]+\)', r'\1', x)   # ссылки: только текст

        if re.fullmatch(r'\[\[BLOCK-[^\]]+\]\]', s):
            continue                                  # место вставки схемы
        if s.startswith('#'):
            # у заголовка нумерация - часть названия, её нельзя срезать
            out.append(clean(re.sub(r'^#{1,6}\s*', '', s)))
            continue
        s = re.sub(r'^>\s?', '', s)                   # цитаты
        s = re.sub(r'^[-*]\s+', '', s)                # маркеры списка
        s = re.sub(r'^\d+\.\s+', '', s)               # нумерация списка
        out.append(clean(s))
    return '\n'.join(out)


# ---------------------------------------------------------------- из .html

DROP_BLOCKS = [
    r'<head>.*?</head>',
    r'<script.*?</script>',
    r'<style.*?</style>',
    r'<nav class="toc.*?</nav>',
    r'<!--seo-prev-next-start-->.*?<!--seo-prev-next-end-->',
    r'<!--umami-start-->.*?<!--umami-end-->',
    r'<figure class="diagram".*?</figure>',   # схемы приходят не из .md, см. ниже
    # Обвязка новой темы. Правила выше писались под боевую разметку, где меню
    # и подвал рисует скрипт и в HTML их нет. В новой теме они статические -
    # и без этих трёх строк проверка объявляла расхождением каждый документ,
    # находя в странице «лишние» слова меню, названия языков и адрес почты.
    r'<a class="skip".*?</a>',
    r'<header class="hdr".*?</header>',
    r'<footer class="ftr".*?</footer>',
    r'<nav class="seo-prev-next".*?</nav>',
]


def html_text(path):
    s = io.open(path, encoding='utf-8').read()
    for pat in DROP_BLOCKS:
        s = re.sub(pat, ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)


# ---------------------------------------------------------------- отчёт

def report(num, lang='ru', limit=12):
    md_path = os.path.join(md_dir(lang), corpus_file(num, lang))
    html_path = os.path.join(docs_dir(lang), doc_file(num, lang))
    if not os.path.isfile(md_path):
        return num, None, None, ['нет .md-мастера']
    if not os.path.isfile(html_path):
        return num, None, None, ['нет собранной страницы']

    a = words(md_text(md_path))
    b = words(html_text(html_path))
    assert a, 'пустой .md: %s' % md_path
    assert b, 'пустой .html: %s' % html_path

    problems = []
    # схемы в .md не выражаются: проверяем, что каждый сохранённый фрагмент
    # попал на страницу дословно
    page = io.open(html_path, encoding='utf-8').read()
    for marker, frag in load_fragments(num, lang).items():
        if frag not in page:
            problems.append('фрагмент %s не найден на странице целиком' % marker)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        lost = ' '.join(a[i1:i2])[:150]
        got = ' '.join(b[j1:j2])[:150]
        if tag == 'delete':
            problems.append('потеряно (позиция %d): %s' % (i1, lost))
        elif tag == 'insert':
            problems.append('лишнее (позиция %d): %s' % (j1, got))
        else:
            problems.append('заменено (позиция %d): %s  ->  %s' % (i1, lost, got))
        if len(problems) >= limit:
            problems.append('... список обрезан')
            break
    return num, len(a), len(b), problems


def main():
    args = sys.argv[1:] or ['all']
    # Первый довод - язык, если он похож на язык. Без него всё как раньше:
    # русский, чтобы прежние вызовы из памяти и заметок продолжали работать.
    if args and (args[0] in ALL_LANGS or args[0] == 'all') and len(args) > 1:
        langs = ALL_LANGS if args[0] == 'all' else [args[0]]
        args = args[1:]
    else:
        langs = ['ru']
    targets = CHAIN if args == ['all'] else args

    checked = skipped = bad = 0
    for lang in langs:
        for num in targets:
            # Двойное условие, и оба нужны. `has_doc` говорит, положен ли
            # документ этому языку. Наличие слага говорит, есть ли у языка
            # мастер: имя мастера выводится из слага, и у хинди слагов нет
            # вовсе - страницы там остались от прежних заходов, под старыми
            # числовыми именами, а мастеров под ними нет. Без второго условия
            # проверка падает с KeyError, а не пропускает язык.
            if not has_doc(num, lang) or num not in SLUGS.get(lang, {}):
                skipped += 1
                continue
            checked += 1
            n, na, nb, problems = report(num, lang)
            if problems:
                bad += 1
                print('РАСХОЖДЕНИЕ  %s%s   .md %s слов / .html %s слов'
                      % (lang, n, na, nb))
                for p in problems:
                    print('    ', p)
            else:
                print('совпадает    %s%s   %d слов' % (lang, n, na))

    assert checked, ('проверять оказалось нечего - без этой проверки отчёт '
                     '«0 расхождений» получался бы на пустом множестве')
    print('\nитого: %d из %d проверенных с расхождениями'
          '  (пропущено, нет на языке: %d)' % (bad, checked, skipped))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
