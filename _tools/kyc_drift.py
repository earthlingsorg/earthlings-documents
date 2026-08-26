# -*- coding: utf-8 -*-
u"""Дрейф копий корпуса внутри earthlings-kyc: измеряет, а не чинит.

`earthlings-kyc` держит копии части документов в девяти языках
(`app/public/documents/<язык>/`) и синхронизируется ВРУЧНУЮ: ни один скрипт на
KYC не ссылается. Копия документа 20 уже отставала, и нашли это случайно.

Почему измеритель, а не скрипт синка. KYC - работающая система с оплатой и
выпуском паспортов. Автоматический перенос текста туда означал бы, что правка
корпуса меняет живую страницу регистрации без чьего-либо взгляда. Дрейф
надо ВИДЕТЬ; закрывать его - отдельное решение каждый раз.

Сравнивается не разметка, а слова: копии собраны прежней темой, у них другая
обвязка, и сравнивать HTML целиком бессмысленно.

Запуск:  python _tools/kyc_drift.py
Код возврата - число разошедшихся документов.
"""
import io
import os
import re
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
KYC = os.environ.get('EARTHLINGS_KYC') or os.path.join(
    os.path.dirname(REPO), 'earthlings-kyc')

sys.path.insert(0, TOOLS)
import build_site_docs as B                       # noqa: E402


# Классы письма строятся из ЧИСЛОВЫХ кодпойнтов: литерал арабской или
# грузинской буквы молча портится при передаче через редактор и буфер, и
# проверка потом «проходит» на испорченном диапазоне, ничего не находя.
def _rng(a, b):
    return '%s-%s' % (chr(a), chr(b))


H_CYR = _rng(0x0400, 0x04FF)
H_ARAB = _rng(0x0600, 0x06FF)
H_DEVA = _rng(0x0900, 0x097F)
H_GEO = _rng(0x10A0, 0x10FF)
H_CJK = _rng(0x4E00, 0x9FFF) + _rng(0x3400, 0x4DBF)


def words(s):
    u"""Слова текста: разметка, адреса и служебные хвосты выброшены."""
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?s)<!--.*?-->', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'https?://\S+', ' ', s)
    s = re.sub(r'&[a-z]+;|&#\d+;', ' ', s)
    # Иероглифы отделяем пробелами ДО разбиения: в письменности без пробелов
    # целый абзац иначе становится одним «словом», и совпадение множеств
    # падает до нуля на верном тексте. Китайский так и показывал 2,7 процента.
    s = re.sub(r'([一-鿿㐀-䶿])', r' \1 ', s)
    letters = ('0-9A-Za-z' + H_CYR + H_ARAB + H_DEVA + H_GEO + H_CJK)
    return [w for w in re.split(r'[^%s]+' % letters, s) if w]


def md_words(path):
    s = io.open(path, encoding='utf-8').read()
    s = re.sub(r'(?s)^---.*?---', ' ', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'[#*>`|_-]+', ' ', s)
    return words(s)


def main():
    if not os.path.isdir(KYC):
        print(u'каталога KYC нет: %s' % KYC)
        return 0
    root = os.path.join(KYC, 'app', 'public', 'documents')
    assert os.path.isdir(root), root

    rows, drifted = [], 0
    for lang in sorted(os.listdir(root)):
        d = os.path.join(root, lang)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            m = re.fullmatch(r'%s([0-9]{2})\.html' % lang, f)
            if not m:
                continue
            num = m.group(1)
            if lang not in B.SLUGS:
                rows.append((lang, num, u'мастеров языка нет', None))
                continue
            src = os.path.join(B.md_dir(lang), B.corpus_file(num, lang))
            if not os.path.isfile(src):
                rows.append((lang, num, u'мастера нет - документ снят?', None))
                drifted += 1
                continue
            a = md_words(src)
            b = words(io.open(os.path.join(d, f), encoding='utf-8').read())
            # Копия несёт обвязку страницы: меню, подвал, кнопки. Сравниваем
            # присутствие слов мастера в копии, а не длину.
            miss = len([w for w in set(a) if w not in set(b)])
            share = 100.0 * (len(set(a)) - miss) / max(1, len(set(a)))
            ok = share >= 97.0
            rows.append((lang, num,
                         u'слов мастера %d, нет в копии %d (%.1f%% совпало)'
                         % (len(set(a)), miss, share), ok))
            if not ok:
                drifted += 1

    width = max(len(r[2]) for r in rows) if rows else 10
    print('')
    print(u'ДРЕЙФ КОПИЙ КОРПУСА В KYC: %d файлов' % len(rows))
    print('=' * min(110, width + 24))
    for lang, num, note, ok in rows:
        mark = u'ok   ' if ok else (u'?    ' if ok is None else u'ДРЕЙФ')
        print(u'  %s %s%s  %s' % (mark, lang, num, note))
    print('=' * min(110, width + 24))
    print(u'разошлось: %d из %d' % (drifted, len(rows)))
    print(u'')
    print(u'Синк ручной. Это измеритель: он показывает, где копия отстала, и')
    print(u'не переносит текст сам - KYC работающая система с оплатой.')
    return drifted


if __name__ == '__main__':
    sys.exit(main())
