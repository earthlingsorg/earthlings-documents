# -*- coding: utf-8 -*-
"""Английский: списки для audit_lang.py.

Английский устроен иначе остальных языков корпуса, и это видно по составу
проверок. Формы почти не меняются, поэтому термины считаются по границе слова
без допуска окончания. Кавычки прямые ASCII, а не ёлочки и не низкие: типографские
запрещены наравне с остальными языками. Замков в английском нет ни жёстких, ни
мягких - вместо них четыре своих проверки, каждая выросла из построчного чтения
Декларации, Правового обоснования, Устава и Возражений:

- согласование числа у data (корпус трактует его как множественное);
- калька «в порядке, установленном» - in the order вместо in the manner;
- разнобой register / registry;
- неоднозначное «the Charter» там, где рядом стоит Устав ООН или Африканская
  хартия.

Английский - аутентичный язык Устава, Пактов и Всеобщей декларации.
"""
import re

LANG = 'en'
TITLE = 'английский'

COUNT = 'word'
GLOSSARY_ON = 'raw'
LETTERS = 'A-Za-z'
SPACE_BEFORE_PUNCT = ',.;:!?'
SENT_START = 'A-Z"*'
LONG_SENT = 60

# Смешивать британский и американский в одном корпусе - первое, что замечает
# носитель. Корпус ведётся в оксфордской норме: -ize, но programme/defence.
# Пары даны основами, поэтому считаются с допуском окончания.
PAIRS_COUNT = 'term'
PAIRS = [('organiz', 'organis'), ('recogniz', 'recognis'), ('realiz', 'realis'),
         ('minimiz', 'minimis'), ('maximiz', 'maximis'), ('legaliz', 'legalis'),
         ('anonymiz', 'anonymis'), ('pseudonymiz', 'pseudonymis'),
         ('authoriz', 'authoris'), ('defense', 'defence'),
         ('offense', 'offence'), ('favor', 'favour'),
         ('behavior', 'behaviour'), ('labor', 'labour'), ('honor', 'honour'),
         ('center', 'centre'), ('fulfill', 'fulfil'), ('toward', 'towards'),
         ('judgement', 'judgment'),
         ('acknowledgement', 'acknowledgment')]

TICS = ['in the manner laid down by', 'laid down by', 'is not a ground',
        'under any circumstances', 'at any moment', 'on general terms',
        'in so far as', 'it should be noted', 'it is worth',
        'in the name of the people', 'on the merits', 'as a general rule',
        'is entitled to', 'precisely because', 'what is meant is',
        'that is precisely why', 'by its nature', 'in full', 'of its own',
        'is not the case', 'in the event of', 'for the sake of']

GLOSSARY = {
    'народ': ['the people', 'a people'],
    'Устав': ['the Earthlings Charter', 'the Charter'],
    # Строка дрейфа, а не замок: она печатает соотношение вариантов. Запрет
    # на «membership in the people» стоит ниже, в HARD_LOCKS, и держится
    # отдельно - до 2026-08-21 неверный вариант был здесь ЗАКОННОЙ
    # альтернативой, и его возвращение аудит бы не заметил.
    'принадлежность': ['belonging', 'affiliation', 'membership in the people'],
    'взнос': ['contribution', 'fee', 'dues'],
    'сота': ['Cell', 'cell', 'hive'],
    'расчётная единица': ['unit of account', 'settlement unit',
                          'accounting unit'],
    # Ложные срабатывания, проверенные 2026-08-16 и подтверждённые: все 16
    # commission - имена собственные (Африканская комиссия, Избирательная
    # комиссия, Комиссия юристов, Комиссия международного права), а
    # единственный assignment значит «задание», а не поручение в смысле
    # мандата. Термин корпуса - mandate, расползания нет.
    'поручение': ['mandate', 'commission', 'assignment', 'instruction'],
    'ограничение полномочий': ['restriction of powers', 'limitation of powers'],
    'гашение': ['burning', 'redemption', 'cancellation of the passport'],
    'правовая различимость': ['legal cognizability', 'legal distinguishability',
                              'legal recognizability'],
    'неизменяемое ядро': ['unamendable core', 'immutable core',
                          'unchangeable core'],
    'учредительный период': ['founding period', 'constituent period',
                             'constitutive period'],
    'подтверждение личности': ['identity confirmation', 'identity verification'],
    'ничтожно': ['void', 'null and void'],
    'отвод': ['recusal', 'withdrawal from the vote', 'disqualification'],
    'кворум': ['quorum'],
    'этап становления структур': ['structure-formation stage',
                                  'formation stage'],
}

CALQUES = [
    (r'\bin case of\b', 'in the event of / if'),
    (r'\bon the contrary\b(?!,)', 'запятая после'),
    (r'\bthe given\b', '"this" вместо "the given"'),
    (r'\bit is necessary to\b', 'глагол в повелительном'),
    (r'\bis carried out\b', 'активный залог'),
    (r'\bare carried out\b', 'активный залог'),
    (r'\bis realized\b', 'is achieved / is exercised'),
    (r'\bcarries out a mandate\b', 'acts under a mandate'),
    (r'\bin connection with\b', 'because of / under'),
    (r'\bwith the aim of\b', 'to'),
    (r'\bin the quality of\b', 'as'),
    (r'\bhaving reached the age\b', 'aged 18 or over'),
    (r'\bthe given document\b', 'this document'),
    (r'\bat the present time\b', 'now'),
    (r'\bin the given case\b', 'here'),
    (r'\bfrom the side of\b', 'by'),
    (r'\bmore detailed\b', 'more detail'),
    (r'\bdo not represent\b', 'are not'),
]

# Имя народа не переводится: Earthling - и есть английское слово.
FORBIDDEN_WORDS = [r'\b[Ee]arth-?dweller\w{0,2}\b', r'\b[Tt]errestrials?\b']

# Кавычки корпуса - прямые ASCII. Типографские запрещены общим словарём.
QUOTES = ('"', '"')
QUOTES_NAME = 'прямые кавычки'

QUOTE_SRC = (r'Article \d+ of the (Declaration|Charter)|'
             r'(Declaration|Charter), Article \d+')
SOURCE_NOTE = 'каждую сверить с текстом процитированной статьи'


def _data_number(ctx):
    """Корпус трактует data как множественное число."""
    bad = [(n, len(re.findall(r'\bdata (is|was|has been|does)\b', s)))
           for n, s in sorted(ctx.texts.items())]
    bad = [(n, c) for n, c in bad if c]
    print('  ' + (str(bad) if bad else 'чисто (корпус трактует data как мн. ч.)'))


def _order_calque(ctx):
    """«В порядке, установленном» - должно быть in the manner."""
    hits = [(n, len(re.findall(
        r'in the order (of|established|provided|described|set)', s)))
        for n, s in sorted(ctx.texts.items())]
    hits = [(n, c) for n, c in hits if c]
    print('  ' + (str(hits) if hits else 'чисто (должно быть in the manner)'))


def _register_registry(ctx):
    """«Реестр участников» - registry; register оставлен за реестром народов,
    церковными книгами и реестром медиаторов."""
    for w in ('registry', 'register'):
        n = len(re.findall(r'(?<![\w-])%ss?(?![\w-])' % w, ctx.allw, re.I))
        print('  %-10s %d' % (w, n))
    stray = [(n, len(re.findall(r'register of participants', s, re.I)))
             for n, s in sorted(ctx.texts.items())]
    stray = [(n, c) for n, c in stray if c]
    print('  "register of participants" (должно быть registry): %s'
          % (stray if stray else 'нет'))


def _ambiguous_charter(ctx):
    """В корпусе the Charter = Устав Earthlings. Там, где рядом стоит ООН или
    Африканская хартия, требуется уточнение."""
    found = 0
    for n, s in sorted(ctx.texts.items()):
        for m in re.finditer(
                r'(?<!UN )(?<!Earthlings )(?<!African )'
                r'(?<!the United Nations )\bthe Charter\b', s):
            c = ' '.join(s[max(0, m.start() - 90):m.end() + 40].split())
            if re.search(r'\bUN\b|United Nations|African|Article 1\(2\)|Covenant',
                         c):
                found += 1
                print('  %-22s ...%s...' % (n[:22], c))
    if not found:
        print('  чисто')


# Замок принадлежности, поставлен 2026-08-21. Перепись 20 августа нашла
# 28 мест, где корпус говорил «членство» о принадлежности к народу, и все
# восемь языков их несли. Дефект нашла не вычитка, а машинная пара у
# арабского - `الانتماء` против `العضوية`. У английского такой пары не было
# вовсе, и он оказался языком с наибольшим числом правок вместе с немецким.
#
# Замок жёсткий, потому что законного вхождения у этих сочетаний нет:
# `member of the Council`, `member States`, цитата статьи 33(1) UNDRIP и
# племенные реестры США под шаблон не попадают - там слово стоит без
# `of the people` и без `fee`. Проверено на всех 25 мастерах: 0 срабатываний.
HARD_LOCKS = [
    (r'\bmembership (?:in|of) the people\b|'
     r'\bmembers? of the (?:Earthlings )?people\b|'
     r'\bmembership fee\b|\bmembership dues\b',
     'принадлежность к народу - belonging; membership о народе запрещено'),
]

EXTRA_SECTIONS = [
    ('5-бис. СОГЛАСОВАНИЕ ЧИСЛА У DATA', _data_number),
    ('5-трис. КАЛЬКА «В ПОРЯДКЕ, УСТАНОВЛЕННОМ»', _order_calque),
    ('5-кватер. РАЗНОБОЙ REGISTER / REGISTRY', _register_registry),
    ('5-квинт. НЕОДНОЗНАЧНОЕ "the Charter"', _ambiguous_charter),
]
