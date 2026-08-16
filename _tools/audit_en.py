# -*- coding: utf-8 -*-
"""Машинная вычитка английского корпуса.

Ловит то, что на восьмидесяти тысячах слов глаз не находит: разнобой
орфографических вариантов между файлами, расползание терминов, обороты-тики
и кальки с русского. Стилистику не оценивает - это работа близкого чтения.

Использование: python _tools/audit_en.py [en]
"""
import io, os, re, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
DIR = os.path.join(REPO, LANG)
assert os.path.isdir(DIR), DIR


class Tee(object):
    """Пишет отчёт в файл UTF-8 и одновременно в консоль.

    Русская консоль Windows работает в cp866: заголовки разделов в ней
    читаются, а цитата с любым знаком вне этой кодировки роняет процесс
    посреди отчёта. В консоль отдаём с заменой, полный текст - из файла.
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
        if f.endswith('.md'):
            out[f] = io.open(os.path.join(DIR, f), encoding='utf-8').read()
    m = os.path.join(REPO, '_manifest', '%s-manifest.md' % LANG)
    if os.path.isfile(m):
        out['manifest'] = io.open(m, encoding='utf-8').read()
    assert out and all(t.strip() for t in out.values()), 'пустой ввод'
    return out


# Смешивать британский и американский в одном корпусе - первое, что замечает
# носитель. Корпус ведётся в оксфордской норме: -ize, но programme/defence.
PAIRS = [('organiz', 'organis'), ('recogniz', 'recognis'), ('realiz', 'realis'),
         ('minimiz', 'minimis'), ('maximiz', 'maximis'), ('legaliz', 'legalis'),
         ('anonymiz', 'anonymis'), ('pseudonymiz', 'pseudonymis'),
         ('authoriz', 'authoris'), ('defense', 'defence'), ('offense', 'offence'),
         ('favor', 'favour'), ('behavior', 'behaviour'), ('labor', 'labour'),
         ('honor', 'honour'), ('center', 'centre'), ('fulfill', 'fulfil'),
         ('toward ', 'towards '), ('judgement', 'judgment'),
         ('acknowledgement', 'acknowledgment')]

# Обороты, которые верны поодиночке и читаются машинным переводом, когда
# размазаны по всему корпусу.
TICS = ['in the manner laid down by', 'laid down by', 'is not a ground',
        'under any circumstances', 'at any moment', 'on general terms',
        'in so far as', 'it should be noted', 'it is worth',
        'in the name of the people', 'on the merits', 'as a general rule',
        'is entitled to', 'precisely because', 'what is meant is',
        'that is precisely why', 'by its nature', 'in full', 'of its own',
        'is not the case', 'in the event of', 'for the sake of']

# Каждый русский термин обязан иметь ровно одно английское соответствие.
# Слева - что ищем, справа - конкурирующие варианты одного понятия.
GLOSSARY = {
    'народ': ['the people', 'a people'],
    'Устав': ['the Earthlings Charter', 'the Charter'],
    'принадлежность': ['belonging', 'affiliation', 'membership in the people'],
    'взнос': ['contribution', 'fee', 'dues'],
    'сота': ['Cell', 'cell', 'hive'],
    'расчётная единица': ['unit of account', 'settlement unit', 'accounting unit'],
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
    'неизменяемое ядро': ['unamendable core', 'immutable core', 'unchangeable core'],
    'учредительный период': ['founding period', 'constituent period',
                             'constitutive period'],
    'подтверждение личности': ['identity confirmation', 'identity verification'],
    'ничтожно': ['void', 'null and void'],
    'отвод': ['recusal', 'withdrawal from the vote', 'disqualification'],
    'кворум': ['quorum'],
    'этап становления структур': ['structure-formation stage', 'formation stage'],
}

# Кальки: конструкции, грамматически верные и выдающие перевод с русского.
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


# Классы дефектов, найденные построчным чтением Декларации, Правового
# обоснования, Устава и Возражений. Каждый ловится машинно, поэтому вынесен
# сюда: следующая вычитка начинается не с нуля, а с готового списка.
def extra_checks(texts):
    allw = ' '.join(texts.values())

    print('\n=== 7. СОГЛАСОВАНИЕ ЧИСЛА У DATA ===')
    bad = [(n, len(re.findall(r'\bdata (is|was|has been|does)\b', s)))
           for n, s in sorted(texts.items())]
    bad = [(n, c) for n, c in bad if c]
    print('  ' + (str(bad) if bad else 'чисто (корпус трактует data как мн. ч.)'))

    print('\n=== 8. КАЛЬКА «В ПОРЯДКЕ, УСТАНОВЛЕННОМ» ===')
    hits = [(n, len(re.findall(r'in the order (of|established|provided|described|set)', s)))
            for n, s in sorted(texts.items())]
    hits = [(n, c) for n, c in hits if c]
    print('  ' + (str(hits) if hits else 'чисто (должно быть in the manner)'))

    print('\n=== 9. РАЗНОБОЙ REGISTER / REGISTRY ===')
    # «Реестр участников» - основной термин; register оставлен только за
    # реестром народов, церковными книгами и реестром медиаторов.
    for w in ('registry', 'register'):
        n = len(re.findall(r'(?<![\w-])%ss?(?![\w-])' % w, allw, re.I))
        print('  %-10s %d' % (w, n))
    stray = [(n, len(re.findall(r'register of participants', s, re.I)))
             for n, s in sorted(texts.items())]
    stray = [(n, c) for n, c in stray if c]
    print('  "register of participants" (должно быть registry): %s'
          % (stray if stray else 'нет'))

    print('\n=== 10. НЕОДНОЗНАЧНОЕ "the Charter" ===')
    # В корпусе the Charter = Устав Earthlings. Там, где рядом стоит ООН или
    # Африканская хартия, требуется уточнение.
    for n, s in sorted(texts.items()):
        for m in re.finditer(r'(?<!UN )(?<!Earthlings )(?<!African )(?<!the United Nations )'
                             r'\bthe Charter\b', s):
            ctx = ' '.join(s[max(0, m.start() - 90):m.end() + 40].split())
            if re.search(r'\bUN\b|United Nations|African|Article 1\(2\)|Covenant', ctx):
                print('  %-22s ...%s...' % (n[:22], ctx))

    print('\n=== 11. ЦИТАТЫ, КОТОРЫЕ НАДО СВЕРЯТЬ С ИСТОЧНИКОМ ===')
    # Цитата в кавычках обязана совпадать с процитированной статьёй дословно.
    # Машина сверить не может - печатаем список для ручной сверки.
    q = 0
    for n, s in sorted(texts.items()):
        # Абзац, где есть и ссылка на статью корпуса, и текст в кавычках.
        for para in re.split(r'\n\s*\n', s):
            if re.search(r'Article \d+ of the (Declaration|Charter)|'
                         r'(Declaration|Charter), Article \d+', para) and '"' in para:
                q += 1
                frag = ' '.join(para.split())
                print('  %-22s %s...' % (n[:22], frag[:120]))
    print('  всего: %d - каждую сверить с текстом процитированной статьи' % q)


def main():
    texts = load()
    allw = ' '.join(texts.values())
    low = allw.lower()
    problems = 0

    print('файлов: %d, слов: %d' % (len(texts), len(allw.split())))

    print('\n=== 1. ОРФОГРАФИЧЕСКИЕ ВАРИАНТЫ ===')
    for a, b in PAIRS:
        na, nb = low.count(a), low.count(b)
        if na and nb:
            problems += 1
            where_a = sorted(n for n, s in texts.items() if a in s.lower())
            where_b = sorted(n for n, s in texts.items() if b in s.lower())
            print('  СМЕШЕНИЕ %-12s %3d %s' % (a.strip(), na, ','.join(where_a)[:60]))
            print('           %-12s %3d %s' % (b.strip(), nb, ','.join(where_b)[:60]))
    if not problems:
        print('  чисто')

    print('\n=== 2. ОБОРОТЫ-ТИКИ (>= 10 вхождений) ===')
    for t in sorted(TICS, key=lambda x: -low.count(x)):
        n = low.count(t)
        if n >= 10:
            inf = sum(1 for s in texts.values() if t in s.lower())
            print('  %4d x  "%s"  (файлов: %d)' % (n, t, inf))

    print('\n=== 3. РАСПОЛЗАНИЕ ТЕРМИНОВ ===')
    for ru, variants in sorted(GLOSSARY.items()):
        # Варианты, различающиеся только регистром, схлопываем. Счёт идёт с
        # re.I, поэтому такая пара всегда давала бы «расползание» с двумя
        # одинаковыми числами: Cell=95 | cell=95 - это одно множество,
        # посчитанное дважды. Регистр проверяется отдельно, не здесь.
        seen, uniq = set(), []
        for v in variants:
            if v.lower() not in seen:
                seen.add(v.lower())
                uniq.append(v)
        counts = [(v, len(re.findall(r'(?<![\w-])' + re.escape(v) + r'(?![\w-])',
                                     allw, re.I))) for v in uniq]
        used = [(v, c) for v, c in counts if c]
        if len(used) > 1:
            print('  %-24s %s' % (ru, '  |  '.join('%s=%d' % (v, c) for v, c in used)))

    print('\n=== 4. КАЛЬКИ ===')
    found = 0
    for pat, fix in CALQUES:
        hits = [(n, len(re.findall(pat, s, re.I))) for n, s in texts.items()]
        hits = [(n, c) for n, c in hits if c]
        if hits:
            found += 1
            total = sum(c for _, c in hits)
            print('  %-28s %3d  -> %s' % (pat.replace(r'\b', ''), total, fix))
            print('        %s' % ', '.join('%s:%d' % (n, c) for n, c in hits)[:110])
    if not found:
        print('  чисто')

    print('\n=== 5. МЕХАНИКА ===')
    for name, s in sorted(texts.items()):
        for label, pat in [('двойной пробел', r'[^\n] {2,}[^\n]'),
                           ('пробел перед знаком', r' [,.;:!?]'),
                           ('повтор слова', r'\b(\w+) \1\b')]:
            m = re.findall(pat, s)
            m = [x for x in m if not (label == 'повтор слова'
                                      and x.lower() in ('that', 'had', 'the'))]
            if m:
                print('  %-34s %-18s %d  %s' % (name, label, len(m), str(m[:3])[:60]))

    print('\n=== 6. ДЛИННЫЕ ПРЕДЛОЖЕНИЯ (> 60 слов) ===')
    # Резать по всему файлу нельзя: абзац, следующий за точкой и начинающийся
    # с врезки `>`, дефиса списка или строчной буквы, приклеивается к
    # предыдущему, и счётчик выдаёт предложения, которых в тексте нет. Так
    # документ 32 дважды попадал в отчёт ни за что. Сначала абзацы, потом
    # предложения внутри абзаца.
    for name, s in sorted(texts.items()):
        body = re.sub(r'`[^`]*`|\[[^\]]*\]\([^)]*\)|^\|.*$|^#+ .*$', ' ',
                      s, flags=re.M)
        # Пункт списка - отдельная единица: без этого весь список считается
        # одним предложением и любой перечень из десяти пунктов «длинный».
        for para in re.split(r'\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)', body):
            para = ' '.join(para.split())
            if not para:
                continue
            for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z"*])', para):
                w = len(sent.split())
                if w > 60:
                    print('  %-34s %3d слов  %s...' % (name, w, sent[:90]))

    extra_checks(texts)
    print('\nполный отчёт в UTF-8: %s' % os.path.relpath(REPORT, REPO))


if __name__ == '__main__':
    main()
    sys.stdout.flush()
