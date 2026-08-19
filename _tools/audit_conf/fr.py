# -*- coding: utf-8 -*-
"""Французский: списки для audit_lang.py.

Четыре вещи, своих только для французского:

1. Кавычки - ёлочки (U+00AB/U+00BB), законная норма языка. Запрещены
   английские и немецкая низкая: они попадают в текст из чужой раскладки.
2. Пробел перед `; : ! ?` во французском НОРМА, а не механическая ошибка.
   Проверка «пробел перед знаком» сужена до запятой и точки. Пробел при этом
   обычный ASCII, а не узкий неразрывный: решение проекта, подтверждённое
   прецедентом корпуса - 59 пар ёлочек, ноль U+202F.
3. Лигатура œ (U+0153) - законная французская буква, а не типографский изыск.
   Запрещать её нельзя, но смешивать с разложенным 'oe' в одном корпусе тоже.
4. Правоспособность и дееспособность разведены отдельной проверкой, и к ним
   добавлена personnalite juridique: официальный французский текст статьи 16
   Пакта передаёт этим словом правоспособность человека.

Французский - аутентичный язык Устава, Пактов и Всеобщей декларации, поэтому
расползание терминов считается по всему тексту, вместе с цитатами: цитата на
аутентичном языке обязана совпадать с термином корпуса, и расхождение внутри
неё есть настоящий сигнал, а не шум.
"""
import re
from . import _helpers as H

LANG = 'fr'
TITLE = 'французский'

COUNT = 'flex'
GLOSSARY_ON = 'raw'
# Обороты считаются без учёта регистра: «En outre» и «en outre» - одно и то же,
# а французский регулярно открывает ими предложение.
TICS_CI = True
LETTERS = 'A-Za-zÀÂÄÉÈÊËÎÏÔÖÙÛÜÇàâäéèêëîïôöùûüçŒœ'
SPACE_BEFORE_PUNCT = ',.'      # перед ; : ! ? пробел - французская норма
SENT_START = 'A-ZÀÂÉÈÊÎÔÙÛÇ"*' + H.GUILLEMET_OPEN

PAIRS = [('État', 'Etat'), ('œuvre', 'oeuvre'), ('cœur', 'coeur'),
         ('vœu', 'voeu'), ('sœur', 'soeur'), ('nœud', 'noeud'),
         ('événement', 'évènement'), ('clé', 'clef'),
         ('Île', 'Ile')]

TICS = ['dans le cadre de', 'au niveau de', 'en ce qui concerne',
        'il convient de', 'à cet égard', 'par ailleurs', 'en outre',
        'du point de vue de', 'dans la mesure où', 'à savoir',
        'compte tenu de', 'de manière à', 'au titre de', 'ainsi donc',
        'il est à noter', 'il faut souligner', 'en règle générale',
        'sur le plan de', 'à ce titre', 'de ce fait', 'dans le but de',
        'par le biais de', 'au sein de', 'en vue de']

# Источник: fr/_СЛОВАРЬ_РЕШЕНИЙ.md, разделы 2 и 3.
#
# Числа здесь выше, чем печатал audit_fr.py, и это исправление, а не сдвиг.
# Прежняя граница слова включала апостроф - `(?<![\w'-])`, - и поэтому
# элидированные формы не считались вовсе: l'appartenance, d'identification,
# d'annulation проходили мимо. На одном только слове appartenance это 121
# вхождение из 163. Расползание считается по соотношению вариантов, и
# соотношение было посчитано по трети текста.
GLOSSARY = {
    'народ': ['peuple', 'population', 'nation'],
    'общность': ['communauté', 'collectivité'],
    'Устав': ['Charte', 'statuts des Earthlings'],
    'Казначейство': ['Trésorerie', 'Trésor public', 'Caisse commune'],
    'Фонд': ['Fonds', 'Fondation'],
    'принадлежность': ['appartenance', 'adhésion'],
    'гражданство': ['nationalité', 'citoyenneté'],
    'самоопределение': ['autodétermination', 'libre détermination'],
    'правосубъектность': ['personnalité juridique', 'subjectivité juridique'],
    'свобода объединения': ["liberté d'association", 'liberté de réunion'],
    'взнос': ['cotisation', 'redevance', "frais d'adhésion"],
    'сота': ['cellule', 'alvéole'],
    'учредительный период': ['période constituante', 'période fondatrice',
                             'phase de fondation'],
    'неизменяемое ядро': ['noyau intangible', 'noyau immuable',
                          'noyau inaltérable'],
    'поручение': ['mission', 'mandat'],
    'подтверждение личности': ["vérification d'identité", "contrôle d'identité",
                               'identification'],
    'коренные народы': ['peuples autochtones', 'peuples indigènes'],
    'делегирование': ['délégation', 'procuration'],
    'подотчётность': ['reddition de comptes', 'redevabilité'],
    'отсутствие господства': ['absence de domination', 'non-domination'],
    'управление': ['gouvernance', 'administration'],
    'правовая различимость': ['discernabilité', 'distinguabilité',
                              'visibilité juridique'],
    'гашение': ['destruction', 'brûlage', 'annulation'],
}

CALQUES = [
    # «dans l'ordre de leur dépôt» - правильный французский (порядок
    # следования), а не калька русского «порядка» как процедуры. Исключено.
    (r"(?<!dans )\bl'ordre (de|du|des) (son|sa|ses|la|l'|vérification|"
     r"suppression|examen|adhésion|participation)",
     'la procédure / les modalités'),
    (r"\bdans l'ordre établi\b", 'selon la procédure établie'),
    (r"\bsur les bases générales\b", 'dans les conditions de droit commun'),
    # «mettre en conformité avec» - законный оборот французского права;
    # калька - только предложное употребление вместо «conformément à».
    (r'(?:^|[.,;:] )en conformité avec\b', 'conformément à'),
    (r'\bdans le cas donné\b', 'ici'),
    (r'\ble document donné\b|\bla présente donnée\b', 'ce document'),
    (r"\bà l'heure actuelle\b", 'actuellement'),
    (r'\bpossède le droit\b', 'a le droit'),
    (r'\bporte la responsabilité\b', 'est responsable / répond de'),
    (r"\bs'avère être\b", 'est'),
    # Пассив с НАЗВАННЫМ исполнителем - норма французской нормативной прозы.
    # Калька - только пассив, который действующее лицо прячет.
    (r"(?<!n')\b(est|sont) (effectué|réalisé)e?s?\b"
     r'(?! (par|dans|hors|en|à|au|selon))',
     'активный залог: назвать действующее лицо'),
    (r'\bavec le but de\b', 'pour'),
    (r'\bafin de pouvoir\b', 'pour'),
    (r"\bau cours de \d", 'dans un délai de'),
    (r'\bà partir du moment où\b', 'dès que'),
    (r'\best obligé de\b', 'doit'),
    (r'\bau moyen du fait que\b', 'parce que'),
    (r'\bil est nécessaire de noter\b', 'выбросить'),
]

# Французский эквивалент немецкого Erdling.
FORBIDDEN_WORDS = [r'\b[Tt]errien(?:s|ne|nes)?\b']

HARD_LOCKS = [
    (r'\bvolonté générale\b',
     'руссоистская volonte generale со всем шлейфом; берём volonte commune'),
    (r'\bsubjectivité juridique\b|\bsubjectivité internationale\b',
     'калька континентальной доктрины; берём personnalite juridique'),
    (r'\bquasi-?étatique\w{0,2}\b|\bpara-?étatique\w{0,2}\b|'
     r'\bpara-?souverain\w{0,2}\b',
     'наши институты не государствоподобны'),
    (r'\btitre de voyage\b|\bdocument de voyage\b|'
     r'\bvalable pour franchir\b|\bfranchir une frontière\b',
     'паспорт earthling никогда не подаётся как проездной документ'),
    (r'\bNous ne sommes pas un\b|\bNous ne sommes pas une\b',
     'защитный зачин; переписывается утвердительно'),
    (r'\bde souche\b',
     'этническое чтение слова peuple, от которого корпус защищается'),
]

SOFT_LOCKS = [
    (r"\bau nom de l'humanité\b",
     'законно ТОЛЬКО в отрицании или в приводимой цитате; утверждение - дефект'),
    (r'\bcitoyenneté\w{0,2}\b',
     'для гражданства берём nationalite; citoyennete - только политическое '
     'значение и цитата ДФЕС'),
    (r'\bgouvernement\w{0,2}\b',
     'законно о государстве и в обороте gouvernement du peuple; '
     'наши институты - никогда'),
    (r'\bautorité publique\w{0,2}\b|\bpuissance publique\b|'
     r'\bfonctionnaire\w{0,2}\b|\bagent public\w{0,2}\b',
     'законно о государстве; наши институты - никогда'),
    (r'\bmandat\w{0,3}\b',
     'поручение у нас - mission; mandat законен только о представительстве '
     'государств и выборных мандатах'),
    (r'\bethni\w{0,6}\b',
     'законно только в разделе «Народ и нация», где различение намеренно'),
    (r'\bEthereum\b', 'сеть в корпусе - Polygon'),
]

# capacite de jouissance - способность иметь права; capacite d'exercice -
# способность их осуществлять; capacite d'agir - то же для коллективного
# субъекта; personnalite juridique - правосубъектность, и она же стоит в
# официальном французском тексте статьи 16 Пакта.
CAPACITY = ['capacité de jouissance', "capacité d'exercice", "capacité d'agir",
            'capacité juridique', 'personnalité juridique']

QUOTES_NAME = 'французские ёлочки'
SPACE_IN_QUOTES = True   # « texte » - французская норма, а не дефект

QUOTE_SRC = (r'Charte des Nations Unies|Nations Unies|Pacte|'
             r'Déclaration universelle|article \d+ (de|du|des)')
SOURCE_NOTE = 'каждую сверить с аутентичным французским текстом акта'

# Заглавная A без диакритики в начале фразы: должно быть À.
# Простой парой не ловится - 'A ' встречается в 'A/B', 'AES-256' и в именах,
# и даёт постоянный ложный шум, поэтому нужен просмотр вперёд на заглавную.
#
# В audit_fr.py это выражение было объявлено и НИ РАЗУ не вызвано: проверка
# существовала на бумаге, а французский корпус её не проходил ни разу. Ровно
# от таких потерь и заведён общий инструмент - здесь она включена.
_BARE_A = re.compile(r'(?<![\w-])A (?=[A-ZÉÀ])')


def _bare_a(ctx):
    found = 0
    for name, s in sorted(ctx.texts.items()):
        for m in _BARE_A.finditer(s):
            found += 1
            c = ' '.join(s[max(0, m.start() - 40):m.end() + 40].split())
            print('  %-26s %s' % (name[:26], c[:90]))
    if not found:
        print('  чисто')


EXTRA_SECTIONS = [('5-бис. ЗАГЛАВНАЯ A БЕЗ ДИАКРИТИКИ (должно быть À)', _bare_a)]
