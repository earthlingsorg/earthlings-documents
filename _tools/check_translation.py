# -*- coding: utf-8 -*-
"""Структурная сверка перевода с русским мастером.

Перевод обязан быть зеркалом мастера по разбивке на блоки: заголовки, врезки,
списки и таблицы стоят на тех же местах. Иначе сборщик соберёт два разных
документа, а сверка на глаз пропустит выпавший абзац - их в корпусе тысячи.

Использование:
  python check_translation.py 04 en
  python check_translation.py --all en
"""
import io, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert os.path.isdir(os.path.join(REPO, 'ru')), REPO

# Словарь строим из КОДПОЙНТОВ: литералы в этом файле молча портятся
# при передаче через heredoc и проверка «проходит» на сломанном словаре.
FORBIDDEN = {
    0x2014: 'em-dash', 0x2013: 'en-dash', 0x2212: 'minus', 0x2026: 'ellipsis',
    0x201C: 'ldquo', 0x201D: 'rdquo', 0x201E: 'bdquo', 0x201F: 'quote',
    0x2018: 'lsquo', 0x2019: 'rsquo', 0x201A: 'sbquo', 0x201B: 'quote',
    0x2039: 'lsaquo', 0x203A: 'rsaquo',
    0x00A0: 'nbsp', 0x202F: 'narrow-nbsp', 0x2009: 'thin-space',
    0x2007: 'figure-space', 0x2008: 'punct-space', 0x200A: 'hair-space',
    0x200B: 'zwsp', 0x200C: 'zwnj', 0x2060: 'word-joiner', 0xFEFF: 'bom',
}


def kind(b):
    if b.startswith('# '):
        return 'h1'
    if b.startswith('## '):
        return 'h2'
    if b.startswith('### '):
        return 'h3'
    if b.startswith('>'):
        return 'quote'
    if re.match(r'^[-*] |^\d+\. ', b):
        return 'list'
    if b.startswith('|'):
        return 'table'
    if re.match(r'^-{3,}$', b):
        return 'hr'
    return 'p'


def blocks(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.strip(), 'пустой файл: %s' % path
    return [b.strip() for b in re.split(r'\n\s*\n', s) if b.strip()], s


def find(lang, num):
    d = os.path.join(REPO, lang)
    for f in sorted(os.listdir(d)):
        if f.startswith(num + '-') and f.endswith('.md'):
            return os.path.join(d, f)
    return None


def check(num, lang):
    rp, tp = find('ru', num), find(lang, num)
    if not rp:
        print('%s: нет русского мастера' % num)
        return False
    if not tp:
        print('%s: нет перевода в %s/' % (num, lang))
        return False
    ru, rs = blocks(rp)
    tr, ts = blocks(tp)

    ok = True
    head = '%s %s' % (num, os.path.basename(tp))
    if len(ru) != len(tr):
        print('%s  БЛОКИ: ru %d  %s %d' % (head, len(ru), lang, len(tr)))
        ok = False
        # показываем первое расхождение - дальше сравнивать бессмысленно
        for i in range(min(len(ru), len(tr))):
            if kind(ru[i]) != kind(tr[i]):
                print('   первое расхождение на блоке %d: ru=%s %s' % (
                    i, kind(ru[i]), ru[i][:70].replace('\n', ' ')))
                break
    else:
        bad = [i for i in range(len(ru)) if kind(ru[i]) != kind(tr[i])]
        if bad:
            ok = False
            print('%s  ТИПЫ БЛОКОВ: %d расхождений' % (head, len(bad)))
            for i in bad[:5]:
                print('   #%d ru=%s %s=%s | %s' % (
                    i, kind(ru[i]), lang, kind(tr[i]), ru[i][:60].replace('\n', ' ')))

    if rs.count('**') != ts.count('**'):
        ok = False
        print('%s  ЖИРНЫЕ: ru %d  %s %d' % (head, rs.count('**'), lang, ts.count('**')))

    hits = {}
    for ch in ts:
        o = ord(ch)
        if o in FORBIDDEN:
            hits[FORBIDDEN[o]] = hits.get(FORBIDDEN[o], 0) + 1
    if hits:
        ok = False
        print('%s  ТИПОГРАФИКА: %s' % (head, hits))

    if ok:
        print('%s  ок: %d блоков, слов ru %d  %s %d' % (
            head, len(ru), len(rs.split()), lang, len(ts.split())))
    return ok


def main():
    args = [a for a in sys.argv[1:]]
    lang = args[-1] if args and len(args[-1]) == 2 else 'en'
    if '--all' in args:
        nums = sorted(f[:2] for f in os.listdir(os.path.join(REPO, 'ru'))
                      if re.match(r'^\d\d-', f))
    else:
        nums = [a for a in args if re.match(r'^\d\d$', a)]
    assert nums, 'нечего проверять: укажите номера или --all'
    bad = [n for n in nums if not check(n, lang)]
    print('---')
    print('проверено %d, с расхождениями %d' % (len(nums), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
