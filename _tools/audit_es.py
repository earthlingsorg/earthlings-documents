# -*- coding: utf-8 -*-
"""Машинная вычитка испанского корпуса.

Сделан из audit_fr.py, который свежее audit_de.py и в котором уже вычищены
восемь классов ложных срабатываний. Ловит то же самое, но своими списками:
испанский даёт другой набор следов перевода.

Пять различий против французского аудита, каждое существенное:

1. Кавычки. Испанская пара - ёлочки (U+00AB + U+00BB): RAE считает comillas
   latinas основными кавычками языка. Запрещены английские (U+201C/U+201D),
   немецкая низкая (U+201E) и типографский апостроф (U+2019).
2. Пробела перед `; : ! ?` в испанском НЕТ - это французская норма, а не
   испанская. Проверка «пробел перед знаком» здесь полная, как в немецком.
3. Перевёрнутые `¿` и `¡` - родная пунктуация, и они ОБЯЗАТЕЛЬНЫ. Проверяется
   не запрет, а парность: `¿` к `?` и `¡` к `!`.
4. Пробела внутри ёлочек в испанском быть не должно (во французском - должен).
   Проверка перевёрнута: ловим `« текст »`, а не `«текст»`.
5. Правоспособность и дееспособность в испанском разводятся одной парой -
   capacidad juridica / capacidad de obrar - и она работает и для человека, и
   для коллективного субъекта. Французской второй пары здесь не нужно.
   Но personalidad juridica добавлена: официальный испанский текст статьи 16
   Пакта передаёт этим словом правоспособность человека.

Использование: python _tools/audit_es.py [es]
"""
import io, os, re, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = sys.argv[1] if len(sys.argv) > 1 else 'es'
DIR = os.path.join(REPO, LANG)
assert os.path.isdir(DIR), DIR


class Tee(object):
    """Пишет отчёт в файл UTF-8 и одновременно в консоль.

    Без этого аудит падает на первом же диакритическом знаке: русская консоль
    Windows работает в cp866, и 'ñ' в неё не кодируется - процесс умирает
    посреди отчёта с UnicodeEncodeError. В консоль отдаём с заменой
    непредставимых знаков, полный текст читается из файла.
    """

    def __init__(self, path, console):
        self.f = io.open(path, 'w', encoding='utf-8', newline='\n')
        self.c = console
        self.enc = getattr(console, 'encoding', None) or 'ascii'

    def write(self, s):
        self.f.write(s)
        try:
            self.c.write(s)
        except UnicodeEncodeError:
            self.c.write(s.encode(self.enc, 'replace').decode(self.enc))

    def flush(self):
        self.f.flush()
        self.c.flush()


REPORT = os.path.join(REPO, '_tools', 'audit-report-%s.txt' % LANG)
sys.stdout = Tee(REPORT, sys.stdout)


def load():
    out = {}
    for f in sorted(os.listdir(DIR)):
        if f.endswith('.md') and f[0].isdigit():
            out[f] = io.open(os.path.join(DIR, f), encoding='utf-8').read()
    m = os.path.join(REPO, '_manifest', '%s-manifest.md' % LANG)
    if os.path.isfile(m):
        out['manifest'] = io.open(m, encoding='utf-8').read()
    assert out, 'нет мастеров в %s - переводить ещё нечего' % DIR
    assert all(t.strip() for t in out.values()), 'пустой файл на входе'
    return out


# Смешение орфографических вариантов в одном корпусе носитель видит сразу.
# Слева норма корпуса, справа конкурент. Пара печатается, только если в
# корпусе есть ОБА варианта: одиночное вхождение нормы дефектом не является.
# 'sólo', 'éste', 'ésta', 'aquél' - формы, от которых RAE отказалась в 2010;
# они не запрещены, но соседство с современной формой выдаёт разнобой.
PAIRS = [('período', 'periodo'), ('solo ', 'sólo '), ('guion', 'guión'),
         ('este ', 'éste '), ('esta ', 'ésta '), ('aquel ', 'aquél '),
         ('quórum', 'quorum'), ('vídeo', 'video'),
         ('Estado', 'estado nacional'), ('sustituir', 'substituir')]

# Заглавная A без диакритики в начале фразы во французском была реальной
# ошибкой набора; в испанском таких пар нет, и раздел заменён проверкой
# перевёрнутых знаков (раздел 6).

# Обороты, верные поодиночке и выдающие перевод, когда размазаны по корпусу.
# Часть из них - законная испанская правовая проза; порог 10 вхождений и
# ручной разбор, а не автоматический дефект.
TICS = ['en el marco de', 'a nivel de', 'en lo que respecta a',
        'cabe señalar', 'cabe destacar', 'por otra parte', 'además de ello',
        'desde el punto de vista de', 'en la medida en que',
        'teniendo en cuenta', 'de manera que', 'a título de', 'así pues',
        'es preciso subrayar', 'por regla general', 'en el plano de',
        'a este respecto', 'con el fin de', 'por medio de', 'en el seno de',
        'con vistas a', 'no obstante', 'dicho', 'el citado', 'el referido',
        'en aras de', 'a los efectos de']

# Каждый русский термин обязан иметь ровно одно испанское соответствие.
# Основной вариант - первый; остальные конкуренты, которые надо вытеснить.
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

# Кальки: грамматически верно и выдаёт русский исходник.
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
    # «el mismo» вместо притяжательного - канцелярит, который RAE прямо
    # не рекомендует. Ловится ТОЛЬКО местоименное употребление: за ним сразу
    # идёт знак препинания. Прилагательное «el mismo umbral», «la misma
    # manera» - правильный испанский, и первая версия правила давала на нём
    # 34 ложных срабатывания из 34.
    (r'\b(?:del|al|de la|de los|de las|en el|en la) mism[oa]s?\b(?=\s*[.,;:)])',
     'притяжательное: su / sus'),
    # «el cual» после предлога - норма испанского и часто единственный способ
    # снять двусмысленность («cada una de las cuales», «a partir de los
    # cuales»). Канцеляритом он становится только как подлежащее после
    # запятой, и ловим именно это.
    (r',\s(?:el|la|los|las) cual(?:es)?\b',
     'que / quien: «, el cual» как подлежащее - имитация канцелярского стиля'),
]

# Имя народа не переводится и не транслитерируется ни в одном языке,
# включая метаданные. Это правило из инструкции, не предпочтение.
# Испанский эквивалент немецкого Erdling и французского Terrien.
FORBIDDEN_WORDS = ['terrícola', 'terrícolas', 'Terrícola', 'Terrícolas']

# Замки раздела 7 в es/_СЛОВАРЬ_РЕШЕНИЙ.md, которых не ловит ни один другой
# раздел аудита. Разделены по тому, бывает ли законное вхождение.

# HARD - законного вхождения не бывает: любое найденное есть дефект.
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

# SOFT - вхождение законно ровно тогда, когда речь о государстве, а не о нас,
# либо внутри цитаты или отрицания. Печатается списком на ручной разбор.
SOFT_LOCKS = [
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
    (r'\bEthereum\b',
     'сеть в корпусе - Polygon'),
]

# Типографика. Испанская пара ёлочек законна, английские и немецкая - нет.
ES_OPEN, ES_CLOSE = chr(0x00AB), chr(0x00BB)
INV_Q, INV_E = chr(0x00BF), chr(0x00A1)
BAD_CHARS = {
    0x2014: 'длинное тире', 0x2013: 'короткое тире', 0x2212: 'минус',
    0x2026: 'многоточие одним знаком',
    0x201C: 'английская открывающая кавычка',
    0x201D: 'английская закрывающая кавычка',
    0x201E: 'немецкая низкая кавычка',
    0x2018: 'английская одинарная', 0x2019: 'типографский апостроф',
    0x00A0: 'неразрывный пробел', 0x202F: 'узкий неразрывный',
    0x2009: 'тонкий пробел', 0x200B: 'нулевой пробел', 0x200C: 'ZWNJ',
    0x2060: 'word-joiner', 0xFEFF: 'BOM',
}


def sentences(text):
    """Предложения внутри абзаца, а не через весь файл.

    Резать сразу по всему тексту нельзя: абзац, следующий за точкой и
    начинающийся с врезки `>`, дефиса списка или строчной буквы, приклеивается
    к предыдущему, и счётчик выдаёт несуществующие предложения.
    """
    body = re.sub(r'`[^`]*`|\[[^\]]*\]\([^)]*\)|^\|.*$|^#+ .*$', ' ',
                  text, flags=re.M)
    for para in re.split(r'\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)', body):
        para = ' '.join(para.split())
        if not para:
            continue
        # Открывающая ёлочка и перевёрнутые знаки в классе символов собираются
        # из кодпойнтов: литерал молча портится при передаче через heredoc.
        for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑÜ"*'
                          + ES_OPEN + INV_Q + INV_E + r'])', para):
            yield s


def unquoted(s):
    """Текст без дословных цитат из актов и без служебных строк.

    Цитата воспроизводит орфографию подлинника, а она бывает старше нынешней
    нормы: резолюция 1541 (XV) 1960 года пишет «distinto de éste», и RAE
    отменила это ударение только в 2010-м. Править цитату нельзя, а считать
    её разнобоем корпуса - ложная тревога. По той же причине выбрасываются
    адреса и код: '?' в 'safe.global/home?safe=' не вопросительный знак.
    """
    s = re.sub(ES_OPEN + r'[^' + ES_CLOSE + r']*' + ES_CLOSE, ' ', s)
    s = re.sub(r'`[^`]*`|\((?:https?|mailto):[^)]*\)|\bhttps?://\S+', ' ', s)
    return s


def count_word(s, w):
    """Счёт по границе слова: без неё 'video' находится внутри 'Montevideo'."""
    return len(re.findall(r'(?<![\w-])' + re.escape(w.strip()) + r'(?![\w-])', s))


def main():
    texts = load()
    allw = ' '.join(texts.values())
    clean = {n: unquoted(s) for n, s in texts.items()}
    allc = ' '.join(clean.values())
    low = allw.lower()

    print('файлов: %d, слов: %d' % (len(texts), len(allw.split())))

    print('\n=== 1. ОРФОГРАФИЧЕСКИЕ ВАРИАНТЫ ===')
    problems = 0
    for a, b in PAIRS:
        na, nb = count_word(allc, a), count_word(allc, b)
        if na and nb:
            problems += 1
            wa = sorted(n for n, s in clean.items() if count_word(s, a))
            wb = sorted(n for n, s in clean.items() if count_word(s, b))
            print('  СМЕШЕНИЕ %-14s %3d %s' % (a.strip(), na, ','.join(wa)[:56]))
            print('           %-14s %3d %s' % (b.strip(), nb, ','.join(wb)[:56]))
    if not problems:
        print('  чисто')

    print('\n=== 2. ОБОРОТЫ-ТИКИ (>= 10 вхождений) ===')
    shown = 0
    for t in sorted(TICS, key=lambda x: -low.count(x.lower())):
        n = low.count(t.lower())
        if n >= 10:
            inf = sum(1 for s in texts.values() if t.lower() in s.lower())
            print('  %4d x  "%s"  (файлов: %d)' % (n, t, inf))
            shown += 1
    if not shown:
        print('  чисто')

    print('\n=== 3. РАСПОЛЗАНИЕ ТЕРМИНОВ ===')
    drift = 0
    for ru, variants in sorted(GLOSSARY.items()):
        counts = [(v, len(re.findall(r'(?<![\w-])' + re.escape(v) + r'\w{0,3}(?![\w-])',
                                     allw, re.I))) for v in variants]
        used = [(v, c) for v, c in counts if c]
        if len(used) > 1:
            drift += 1
            print('  %-24s %s' % (ru, '  |  '.join('%s=%d' % (v, c) for v, c in used)))
    if not drift:
        print('  чисто')

    print('\n=== 4. КАЛЬКИ ===')
    found = 0
    for pat, fix in CALQUES:
        hits = [(n, len(re.findall(pat, s))) for n, s in texts.items()]
        hits = [(n, c) for n, c in hits if c]
        if hits:
            found += 1
            total = sum(c for _, c in hits)
            print('  %-40s %3d  -> %s' % (pat.replace(r'\b', '')[:40], total, fix))
            print('        %s' % ', '.join('%s:%d' % (n, c) for n, c in hits)[:110])
    if not found:
        print('  чисто')

    print('\n=== 5. МЕХАНИКА ===')
    # Пробел перед знаком препинания в испанском - всегда ошибка: пробел
    # перед `; : ! ?` есть французская норма, а не испанская.
    mech = 0
    for name, s in sorted(texts.items()):
        for label, pat in [('двойной пробел', r'[^\n] {2,}[^\n]'),
                           ('пробел перед знаком', r' [,.;:!?](?:\s|$)'),
                           ('повтор слова', r'\b(\w+) \1\b')]:
            m = [x for x in re.findall(pat, s)
                 if not (label == 'повтор слова'
                         # «se se» не бывает, а «la la» бывает в перечнях;
                         # служебные слова и возвратные формы исключаем.
                         and x.lower() in ('la', 'el', 'los', 'las', 'de',
                                           'del', 'a', 'que', 'quien',
                                           'se', 'no', 'y', 'o', 'lo'))]
            if m:
                mech += 1
                print('  %-34s %-32s %d  %s'
                      % (name[:34], label, len(m), str(m[:3])[:60]))
    if not mech:
        print('  чисто')

    print('\n=== 6. ТИПОГРАФИКА ===')
    # Словарь строится из числовых кодпойнтов: литералы молча портятся
    # при передаче через heredoc и буфер обмена.
    bad = collections.Counter()
    for name, s in sorted(texts.items()):
        for ch in s:
            if ord(ch) in BAD_CHARS:
                bad['%s: %s' % (name[:24], BAD_CHARS[ord(ch)])] += 1
    if bad:
        for k, v in sorted(bad.items()):
            print('  %-52s %d' % (k, v))
    else:
        print('  чисто')
    op, cl = allw.count(ES_OPEN), allw.count(ES_CLOSE)
    print('  испанские ёлочки: открывающих %d, закрывающих %d%s'
          % (op, cl, '' if op == cl else '   <-- НЕ СОВПАДАЕТ'))
    # Пробел внутри ёлочек - французская норма, в испанском его быть не должно.
    # Проверка перевёрнута против audit_fr.py намеренно.
    loose = len(re.findall(ES_OPEN + r' ', allw)) + \
        len(re.findall(r' ' + ES_CLOSE, allw))
    print('  ёлочек с пробелом внутри: %d%s'
          % (loose, '' if not loose else '   <-- убрать, это французская норма'))
    # Перевёрнутые знаки обязательны и должны быть парны своим прямым.
    # Считаем по файлам и по тексту без адресов: '?' в строке запроса
    # 'safe.global/home?safe=' не вопросительный знак и пары не требует.
    for name, s in sorted(clean.items()):
        for inv, direct, label in ((INV_Q, '?', 'вопрос'), (INV_E, '!', 'воскл')):
            a, b = s.count(inv), s.count(direct)
            if a != b:
                print('  %-26s %s: %s=%d, %s=%d   <-- НЕ СОВПАДАЕТ'
                      % (name[:26], label, inv, a, direct, b))
    print('  перевёрнутых всего: %s=%d, %s=%d'
          % (INV_Q, allc.count(INV_Q), INV_E, allc.count(INV_E)))

    print('\n=== 7. ИМЯ НАРОДА НЕ ПЕРЕВОДИТСЯ ===')
    hits = [(n, w) for n, s in sorted(texts.items())
            for w in FORBIDDEN_WORDS if re.search(r'\b%s\b' % w, s)]
    print('  ' + (str(hits) if hits else 'чисто (везде Earthlings латиницей)'))

    print('\n=== 8. ПРАВОСПОСОБНОСТЬ, ДЕЕСПОСОБНОСТЬ, ПРАВОСУБЪЕКТНОСТЬ ===')
    # capacidad juridica - способность иметь права; capacidad de obrar -
    # способность их осуществлять, и она же для коллективного субъекта;
    # personalidad juridica - правосубъектность, и она же стоит в официальном
    # испанском тексте статьи 16 Пакта о правоспособности человека.
    # Подмена меняет смысл, разбирается по таблице 5.4 словаря решений.
    for w in ('capacidad jurídica', 'capacidad de obrar',
              'personalidad jurídica', 'persona jurídica', 'persona física'):
        where = [n for n, s in sorted(texts.items()) if w in s]
        if where:
            print('  %-24s %d раз  %s' % (w, allw.count(w), ','.join(where)[:66]))

    print('\n=== 9. ДЛИННЫЕ ПРЕДЛОЖЕНИЯ (> 60 слов) ===')
    long_found = 0
    for name, s in sorted(texts.items()):
        for sent in sentences(s):
            w = len(sent.split())
            if w > 60:
                long_found += 1
                print('  %-30s %3d слов  %s...' % (name[:30], w, sent[:90]))
    if not long_found:
        print('  чисто')

    print('\n=== 10. ЗАМКИ ===')
    # Раздел 7 файла es/_СЛОВАРЬ_РЕШЕНИЙ.md. Делится надвое, и смешивать
    # половины нельзя: у одной любое вхождение - дефект, у другой вхождение
    # законно ровно тогда, когда речь о государстве, а не о нас.
    hard = 0
    for pat, why in HARD_LOCKS:
        for name, s in sorted(texts.items()):
            for m in re.finditer(pat, s):
                hard += 1
                ctx = ' '.join(s[max(0, m.start() - 45):m.end() + 45].split())
                print('  ДЕФЕКТ %-22s %-24s %s' % (m.group(0)[:22], name[:24], ctx[:80]))
                print('         %s' % why)
    if not hard:
        print('  жёсткие замки: чисто')
    soft = collections.Counter()
    for pat, why in SOFT_LOCKS:
        for name, s in sorted(texts.items()):
            for m in re.finditer(pat, s, re.I):
                soft[(m.group(0).lower(), name, why)] += 1
    if soft:
        print('  на ручной разбор (законно только о государстве, не о нас):')
        for (w, name, why), n in sorted(soft.items()):
            print('    %-22s %-24s %2d  %s' % (w[:22], name[:24], n, why[:60]))
    else:
        print('  мягкие замки: чисто')

    print('\n=== 11. ЦИТАТЫ, КОТОРЫЕ НАДО СВЕРЯТЬ С ПОДЛИННИКОМ ===')
    # Испанский - аутентичный язык Устава ООН, Пактов и Всеобщей декларации.
    # Обратный перевод с русского недопустим - печатаем список для сверки.
    q = 0
    for name, s in sorted(texts.items()):
        for para in re.split(r'\n\s*\n', s):
            if re.search(r'Carta de las Naciones Unidas|Naciones Unidas|Pacto|'
                         r'Declaración Universal|artículo \d+ (de|del)',
                         para) and ES_OPEN in para:
                q += 1
                print('  %-24s %s...' % (name[:24], ' '.join(para.split())[:110]))
    print('  всего: %d - каждую сверить с аутентичным испанским текстом акта' % q)
    print('\nполный отчёт в UTF-8: %s' % os.path.relpath(REPORT, REPO))


if __name__ == '__main__':
    main()
    sys.stdout.flush()
