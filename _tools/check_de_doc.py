# -*- coding: utf-8 -*-
"""Приёмка одного немецкого документа за один вызов.

Собирает в один компактный отчёт то, что раньше запускалось тремя командами
и читалось тремя чтениями: структуру против русского мастера, поштучную
сверку чисел с русским и английским, дельту машинного аудита по этому файлу.

Отчёт пишется в _tools/_doc-report.txt в UTF-8 и НЕ печатается в консоль:
русская консоль Windows работает в cp866, умлауты в неё не кодируются, и
процесс умирает посреди отчёта. Это уже случалось.

Использование: python _tools/check_de_doc.py 05
"""
import io, os, re, sys, collections, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert os.path.isdir(os.path.join(REPO, 'ru')), REPO

NUM = sys.argv[1] if len(sys.argv) > 1 else None
assert NUM and re.match(r'^\d\d$', NUM), 'укажите номер документа двумя цифрами'

OUT = os.path.join(REPO, '_tools', '_doc-report.txt')
DE_OPEN, DE_CLOSE, ASCII_Q = chr(0x201E), chr(0x201C), chr(0x22)


def find(lang):
    d = os.path.join(REPO, lang)
    for f in sorted(os.listdir(d)):
        if f.startswith(NUM + '-') and f.endswith('.md'):
            return os.path.join(d, f)
    return None


def read(p):
    return io.open(p, encoding='utf-8').read() if p else ''


def main():
    rp, ep, dp = find('ru'), find('en'), find('de')
    assert rp, 'нет русского мастера %s' % NUM
    assert dp, 'нет немецкого перевода %s' % NUM
    ru, en, de = read(rp), read(ep), read(dp)
    assert ru.strip() and de.strip(), 'пустой файл на входе'

    o = ['=== ДОКУМЕНТ %s: %s ===' % (NUM, os.path.basename(dp)), '']

    # 1. Структура - вызываем существующий скрипт, чтобы не заводить второй
    #    источник истины о том, что такое блок.
    r = subprocess.run([sys.executable,
                        os.path.join(REPO, '_tools', 'check_translation.py'),
                        NUM, 'de'],
                       capture_output=True, cwd=REPO)
    o.append('1. СТРУКТУРА: %s' % ('ок' if r.returncode == 0 else 'РАСХОЖДЕНИЕ'))
    if r.returncode != 0:
        o.append(r.stdout.decode('utf-8', 'replace'))

    # 2. Числа. Русский - источник истины, английский печатается третьим
    #    столбцом как контролёр. Числа, записанные в русском словами, должны
    #    быть словами и в немецком - иначе расхождение на пустом месте.
    def nums(s):
        return collections.Counter(re.findall(r'\d+', s))
    a, b, c = nums(ru), nums(en), nums(de)
    bad = [k for k in sorted(set(a) | set(c)) if a[k] != c[k]]
    o.append('2. ЧИСЛА: различных в ru %d, расхождений ru/de %d' % (len(a), len(bad)))
    for k in bad:
        o.append('     %-8s ru=%d en=%d de=%d' % (k, a[k], b[k], c[k]))

    # 3. Типографика этого файла отдельно: общий аудит считает по корпусу,
    #    и файл с непарной кавычкой в нём теряется среди прочих.
    op, cl, asc = de.count(DE_OPEN), de.count(DE_CLOSE), de.count(ASCII_Q)
    o.append('3. КАВЫЧКИ: открывающих %d, закрывающих %d, ASCII %d%s'
             % (op, cl, asc, '' if op == cl and asc == 0 else '   <-- РАЗБИРАТЬ'))

    # 4. Жирные и структурные счётчики - дельта к русскому, а не абсолют.
    for label, pat in [('жирных **', r'\*\*'), ('пунктов списка', r'^\d+\. '),
                       ('маркеров -', r'^- '), ('таблиц |', r'^\|')]:
        na = len(re.findall(pat, ru, re.M))
        nc = len(re.findall(pat, de, re.M))
        if na != nc:
            o.append('4. %s: ru %d  de %d   <-- РАСХОЖДЕНИЕ' % (label, na, nc))
    o.append('4. счётчики разметки сверены с русским')

    # 5. Дельта аудита: только строки, где упомянут этот файл.
    r2 = subprocess.run([sys.executable, os.path.join(REPO, '_tools', 'audit_de.py')],
                        capture_output=True, cwd=REPO)
    rep = read(os.path.join(REPO, '_tools', 'audit-report-de.txt'))
    mine = [l for l in rep.split('\n') if os.path.basename(dp)[:24] in l]
    o.append('5. АУДИТ, строки про этот файл: %d' % len(mine))
    o.extend('     ' + l.strip() for l in mine)

    # 6. Разделы аудита, которые считаются по всему корпусу и потому
    #    печатаются целиком: расползание терминов и жёсткие замки.
    for head, nxt in [('=== 3.', '=== 4.'), ('=== 10.', '=== 11.')]:
        if head in rep and nxt in rep:
            o.append('')
            o.append(rep[rep.index(head):rep.index(nxt)].rstrip())

    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(o))
    print('report written')


if __name__ == '__main__':
    main()
