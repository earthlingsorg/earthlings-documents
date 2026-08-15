# -*- coding: utf-8 -*-
"""Сверка: весь ли текст .md-мастера дошёл до собранной страницы.

Сравниваются последовательности слов, а не байты: разметка, пунктуация и
переносы строк роли не играют, важно только, что ни одно слово не потерялось
и ни одно не появилось из ниоткуда.

Из HTML при этом выбрасывается всё, что не является телом документа:
оглавление (оно задваивает заголовки), навигация по корпусу, скрипты, стили.

Использование:
  python verify_md_html.py 05         один документ
  python verify_md_html.py all        весь корпус
"""
import io, os, re, sys, html, difflib, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site_docs import CORPUS, CHAIN, MD_DIR, DOCS, load_fragments

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
]


def html_text(path):
    s = io.open(path, encoding='utf-8').read()
    for pat in DROP_BLOCKS:
        s = re.sub(pat, ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)


# ---------------------------------------------------------------- отчёт

def report(num, limit=12):
    md_path = os.path.join(MD_DIR, CORPUS[num])
    html_path = os.path.join(DOCS, 'ru%s.html' % num)
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
    for marker, frag in load_fragments(num).items():
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
    targets = CHAIN if args == ['all'] else args
    bad = 0
    for num in targets:
        n, na, nb, problems = report(num)
        if problems:
            bad += 1
            print('РАСХОЖДЕНИЕ  ru%s   .md %s слов / .html %s слов' % (n, na, nb))
            for p in problems:
                print('    ', p)
        else:
            print('совпадает    ru%s   %d слов' % (n, na))
    print('\nитого: %d из %d документов с расхождениями' % (bad, len(targets)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
