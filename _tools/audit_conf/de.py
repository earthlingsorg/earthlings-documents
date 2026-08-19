# -*- coding: utf-8 -*-
"""Немецкий: списки для audit_lang.py.

Четыре вещи, своих только для немецкого:

1. Кавычки перевёрнуты против остальных языков корпуса: законная пара -
   низкая открывающая U+201E и высокая закрывающая U+201C. Русские ёлочки
   U+00AB/U+00BB здесь ЗАПРЕЩЕНЫ, а в испанском, французском и грузинском
   они норма. Перепутать это значит объявить норму языка ошибкой.
2. Порог длины предложения 70 слов, а не 60: немецкая правовая проза держит
   придаточные лучше французской, и общий порог давал бы сплошной шум.
3. Допуск окончания 6 знаков: немецкое словосложение и склонение дают
   Selbstbestimmungsrecht от Selbstbestimmung, и короткий допуск их разводит.
4. «die die», «das das», «der der» в придаточных - норма немецкого, а не
   опечатка набора, и повтор слова для них выключен поимённо.
"""
from . import _helpers as H

LANG = 'de'
TITLE = 'немецкий'

COUNT = 'flex'
FLEX_EXTRA = 6
GLOSSARY_ON = 'raw'
# Регистр в немецком различает слова, поэтому термины считаются С УЧЁТОМ
# регистра: Kollektiv - существительное, kollektiv - прилагательное.
COUNT_CI = False
TICS_CI = True
LETTERS = 'A-Za-zÄÖÜäöüß'
SPACE_BEFORE_PUNCT = ',.;:!?'
SENT_START = 'A-ZÄÖÜ"*' + H.LOW9_OPEN
LONG_SENT = 70

REPEAT_LETTERS = r'\w'
REPEAT_MIN = 1
REPEAT_SKIP = ('die', 'das', 'der', 'sie', 'so')

PAIRS = [('dass', 'daß'), ('muss', 'muß'), ('Schluss', 'Schluß'),
         ('Fluss', 'Fluß'), ('gemäss', 'gemäß'), ('grösser', 'größer'),
         ('Grösse', 'Größe'), ('Strasse', 'Straße'), ('heisst', 'heißt'),
         ('E-Mail', 'Email'), ('sodass', 'so dass')]

TICS = ['im Rahmen von', 'in Bezug auf', 'im Hinblick auf', 'hinsichtlich',
        'diesbezüglich', 'darüber hinaus', 'im Falle von', 'seitens',
        'es sei darauf hingewiesen', 'es ist zu beachten', 'in der Regel',
        'grundsätzlich', 'entsprechend den', 'im Sinne von', 'zum einen',
        'nach Massgabe', 'nach Maßgabe', 'im Zuge', 'vor dem Hintergrund',
        'unter Berücksichtigung', 'in diesem Zusammenhang']

# Источник: раздел 13 ПЕРЕВОД_КОРПУСА_ЕДИНАЯ_ИНСТРУКЦИЯ.md, подраздел E.
GLOSSARY = {
    'народ': ['Volk', 'Bevölkerung', 'Nation', 'Gemeinwesen'],
    'общность': ['Gemeinschaft', 'Gemeinde', 'Kollektiv'],
    'Устав': ['Charta', 'Satzung', 'Statut'],
    'Казначейство': ['Schatzkammer', 'Schatzamt', 'Finanzverwaltung'],
    'Фонд': ['Fonds', 'Stiftung'],
    'принадлежность': ['Zugehörigkeit', 'Mitgliedschaft', 'Angehörigkeit'],
    'гражданство': ['Staatsangehörigkeit', 'Staatsbürgerschaft'],
    'самоопределение': ['Selbstbestimmung', 'Selbstbestimmungsrecht'],
    'правосубъектность': ['Rechtspersönlichkeit', 'Rechtssubjektivität'],
    'свобода объединения': ['Vereinigungsfreiheit', 'Versammlungsfreiheit'],
    'взнос': ['Beitrag', 'Gebühr', 'Abgabe'],
    'сота': ['Zelle', 'Wabe'],
    'учредительный период': ['Gründungsperiode', 'Gründungsphase',
                             'konstituierende Periode', 'Gründungszeitraum'],
    'неизменяемое ядро': ['unabänderlicher Kern', 'unveränderlicher Kern',
                          'unantastbarer Kern'],
    'гашение': ['Löschung', 'Verbrennung', 'Vernichtung', 'Annullierung'],
    'кворум': ['Quorum', 'Beschlussfähigkeit'],
    'поручение': ['Mandat', 'Auftrag', 'Weisung'],
    'ничтожно': ['nichtig', 'ungültig', 'unwirksam'],
    'отвод': ['Befangenheit', 'Ausschluss von der Abstimmung'],
}

CALQUES = [
    (r'\bin der Ordnung\b', 'in der Weise / nach dem Verfahren'),
    (r'\bauf allgemeiner Grundlage\b', 'unter den allgemeinen Voraussetzungen'),
    (r'\bim gegebenen Fall\b', 'hier'),
    (r'\bdas gegebene Dokument\b', 'dieses Dokument'),
    (r'\bder gegebene\b', '"dieser" вместо "der gegebene"'),
    (r'\bzum gegenwärtigen Zeitpunkt\b', 'jetzt / derzeit'),
    (r'\bvon Seiten\b', 'durch'),
    (r'\bstellt (eine|einen|ein) .{1,30} dar\b', 'ist'),
    (r'\bträgt (die )?Verantwortung vor\b', 'haftet gegenüber'),
    (r'\bnach Erreichen des Alters\b', 'ab 18 Jahren'),
    (r'\bbesitzt das Recht\b', 'hat das Recht'),
    (r'\bim Laufe von\b', 'innerhalb'),
    (r'\bwird durchgeführt\b', 'активный залог'),
    (r'\bwerden durchgeführt\b', 'активный залог'),
    (r'\bist verpflichtet zu\b', 'muss'),
    (r'\bin Übereinstimmung mit\b', 'nach / gemäß'),
    (r'\bmit dem Ziel\b', 'um zu'),
    (r'\bin der Eigenschaft (als|von)\b', 'als'),
]

FORBIDDEN_WORDS = [r'\bErdling(?:e|en|s)?\b', r'\bErdbewohner\w{0,3}\b',
                   r'\bErdenbürger\w{0,3}\b']

HARD_LOCKS = [
    (r'\bGemeinwille\w{0,3}\b',
     'руссоистская volonte generale со всем шлейфом; берём gemeinsamer Wille'),
    (r'(?<![\w-])Rechtssubjektivität\w{0,6}(?![\w-])',
     'калька континентальной доктрины; берём Rechtspersönlichkeit'),
    (r'\bvölkisch\w{0,3}\b', 'прямая отсылка к этнонационализму'),
    (r'\bVolkstum\w{0,3}\b|\bVolksgruppe\w{0,2}\b|\bVolkszugehörigkeit\w{0,3}\b',
     'этническое чтение слова Volk, от которого корпус защищается'),
    (r'\bstaats(ähnlich|gleich)\w{0,3}\b',
     'наши институты не государствоподобны'),
    (r'\bWir sind kein\w{0,2}\b',
     'защитный зачин; переписывается утвердительно'),
    (r'\bReisepass\w{0,3}\b|\bAusweisdokument\w{0,3}\b',
     'паспорт earthling никогда не подаётся как проездной документ'),
]

SOFT_LOCKS = [
    # Был жёстким замком и оказался негодным в этом качестве. Корпус
    # ОТКАЗЫВАЕТСЯ говорить от имени человечества, и делает это словами: фраза
    # законно стоит в отрицании (документ 04) и внутри приводимого возражения
    # (документ 26). Жёсткий замок на ней даёт постоянный шум и перестаёт быть
    # замком; мягкий печатает список, и утвердительное употребление видно.
    (r'\bim Namen der Menschheit\b',
     'законно ТОЛЬКО в отрицании или в приводимой цитате; утверждение - дефект'),
    (r'\bStaatsbürgerschaft\w{0,3}\b',
     'для гражданства берём Staatsangehörigkeit (GG Art. 16)'),
    (r'\bRegierung\w{0,3}\b',
     'законно о государстве; наши институты - никогда'),
    (r'\bBehörde\w{0,2}\b|\bAmtsträger\w{0,2}\b|\bHoheitsgewalt\b',
     'законно о государстве; наши институты - никогда'),
    (r'\bEthereum\b', 'сеть в корпусе - Polygon'),
]

# Rechtsfähigkeit - способность иметь права; Geschäftsfähigkeit - способность
# их осуществлять. В корпусе это разные утверждения, и подмена меняет смысл.
CAPACITY = ['Rechtsfähigkeit', 'Geschäftsfähigkeit', 'Handlungsfähigkeit']
CAPACITY_TITLE = 'ПРАВОСПОСОБНОСТЬ И ДЕЕСПОСОБНОСТЬ'

# Немецкая пара кавычек законна; ёлочки в немецком тексте - чужая раскладка.
QUOTES = (H.LOW9_OPEN, H.LOW9_CLOSE)
QUOTES_NAME = 'немецкие кавычки'
ALLOWED = {0x201E, 0x201C}
EXTRA_BAD = {0x00AB: 'русская ёлочка', 0x00BB: 'русская ёлочка'}

# У Устава ООН и Пактов есть официальные немецкие тексты. Обратный перевод с
# русского недопустим - печатаем список для ручной сверки.
QUOTE_SRC = (r'Charta der Vereinten Nationen|Vereinte Nationen|'
             r'Pakt|Artikel \d+ (der|des)')
SOURCE_NOTE = 'каждую сверить с официальным немецким текстом акта'
