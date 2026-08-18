# -*- coding: utf-8 -*-
"""Машинная вычитка французского корпуса.

Устроен как audit_de.py и ловит то же самое, но своими списками: французский
даёт другой набор следов перевода. Стилистику не оценивает - это работа
близкого чтения.

Четыре различия против немецкого аудита, каждое существенное:

1. Кавычки. Французская пара - ёлочки (U+00AB + U+00BB), законная норма языка,
   а не признак машинного текста. Запрещены английские (U+201C/U+201D) и
   немецкая низкая (U+201E): они попадают в текст из чужой раскладки.
2. Пробел перед `;` `:` `!` `?` во французском НОРМА, а не механическая
   ошибка. Проверка «пробел перед знаком» сужена до запятой и точки.
   Пробел при этом обычный ASCII, а не узкий неразрывный: решение проекта,
   подтверждённое прецедентом корпуса (59 пар ёлочек, ноль U+202F).
3. Порог длины предложения 60 слов: французская правовая проза держит
   придаточные лучше английской и хуже немецкой.
4. Правоспособность и дееспособность разведены отдельной проверкой, и к ним
   добавлена personnalite juridique: официальный французский текст статьи 16
   Пакта передаёт этим словом правоспособность человека, и путаница здесь
   стоит дороже, чем в немецком.

Использование: python _tools/audit_fr.py [fr]
"""
import io, os, re, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = sys.argv[1] if len(sys.argv) > 1 else 'fr'
DIR = os.path.join(REPO, LANG)
assert os.path.isdir(DIR), DIR


class Tee(object):
    """Пишет отчёт в файл UTF-8 и одновременно в консоль.

    Без этого аудит падает на первом же диакритическом знаке: русская консоль
    Windows работает в cp866, и 'é' в неё не кодируется - процесс умирает
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
# Слева норма корпуса, справа конкурент.
# Лигатура œ (U+0153) - законная французская буква, а не типографский изыск;
# запрещать её нельзя, но смешивать с разложенным 'oe' в одном корпусе тоже.
PAIRS = [('État', 'Etat'), ('œuvre', 'oeuvre'), ('cœur', 'coeur'),
         ('vœu', 'voeu'), ('sœur', 'soeur'), ('nœud', 'noeud'),
         ('événement', 'évènement'), ('clé ', 'clef '),
         ('Île', 'Ile')]

# Заглавная A без диакритики в начале фразы. Простой парой это не ловится:
# 'A ' встречается в 'A/B', 'AES-256' и в именах, и даёт постоянный ложный шум.
BARE_A = re.compile(r"(?<![\w-])A (?=[A-ZÉÀ])")

# Обороты, верные поодиночке и выдающие перевод, когда размазаны по корпусу.
# Часть из них - законная французская правовая проза; порог 10 вхождений и
# ручной разбор, а не автоматический дефект.
TICS = ['dans le cadre de', 'au niveau de', 'en ce qui concerne',
        'il convient de', 'à cet égard', 'par ailleurs', 'en outre',
        'du point de vue de', 'dans la mesure où', 'à savoir',
        'compte tenu de', 'de manière à', 'au titre de', 'ainsi donc',
        'il est à noter', 'il faut souligner', 'en règle générale',
        'sur le plan de', 'à ce titre', 'de ce fait', 'dans le but de',
        'par le biais de', 'au sein de', 'en vue de']

# Каждый русский термин обязан иметь ровно одно французское соответствие.
# Основной вариант - первый; остальные конкуренты, которые надо вытеснить.
# Источник: fr/_СЛОВАРЬ_РЕШЕНИЙ.md, разделы 2 и 3.
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

# Кальки: грамматически верно и выдаёт русский исходник.
CALQUES = [
    # «dans l'ordre de leur dépôt» - правильный французский (порядок следования),
    # а не калька русского «порядка» как процедуры. Исключено.
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
    (r"\bau cours de \d", "dans un délai de"),
    (r'\bà partir du moment où\b', 'dès que'),
    (r'\best obligé de\b', 'doit'),
    (r'\bau moyen du fait que\b', 'parce que'),
    (r'\bil est nécessaire de noter\b', 'выбросить'),
]

# Имя народа не переводится и не транслитерируется ни в одном языке,
# включая метаданные. Это правило из инструкции, не предпочтение.
# Французский эквивалент немецкого Erdling.
FORBIDDEN_WORDS = ['Terrien', 'Terriens', 'Terrienne', 'Terriennes',
                   'terrien', 'terriens']

# Замки раздела 7 в fr/_СЛОВАРЬ_РЕШЕНИЙ.md, которых не ловит ни один другой
# раздел аудита. Разделены по тому, бывает ли законное вхождение.

# HARD - законного вхождения не бывает: любое найденное есть дефект.
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

# SOFT - вхождение законно ровно тогда, когда речь о государстве, а не о нас,
# либо внутри цитаты или отрицания. Печатается списком на ручной разбор.
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
    (r'\bEthereum\b',
     'сеть в корпусе - Polygon'),
]

# Типографика. Французская пара ёлочек законна, английские и немецкая - нет.
FR_OPEN, FR_CLOSE = chr(0x00AB), chr(0x00BB)
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
        # Открывающая ёлочка в классе символов собирается из кодпойнта:
        # литерал молча портится при передаче через heredoc и буфер обмена.
        for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÀÂÉÈÊÎÔÙÛÇ"*' + FR_OPEN + r'])',
                          para):
            yield s


def main():
    texts = load()
    allw = ' '.join(texts.values())
    low = allw.lower()

    print('файлов: %d, слов: %d' % (len(texts), len(allw.split())))

    print('\n=== 1. ОРФОГРАФИЧЕСКИЕ ВАРИАНТЫ ===')
    problems = 0
    for a, b in PAIRS:
        na, nb = allw.count(a), allw.count(b)
        if na and nb:
            problems += 1
            wa = sorted(n for n, s in texts.items() if a in s)
            wb = sorted(n for n, s in texts.items() if b in s)
            print('  СМЕШЕНИЕ %-12s %3d %s' % (a.strip(), na, ','.join(wa)[:60]))
            print('           %-12s %3d %s' % (b.strip(), nb, ','.join(wb)[:60]))
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
        counts = [(v, len(re.findall(r"(?<![\w'-])" + re.escape(v) + r"\w{0,3}(?![\w-])",
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
        hits = [(n, len(re.findall(pat, s, re.I))) for n, s in texts.items()]
        hits = [(n, c) for n, c in hits if c]
        if hits:
            found += 1
            total = sum(c for _, c in hits)
            print('  %-40s %3d  -> %s' % (pat.replace(r'\b', '')[:40], total, fix))
            print('        %s' % ', '.join('%s:%d' % (n, c) for n, c in hits)[:110])
    if not found:
        print('  чисто')

    print('\n=== 5. МЕХАНИКА ===')
    # Пробел перед ; : ! ? во французском - норма, а не ошибка: проверяем
    # только запятую и точку. Пробел при этом обязан быть обычным ASCII -
    # узкий неразрывный ловится разделом 6.
    mech = 0
    for name, s in sorted(texts.items()):
        for label, pat in [('двойной пробел', r'[^\n] {2,}[^\n]'),
                           ('пробел перед запятой или точкой', r' [,.](?:\s|$)'),
                           ('повтор слова', r'\b(\w+) \1\b')]:
            m = [x for x in re.findall(pat, s)
                 if not (label == 'повтор слова'
                         # «vous vous connectez», «nous nous choisissons» -
                         # возвратная форма, а не повтор слова
                         and x.lower() in ('la', 'le', 'les', 'de', 'des',
                                           'du', 'a', 'que', 'qui',
                                           'nous', 'vous', 'se'))]
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
    op, cl = allw.count(FR_OPEN), allw.count(FR_CLOSE)
    print('  французские ёлочки: открывающих %d, закрывающих %d%s'
          % (op, cl, '' if op == cl else '   <-- НЕ СОВПАДАЕТ'))
    # Пробел внутри ёлочек обязан быть обычным: узкий неразрывный поймал бы
    # раздел выше, а полное отсутствие пробела - французская ошибка набора.
    tight = len(re.findall(FR_OPEN + r'\S', allw)) + \
        len(re.findall(r'\S' + FR_CLOSE, allw))
    print('  ёлочек без пробела внутри: %d%s'
          % (tight, '' if not tight else '   <-- проверить'))

    print('\n=== 7. ИМЯ НАРОДА НЕ ПЕРЕВОДИТСЯ ===')
    hits = [(n, w) for n, s in sorted(texts.items())
            for w in FORBIDDEN_WORDS if re.search(r'\b%s\b' % w, s)]
    print('  ' + (str(hits) if hits else 'чисто (везде Earthlings латиницей)'))

    print('\n=== 8. ПРАВОСПОСОБНОСТЬ, ДЕЕСПОСОБНОСТЬ, ПРАВОСУБЪЕКТНОСТЬ ===')
    # capacite de jouissance - способность иметь права; capacite d'exercice -
    # способность их осуществлять; capacite d'agir - то же для коллективного
    # субъекта; personnalite juridique - правосубъектность, и она же стоит в
    # официальном французском тексте статьи 16 Пакта о правоспособности
    # человека. Подмена меняет смысл, разбирается по таблице 5.4 словаря.
    for w in ('capacité de jouissance', "capacité d'exercice",
              "capacité d'agir", 'capacité juridique',
              'personnalité juridique'):
        where = [n for n, s in sorted(texts.items()) if w in s]
        if where:
            print('  %-26s %d раз  %s' % (w, allw.count(w), ','.join(where)[:66]))

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
    # Раздел 7 файла fr/_СЛОВАРЬ_РЕШЕНИЙ.md. Делится надвое, и смешивать
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
    # Французский - аутентичный язык Устава ООН, Пактов и Всеобщей декларации.
    # Обратный перевод с русского недопустим - печатаем список для сверки.
    q = 0
    for name, s in sorted(texts.items()):
        for para in re.split(r'\n\s*\n', s):
            if re.search(r'Charte des Nations Unies|Nations Unies|Pacte|'
                         r'Déclaration universelle|article \d+ (de|du|des)',
                         para) and FR_OPEN in para:
                q += 1
                print('  %-24s %s...' % (name[:24], ' '.join(para.split())[:110]))
    print('  всего: %d - каждую сверить с аутентичным французским текстом акта' % q)
    print('\nполный отчёт в UTF-8: %s' % os.path.relpath(REPORT, REPO))


if __name__ == '__main__':
    main()
    sys.stdout.flush()
