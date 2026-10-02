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

Мера (с 2026-09-26). Слова мастера и копии сравниваются как ПОСЛЕДОВАТЕЛЬНОСТИ
(`difflib.SequenceMatcher`), а не как множества. До этого сравнивался словарь
документа с порогом 97%, и проверка была слепа: замена слова на другое, уже
встречающееся в документе, перестановка абзацев, пересказ абзаца теми же
словами - всё это давало "0 из 37". Порога больше нет: любой кусок - дрейф,
кроме поимённо названных в KNOWN с доводом.

Считаются только куски `delete` и `replace`: слово мастера пропало из копии или
заменено другим. Куски `insert` НЕ считаются никогда: копия несёт обвязку
страницы (меню с перечнем документов, подвал, подписи ссылок), и эта обвязка
стоит вперемешку с текстом, а не только по краям, - отрезать её нельзя.

ОГРАНИЧЕНИЕ, принятое сознательно: предложение, дописанное в копию и
отсутствующее в мастере, этой мерой НЕ ловится - для неё оно неотличимо от
обвязки. Прежняя мера его не ловила тоже. Если понадобится ловить и это,
нужно сначала вырезать обвязку из копии по разметке, а не по словам.

Запуск:  python _tools/kyc_drift.py [-v]
    -v   все куски, включая названные в KNOWN
Код возврата - число разошедшихся документов.
"""
import difflib
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
# проверка потом "проходит" на испорченном диапазоне, ничего не находя.
#
# Знаки препинания, попадающие внутрь буквенных блоков, вычитаются явным
# списком: иначе арабская запятая или деванагарская данда склеиваются со
# словом, и "слово" с запятой в мастере не совпадает со "слово" в копии.
PUNCT = (0x00D7, 0x00F7,                         # знаки умножения, деления
         0x060C, 0x061B, 0x061F, 0x06D4,         # арабские , ; ? .
         0x0964, 0x0965)                         # данда, двойная данда


def _cls(*ranges):
    u"""Тело класса символов из диапазонов кодпойнтов минус PUNCT."""
    out = []
    for a, b in ranges:
        start = a
        for p in sorted(x for x in PUNCT if a <= x <= b) + [b + 1]:
            if start <= p - 1:
                out.append('%s-%s' % (re.escape(chr(start)),
                                      re.escape(chr(p - 1))))
            start = p + 1
    return ''.join(out)


# Латиница с диакритикой - французский, немецкий, испанский. Без неё `é`
# резало слово надвое, и замена `é` на `è` была невидима.
H_LAT = _cls((0x00C0, 0x024F))
H_CYR = _cls((0x0400, 0x04FF))
H_ARAB = _cls((0x0600, 0x06FF))
H_DEVA = _cls((0x0900, 0x097F))
H_GEO = _cls((0x10A0, 0x10FF))
H_CJK = _cls((0x4E00, 0x9FFF), (0x3400, 0x4DBF))
LETTERS = '0-9A-Za-z' + H_LAT + H_CYR + H_ARAB + H_DEVA + H_GEO + H_CJK

# Адрес - только печатные ASCII без `<` и `>`. Прежнее `https?://\S+` в
# письме без пробелов съедало за адресом весь текст до конца абзаца: копия
# zh/01 несёт автоссылку текстом `&lt;https://...&gt;`, сразу за ней идут
# иероглифы, и целое предложение пропадало из копии, изображая дрейф,
# которого нет.
URL = re.compile(r'https?://[\x21-\x3b\x3d\x3f-\x7e]+')

assert re.findall('[%s]' % H_ARAB, chr(0x060C) + chr(0x0628)) == [chr(0x0628)]
assert re.findall('[%s]' % H_DEVA, chr(0x0964) + chr(0x0915)) == [chr(0x0915)]


def words(s):
    u"""Слова текста: разметка, адреса и служебные хвосты выброшены."""
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?s)<!--.*?-->', ' ', s)
    # Строчные теги снимаются БЕЗ пробела: арабский союз пишется слитно и в
    # копии стоит вплотную к ссылке - `waw<a href=...>слово`. Замена тега
    # пробелом отрывала союз от слова, которое в мастере `waw[слово](...)`
    # остаётся слитным. Блочные теги по-прежнему дают пробел.
    s = re.sub(r'(?i)</?(a|span|strong|em|b|i|code)\b[^>]*>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = URL.sub(' ', s)
    s = re.sub(r'&[a-z]+;|&#\d+;', ' ', s)
    # Иероглифы отделяем пробелами ДО разбиения: в письменности без пробелов
    # целый абзац иначе становится одним "словом".
    s = re.sub('([%s])' % H_CJK, r' \1 ', s)
    return [w for w in re.split(r'[^%s]+' % LETTERS, s) if w]


def md_words(path):
    s = io.open(path, encoding='utf-8').read()
    s = re.sub(r'(?s)^---.*?---', ' ', s)
    # Всё, что копия не несёт ТЕКСТОМ, снимается ДО подстановки служебных
    # знаков ниже: иначе `-` и `_` внутри адреса превращаются в пробелы, адрес
    # перестаёт быть адресом, и его хвост просачивается как слова.
    #   автоссылка <https://...>  - в копии адрес лежит в href;
    #   голый адрес;
    #   номер пункта "1." - в копии его рисует <ol>, текстом он не является.
    s = re.sub(r'<https?://[^>\s]*>', ' ', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = URL.sub(' ', s)
    s = re.sub(r'(?m)^[ \t]*\d+\.[ \t]+', ' ', s)
    # Выделение `**` и код `` ` `` - строчная разметка, как <strong> и <code>
    # в копии, и снимаются так же, без пробела: `waw**слово` в ar/29.
    s = re.sub(r'[*`]+', '', s)
    s = re.sub(r'[#>|_-]+', ' ', s)
    return words(s)


# Куски, названные поимённо: (язык, номер, позиция в мастере) -> довод.
# Прятать сюда настоящий дрейф нельзя: только различие, которое не меняет
# текста, и только если его не удалось снять починкой извлечения.
KNOWN = {}


def chunks(a, b):
    u"""Куски delete и replace: (позиция в мастере, слова мастера, слова копии)."""
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(i1, a[i1:i2], b[j1:j2])
            for tag, i1, i2, j1, j2 in sm.get_opcodes()
            if tag in ('delete', 'replace')]


def _join(ws, lang):
    sep = '' if lang == 'zh' else ' '
    return sep.join(ws) if len(ws) <= 60 else (
        sep.join(ws[:30]) + u' ... ' + sep.join(ws[-30:]))


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    verbose = '-v' in argv
    if not os.path.isdir(KYC):
        print(u'каталога KYC нет: %s' % KYC)
        return 0
    root = os.path.join(KYC, 'app', 'public', 'documents')
    assert os.path.isdir(root), root

    rows, drifted, compared = [], 0, 0
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
                rows.append((lang, num, u'мастеров языка нет', None, []))
                continue
            src = os.path.join(B.md_dir(lang), B.corpus_file(num, lang))
            if not os.path.isfile(src):
                rows.append((lang, num, u'мастера нет - документ снят?',
                             False, []))
                drifted += 1
                continue
            a = md_words(src)
            b = words(io.open(os.path.join(d, f), encoding='utf-8').read())
            # Проверка на нуле слов "проходит" - не давать ей этого.
            assert a, u'мастер пуст после извлечения: %s' % src
            assert b, u'копия пуста после извлечения: %s/%s' % (lang, f)
            compared += 1
            found = chunks(a, b)
            known = [c for c in found if (lang, num, c[0]) in KNOWN]
            bad = [c for c in found if (lang, num, c[0]) not in KNOWN]
            note = u'слов мастера %d, кусков %d' % (len(a), len(bad))
            if known:
                note += u' (+%d названных)' % len(known)
            rows.append((lang, num, note, not bad,
                         bad + (known if verbose else [])))
            if bad:
                drifted += 1

    assert compared, u'ни одной пары мастер-копия не сравнено'
    width = max(len(r[2]) for r in rows) if rows else 10
    print('')
    print(u'ДРЕЙФ КОПИЙ КОРПУСА В KYC: %d файлов' % len(rows))
    print('=' * min(110, width + 24))
    for lang, num, note, ok, found in rows:
        mark = u'ok   ' if ok else (u'?    ' if ok is None else u'ДРЕЙФ')
        print(u'  %s %s%s  %s' % (mark, lang, num, note))
        for pos, ma, co in found:
            tag = KNOWN.get((lang, num, pos))
            print(u'        слово %d%s' % (pos, u'  [названо: %s]' % tag
                                           if tag else u''))
            print(u'          мастер: %s' % _join(ma, lang))
            print(u'          копия:  %s' % (_join(co, lang) if co
                                             else u'(нет)'))
    print('=' * min(110, width + 24))
    print(u'разошлось: %d из %d' % (drifted, len(rows)))
    print(u'')
    print(u'Мера: слова мастера, пропавшие из копии или заменённые. Дописанное')
    print(u'в копию НЕ ловится - оно неотличимо от обвязки страницы.')
    print(u'Синк ручной. Это измеритель: он показывает, где копия отстала, и')
    print(u'не переносит текст сам - KYC работающая система с оплатой.')
    return drifted


if __name__ == '__main__':
    sys.exit(main())
