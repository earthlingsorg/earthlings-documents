# -*- coding: utf-8 -*-
"""Машинная вычитка немецкого корпуса.

Устроен как audit_en.py и ловит то же самое, но своими списками: немецкий
даёт другой набор следов перевода. Стилистику не оценивает - это работа
близкого чтения.

Три различия против английского аудита, каждое существенное:

1. Кавычки. Немецкая пара низкая-верхняя (U+201E + U+201C) - законная норма
   языка, а не признак машинного текста, и запрещать её нельзя. Запрещена
   английская закрывающая (U+201D): она попадает в текст из русского или
   английского исходника и выдаёт его.
2. Порог длины предложения выше: немецкий синтаксис держит придаточные,
   на которых английский рассыпается.
3. Правоспособность и дееспособность разведены отдельной проверкой:
   Rechtsfähigkeit и Geschäftsfähigkeit - разные вещи, и корпус уже занял
   похожий термин в других языках.

Использование: python _tools/audit_de.py [de]
"""
import io, os, re, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = sys.argv[1] if len(sys.argv) > 1 else 'de'
DIR = os.path.join(REPO, LANG)
assert os.path.isdir(DIR), DIR


class Tee(object):
    """Пишет отчёт в файл UTF-8 и одновременно в консоль.

    Без этого аудит немецкого падает на первом же умлауте: русская консоль
    Windows работает в cp866, а 'ä' в неё не кодируется - процесс умирает
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


# Смешение старой и новой орфографии в одном корпусе носитель видит сразу.
# Слева новая норма, справа старая или швейцарская.
PAIRS = [('dass ', 'daß '), ('muss ', 'muß '), ('Schluss', 'Schluß'),
         ('Fluss', 'Fluß'), ('gemäss', 'gemäß'), ('grösser', 'größer'),
         ('Grösse', 'Größe'), ('Strasse', 'Straße'), ('heisst', 'heißt'),
         ('E-Mail', 'Email'), ('sodass', 'so dass')]

# Обороты, верные поодиночке и выдающие перевод, когда размазаны по корпусу.
TICS = ['im Rahmen von', 'in Bezug auf', 'im Hinblick auf', 'hinsichtlich',
        'diesbezüglich', 'darüber hinaus', 'im Falle von', 'seitens',
        'es sei darauf hingewiesen', 'es ist zu beachten', 'in der Regel',
        'grundsätzlich', 'entsprechend den', 'im Sinne von', 'zum einen',
        'nach Massgabe', 'nach Maßgabe', 'im Zuge', 'vor dem Hintergrund',
        'unter Berücksichtigung', 'in diesem Zusammenhang']

# Каждый русский термин обязан иметь ровно одно немецкое соответствие.
# Основной вариант - первый; остальные конкуренты, которые надо вытеснить.
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

# Кальки: грамматически верно и выдаёт русский исходник.
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

# Имя народа не переводится и не транслитерируется ни в одном языке,
# включая метаданные. Это правило из инструкции, не предпочтение.
FORBIDDEN_WORDS = ['Erdling', 'Erdlinge', 'Erdbewohner', 'Erdenbürger']

# Типографика. Немецкая пара кавычек законна, английская закрывающая - нет.
DE_OPEN, DE_CLOSE = chr(0x201E), chr(0x201C)
BAD_CHARS = {
    0x2014: 'длинное тире', 0x2013: 'короткое тире', 0x2212: 'минус',
    0x2026: 'многоточие одним знаком', 0x201D: 'английская закрывающая кавычка',
    0x2018: 'английская одинарная', 0x2019: 'английская одинарная',
    0x00AB: 'русская ёлочка', 0x00BB: 'русская ёлочка',
    0x00A0: 'неразрывный пробел', 0x202F: 'узкий неразрывный',
    0x2009: 'тонкий пробел', 0x200B: 'нулевой пробел', 0x200C: 'ZWNJ',
    0x2060: 'word-joiner', 0xFEFF: 'BOM',
}


def sentences(text):
    """Предложения внутри абзаца, а не через весь файл.

    Резать сразу по всему тексту нельзя: абзац, следующий за точкой и
    начинающийся с врезки `>`, дефиса списка или строчной буквы, приклеивается
    к предыдущему, и счётчик выдаёт несуществующие предложения на шестьдесят
    слов. На английском корпусе это давало ложные срабатывания.
    """
    body = re.sub(r'`[^`]*`|\[[^\]]*\]\([^)]*\)|^\|.*$|^#+ .*$', ' ',
                  text, flags=re.M)
    # Пункт списка - отдельная единица: без этого весь перечень считается
    # одним предложением и любой список из десяти пунктов «длинный».
    for para in re.split(r'\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)', body):
        para = ' '.join(para.split())
        if not para:
            continue
        # Открывающая кавычка в классе символов собирается из кодпойнта:
        # литерал молча портится при передаче через heredoc и буфер обмена.
        for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ"*' + DE_OPEN + r'])', para):
            yield s


def main():
    texts = load()
    allw = ' '.join(texts.values())
    low = allw.lower()

    print('файлов: %d, слов: %d' % (len(texts), len(allw.split())))

    print('\n=== 1. ОРФОГРАФИЧЕСКИЕ ВАРИАНТЫ ===')
    problems = 0
    for a, b in PAIRS:
        na, nb = low.count(a.lower()), low.count(b.lower())
        if na and nb:
            problems += 1
            wa = sorted(n for n, s in texts.items() if a.lower() in s.lower())
            wb = sorted(n for n, s in texts.items() if b.lower() in s.lower())
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
        counts = [(v, len(re.findall(r'(?<![\w-])' + re.escape(v) + r'\w{0,6}(?![\w-])',
                                     allw))) for v in variants]
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
            print('  %-34s %3d  -> %s' % (pat.replace(r'\b', ''), total, fix))
            print('        %s' % ', '.join('%s:%d' % (n, c) for n, c in hits)[:110])
    if not found:
        print('  чисто')

    print('\n=== 5. МЕХАНИКА ===')
    mech = 0
    for name, s in sorted(texts.items()):
        for label, pat in [('двойной пробел', r'[^\n] {2,}[^\n]'),
                           ('пробел перед знаком', r' [,.;:!?]'),
                           ('повтор слова', r'\b(\w+) \1\b')]:
            m = [x for x in re.findall(pat, s)
                 if not (label == 'повтор слова'
                         and x.lower() in ('die', 'das', 'der', 'sie', 'so'))]
            if m:
                mech += 1
                print('  %-34s %-18s %d  %s' % (name[:34], label, len(m), str(m[:3])[:60]))
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
    op, cl = allw.count(DE_OPEN), allw.count(DE_CLOSE)
    print('  немецкие кавычки: открывающих %d, закрывающих %d%s'
          % (op, cl, '' if op == cl else '   <-- НЕ СОВПАДАЕТ'))

    print('\n=== 7. ИМЯ НАРОДА НЕ ПЕРЕВОДИТСЯ ===')
    hits = [(n, w) for n, s in sorted(texts.items())
            for w in FORBIDDEN_WORDS if re.search(r'\b%s\b' % w, s)]
    print('  ' + (str(hits) if hits else 'чисто (везде Earthlings латиницей)'))

    print('\n=== 8. ПРАВОСПОСОБНОСТЬ И ДЕЕСПОСОБНОСТЬ ===')
    # Rechtsfähigkeit - способность иметь права; Geschäftsfähigkeit - способность
    # их осуществлять. В корпусе это разные утверждения, и подмена меняет смысл.
    for w in ('Rechtsfähigkeit', 'Geschäftsfähigkeit', 'Handlungsfähigkeit'):
        where = [n for n, s in sorted(texts.items()) if w in s]
        if where:
            print('  %-20s %d раз  %s' % (w, allw.count(w), ','.join(where)[:70]))

    print('\n=== 9. ДЛИННЫЕ ПРЕДЛОЖЕНИЯ (> 70 слов) ===')
    long_found = 0
    for name, s in sorted(texts.items()):
        for sent in sentences(s):
            w = len(sent.split())
            if w > 70:
                long_found += 1
                print('  %-30s %3d слов  %s...' % (name[:30], w, sent[:90]))
    if not long_found:
        print('  чисто')

    print('\n=== 10. ЦИТАТЫ, КОТОРЫЕ НАДО СВЕРЯТЬ С ПОДЛИННИКОМ ===')
    # У Устава ООН и Пактов есть официальные немецкие тексты. Обратный перевод
    # с русского недопустим - печатаем список для ручной сверки.
    q = 0
    for name, s in sorted(texts.items()):
        for para in re.split(r'\n\s*\n', s):
            if re.search(r'Charta der Vereinten Nationen|Vereinte Nationen|'
                         r'Pakt|Artikel \d+ (der|des)', para) and DE_OPEN in para:
                q += 1
                print('  %-24s %s...' % (name[:24], ' '.join(para.split())[:110]))
    print('  всего: %d - каждую сверить с официальным немецким текстом акта' % q)
    print('\nполный отчёт в UTF-8: %s' % os.path.relpath(REPORT, REPO))


if __name__ == '__main__':
    main()
    sys.stdout.flush()
