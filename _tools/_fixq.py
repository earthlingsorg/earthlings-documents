# -*- coding: utf-8 -*-
"""Замена прямых ASCII-кавычек на немецкую закрывающую в готовом мастере.

Немецкие документы набираются так: открывающая U+201E ставится сразу, а
закрывающая - прямым ASCII, потому что U+201C визуально неотличима от
открывающей и её легко перепутать при наборе. Этот скрипт переводит вторую
в правильный знак и проверяет пару.

Все знаки собираются из КОДПОЙНТОВ: литералы молча портятся при передаче
через heredoc и буфер обмена - на этом уже споткнулись.

Использование: python _tools/_fixq.py de/03-ethik.md [ещё файлы]
"""
import io, os, sys

OPEN, CLOSE, ASCII_Q = chr(0x201E), chr(0x201C), chr(0x22)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

assert len(sys.argv) > 1, 'укажите файлы'
for rel in sys.argv[1:]:
    p = os.path.join(REPO, rel)
    assert os.path.isfile(p), p
    s = io.open(p, encoding='utf-8').read()
    assert s.strip(), 'пустой файл: %s' % rel
    no, nc, na = s.count(OPEN), s.count(CLOSE), s.count(ASCII_Q)
    if na == 0 and no == nc:
        print('%-42s уже в порядке: %d пар' % (rel, no))
        continue
    assert nc == 0, '%s: уже есть %d закрывающих, разбирать руками' % (rel, nc)
    assert na == no, '%s: ASCII %d, открывающих %d - не пара' % (rel, na, no)
    s2 = s.replace(ASCII_Q, CLOSE)
    assert s2.count(OPEN) == s2.count(CLOSE) == no and ASCII_Q not in s2
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s2)
    print('%-42s %d пар' % (rel, no))
