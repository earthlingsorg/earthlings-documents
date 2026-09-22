# -*- coding: utf-8 -*-
"""Испанский: списки для audit_lang.py.

Четыре вещи, своих только для испанского:

1. Кавычки - ёлочки (U+00AB/U+00BB): RAE считает comillas latinas основными
   кавычками языка. Английские, немецкая низкая и типографский апостроф
   запрещены наравне с остальными языками корпуса.
2. Пробела перед `; : ! ?` в испанском НЕТ - это французская норма. Проверка
   «пробел перед знаком» здесь полная, как в немецком.
3. Перевёрнутые `¿` и `¡` - родная пунктуация и ОБЯЗАТЕЛЬНЫ. Проверяется не
   запрет, а парность: `¿` к `?` и `¡` к `!`.
4. Правоспособность и дееспособность разводятся одной парой - capacidad
   juridica / capacidad de obrar, - и она работает и для человека, и для
   коллективного субъекта. Но personalidad juridica нужна отдельно:
   официальный испанский текст статьи 16 Пакта передаёт этим словом
   правоспособность человека.

Испанский - аутентичный язык Устава, обоих Пактов и Всеобщей декларации:
его текст сам является подлинником, а не переводом.
"""
from . import _helpers as H

LANG = 'es'
TITLE = 'испанский'

COUNT = 'flex'
GLOSSARY_ON = 'raw'   # испанский - аутентичный язык актов, цитата обязана совпадать
LETTERS = 'A-Za-zÁÉÍÓÚÑÜáéíóúñü'
SPACE_BEFORE_PUNCT = ',.;:!?'
SENT_START = ('A-ZÁÉÍÓÚÑÜ"*' + H.GUILLEMET_OPEN + H.INV_Q + H.INV_E)

# 'sólo', 'éste', 'ésta', 'aquél' - формы, от которых RAE отказалась в 2010;
# они не запрещены, но соседство с современной формой выдаёт разнобой.
PAIRS = [('período', 'periodo'), ('solo', 'sólo'), ('guion', 'guión'),
         ('este', 'éste'), ('esta', 'ésta'), ('aquel', 'aquél'),
         ('quórum', 'quorum'), ('vídeo', 'video'),
         ('Estado', 'estado nacional'), ('sustituir', 'substituir')]

TICS = ['en el marco de', 'a nivel de', 'en lo que respecta a',
        'cabe señalar', 'cabe destacar', 'por otra parte', 'además de ello',
        'desde el punto de vista de', 'en la medida en que',
        'teniendo en cuenta', 'de manera que', 'a título de', 'así pues',
        'es preciso subrayar', 'por regla general', 'en el plano de',
        'a este respecto', 'con el fin de', 'por medio de', 'en el seno de',
        'con vistas a', 'no obstante', 'dicho', 'el citado', 'el referido',
        'en aras de', 'a los efectos de']

# Источник: es/_СЛОВАРЬ_РЕШЕНИЙ.md, разделы 2 и 3.
GLOSSARY = {
    'народ': ['pueblo', 'población', 'nación'],
    'общность': ['comunidad', 'colectividad'],
    'Устав': ['Carta', 'Estatutos de los Earthlings'],
    'Казначейство': ['Tesorería', 'Tesoro Público', 'Caja común'],
    'Фонд': ['Fondo', 'Fundación'],
    'принадлежность': ['pertenencia', 'adhesión'],
    'гражданство': ['nacionalidad', 'ciudadanía'],
    'самоопределение': ['libre determinación', 'autodeterminación'],
    'правосубъектность': ['personalidad jurídica', 'subjetividad jurídica'],
    'свобода объединения': ['libertad de asociación', 'libertad de reunión'],
    'взнос': ['cuota', 'tasa de entrada', 'canon'],
    'сота': ['célula', 'celda'],
    'учредительный период': ['período constituyente', 'período fundacional',
                             'fase de fundación'],
    'неизменяемое ядро': ['núcleo intangible', 'núcleo inmutable',
                          'núcleo inalterable'],
    'поручение': ['encargo', 'mandato'],
    'подтверждение личности': ['verificación de identidad',
                               'control de identidad', 'identificación'],
    'коренные народы': ['pueblos indígenas', 'pueblos originarios'],
    'делегирование': ['delegación', 'voto por poder'],
    'подотчётность': ['rendición de cuentas', 'responsabilidad'],
    'отсутствие господства': ['ausencia de dominación', 'no dominación'],
    'управление': ['gobernanza', 'administración'],
    'правовая различимость': ['discernibilidad', 'distinguibilidad',
                              'visibilidad jurídica'],
    'гашение': ['destrucción', 'quema', 'anulación'],
    'ничтожно': ['nulo de pleno derecho', 'inválido'],
}

CALQUES = [
    # Русское «порядок» как процедура. «en orden de llegada», «por orden
    # alfabético» - правильный испанский, а не калька; исключены просмотром
    # назад по предлогу.
    (r'(?<!en )(?<!por )\bel orden (de|del|de la|de su) (verificación|'
     r'supresión|examen|adhesión|participación|revisión)',
     'el procedimiento / las modalidades'),
    (r'\ben el orden establecido\b', 'conforme al procedimiento establecido'),
    (r'\ben las bases generales\b', 'en las condiciones generales'),
    # «poner en conformidad con» - законный оборот; калька - только
    # предложное употребление вместо «conforme a».
    (r'(?:^|[.,;:] )[Ee]n conformidad con\b', 'conforme a / de acuerdo con'),
    (r'\ben el caso dado\b', 'aquí / en este caso'),
    (r'\bel documento dado\b|\bla presente dada\b', 'este documento'),
    (r'\ben el momento actual\b', 'actualmente'),
    (r'\bposee el derecho\b', 'tiene derecho'),
    (r'\blleva la responsabilidad\b', 'es responsable / responde de'),
    (r'\bresulta ser\b(?! posible| necesario)', 'es'),
    # Пассив с НАЗВАННЫМ исполнителем - норма испанской нормативной прозы,
    # как и возвратный пассив se + глагол. Калька - только пассив с ser,
    # который действующее лицо прячет.
    (r'(?<!no )\b(es|son) (realizad|efectuad|llevad)[oa]s?\b'
     r'(?! (por|en|a|al|dentro|conforme|según))',
     'возвратный пассив se + глагол либо назвать действующее лицо'),
    (r'\bcon el objetivo de\b', 'para'),
    (r'\ba fin de poder\b', 'para'),
    (r'\ben el transcurso de \d', 'en un plazo de'),
    (r'\ba partir del momento en que\b', 'desde que'),
    (r'\bes necesario señalar\b|\bhay que señalar que\b', 'выбросить'),
    # «el mismo» вместо притяжательного - канцелярит, который RAE прямо не
    # рекомендует. Ловится ТОЛЬКО местоименное употребление: за ним сразу идёт
    # знак препинания. Прилагательное «el mismo umbral», «la misma manera» -
    # правильный испанский, и первая версия правила давала на нём 34 ложных
    # срабатывания из 34.
    (r'\b(?:del|al|de la|de los|de las|en el|en la) mism[oa]s?\b(?=\s*[.,;:)])',
     'притяжательное: su / sus'),
    # «el cual» после предлога - норма испанского и часто единственный способ
    # снять двусмысленность. Канцеляритом он становится только как подлежащее
    # после запятой, и ловим именно это.
    (r',\s(?:el|la|los|las) cual(?:es)?\b',
     'que / quien: «, el cual» как подлежащее - имитация канцелярского стиля'),
]

# Испанский эквивалент немецкого Erdling и французского Terrien.
FORBIDDEN_WORDS = [r'\b[Tt]err[íi]colas?\b']

HARD_LOCKS = [
    (r'\bvoluntad general\b',
     'руссоистская voluntad general со всем шлейфом; берём voluntad comun'),
    (r'\bsubjetividad jurídica\b|\bsubjetividad internacional\b',
     'калька континентальной доктрины; берём personalidad juridica'),
    (r'\bcuasi-?estatal\w{0,2}\b|\bparaestatal\w{0,2}\b|'
     r'\bpara-?soberan\w{0,2}\b',
     'наши институты не государствоподобны'),
    (r'\btítulo de viaje\b|\bdocumento de viaje\b|'
     r'\bválido para cruzar\b|\bcruzar una frontera\b',
     'паспорт earthling никогда не подаётся как проездной документ'),
    (r'\bNo somos un\b|\bNo somos una\b',
     'защитный зачин; переписывается утвердительно'),
    (r'\bde pura cepa\b',
     'этническое чтение слова pueblo, от которого корпус защищается'),
    (r'\bautodeterminación\b',
     'самоопределение в корпусе - libre determinacion, слово актов; '
     'autodeterminacion - слово каталонского спора'),
    (r'\bderecho a decidir\b',
     'лозунг каталонского спора; берём facultad de decidir / poder de decision'),
    (r'\bdeclaración de voluntad\b',
     'сделочный термин частного права; берём expresion de la voluntad'),
    (r'\bEstatutos de los Earthlings\b',
     'Устав у нас - la Carta; Estatutos - обязательный документ испанской '
     'ассоциации по LO 1/2002, а корпус защищается от чтения «мы ассоциация»'),
]

SOFT_LOCKS = [
    # Замок принадлежности, поставлен 2026-08-21. Мягкий, а не жёсткий, из-за
    # одного законного вхождения: `es/04` разбирает расхождение официального
    # русского перевода статьи 33(1) UNDRIP с аутентичным текстом, и слово
    # «membresía» там названо КАК СЛОВО. Замена уничтожила бы смысл абзаца.
    (r'\bmembres[ií]a\b|\bmiembros? del pueblo\b|\bcuota de (?:miembro|socio)\b',
     'принадлежность к народу - pertenencia; membresia о народе запрещена',
     r'traducci[oó]n|aut[eé]ntic|art[ií]culo 33|'
     r'Declaraci[oó]n de las Naciones Unidas|ind[ií]gena'),
    (r'\ben nombre de la humanidad\b',
     'законно ТОЛЬКО в отрицании или в приводимой цитате; утверждение - дефект'),
    (r'\bciudadan[íi]a\w{0,2}\b',
     'для гражданства берём nacionalidad; ciudadania - только политическое '
     'значение и цитата ДФЕС'),
    (r'\bgobierno\w{0,2}\b',
     'законно о государстве и в обороте gobierno del pueblo; '
     'наши институты - никогда'),
    (r'\bautoridad p[úu]blica\w{0,2}\b|\bpoder p[úu]blico\b|'
     r'\bfuncionario\w{0,2}\b|\bcargo p[úu]blico\w{0,2}\b|\bpotestad\w{0,2}\b',
     'законно о государстве; наши институты - никогда'),
    (r'\bmandato\w{0,2}\b',
     'поручение у нас - encargo; mandato законен только там, где русский '
     'говорит «мандат», и о выборных мандатах государств'),
    (r'\betni\w{0,6}\b|\bétnic\w{0,3}\b',
     'законно только в разделе «Народ и нация», где различение намеренно'),
    (r'\bestatutos\b',
     'вне сочетания «estatutos de una asociacion» в чужом смысле - проверить'),
    (r'\bsocios?\b',
     'earthling - participante или earthling; socio - член ассоциации'),
    (r'\bEthereum\b', 'сеть в корпусе - Polygon'),
]

# capacidad juridica - способность иметь права; capacidad de obrar -
# способность их осуществлять, и она же для коллективного субъекта;
# personalidad juridica - правосубъектность, и она же стоит в официальном
# испанском тексте статьи 16 Пакта. Подмена меняет смысл.
CAPACITY = ['capacidad jurídica', 'capacidad de obrar', 'personalidad jurídica',
            'persona jurídica', 'persona física']

QUOTES_NAME = 'испанские ёлочки'
PAIRED = [(H.INV_Q, '?', 'вопрос'), (H.INV_E, '!', 'воскл')]

QUOTE_SRC = (r'Carta de las Naciones Unidas|Naciones Unidas|Pacto|'
             r'Declaración Universal|artículo \d+ (de|del)')
SOURCE_NOTE = 'каждую сверить с аутентичным испанским текстом акта'
