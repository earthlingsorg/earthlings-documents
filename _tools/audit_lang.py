# -*- coding: utf-8 -*-
"""Машинная вычитка корпуса на любом языке: одна механика, конфигурация на язык.

Заменяет audit_de.py, audit_fr.py, audit_es.py и audit_ka.py, которые были
написаны один из другого копированием. Механика в них совпадала на четыре
пятых, а расходилась тем, что каждая сессия дописывала полезную проверку в
свой файл, и прошлые языки о ней не узнавали: фильтр законного окружения,
появившийся на грузинском, не применялся к испанскому, а испанская проверка
парности перевёрнутых знаков не применялась ни к чему больше. Здесь механика
одна, и новая проверка достаётся всем языкам сразу.

Использование:
    python _tools/audit_lang.py ka
    python _tools/audit_lang.py --all

Конфигурация языка лежит в _tools/audit_conf/<lang>.py. Обязательного в ней
нет ничего: всё, чего язык не объявил, просто не проверяется. Полный список
полей - в _tools/audit_conf/_template.py.

Одиннадцать разделов отчёта:
     1  варианты одного слова          PAIRS
     2  обороты-тики                   TICS, TIC_MIN
     3  расползание терминов           GLOSSARY, COUNT_OVERRIDE
     4  кальки                         CALQUES
     5  механика набора                SPACE_BEFORE_PUNCT
    5+  разделы, своие для языка        EXTRA_SECTIONS
     6  типографика                    ALLOWED, EXTRA_BAD, QUOTES, PAIRED
     7  имя народа не переводится      FORBIDDEN_WORDS
     8  правоспособность               CAPACITY
     9  длинные предложения            LONG_SENT
    10  замки                          HARD_LOCKS, SOFT_LOCKS
    11  цитаты на сверку с актом       QUOTE_SRC
"""
import io, os, re, sys, collections, importlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, '_tools'))

from audit_conf import _helpers as H


class Tee(object):
    """Пишет отчёт в файл UTF-8 и одновременно в консоль.

    Без этого аудит падает на первой же нелатинской букве: консоль Windows
    работает в cp866, и 'ხ' или 'ñ' в неё не кодируются - процесс умирает
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

    def close(self):
        self.f.close()


# Значения по умолчанию. Язык переопределяет только то, что у него иначе.
DEFAULTS = {
    'TITLE': '',
    # Модель словоформы. Их четыре, и это не вкус, а устройство языков корпуса:
    #   'word' - по границе слова: английский, где формы почти не меняются;
    #   'flex' - основа плюс короткое окончание, без учёта регистра: испанский,
    #            французский, немецкий, где pueblo/pueblos надо считать вместе;
    #   'stem' - основа плюс длинное окончание: грузинский и всё, что
    #            агглютинативно, где у одного слова полтора десятка форм;
    #   'sub'  - счёт вхождений подстроки: письменность БЕЗ ПРОБЕЛОВ, где не
    #            работает ни одна из трёх первых. В китайском тексте граница
    #            слова \b не срабатывает нигде (соседний иероглиф - тоже \w),
    #            а окончаний нет вовсе, так что и допуск считать нечего.
    #
    # 'sub' переключает не только счёт: письменность без пробелов ломает ещё
    # три механизма, и все три чинятся здесь же, а не в конфигурации языка -
    # см. sentences(), sec_long() и «повтор слова» в sec_mech(). Каждый из них
    # при пробельной разметке молчит НЕ ошибкой, а пустым результатом, поэтому
    # обойти их в конфигурации нельзя: отчёт сказал бы «чисто».
    'COUNT': 'word',
    'LETTERS': H.LATIN,         # класс букв письма, нужен при COUNT='stem'
    'STEM_EXTRA': 8,            # допуск окончания для 'stem'
    # Приставочные частицы, пишущиеся СЛИТНО с основой. Пусто у всех языков,
    # кроме арабского: там والشعب - это «и» плюс артикль плюс «народ», и
    # граница слова стоит перед служебной буквой, а не перед основой. Без
    # этого поля счёт по основе теряет больше половины вхождений и печатает
    # «чисто» на тексте, где термин расползся. См. H.ARABIC_PROCLITIC.
    'STEM_PREFIX': '',
    'FLEX_EXTRA': 3,            # допуск окончания для 'flex'
    # Считать термины без учёта регистра. Для романских языков - да: слово в
    # начале фразы то же самое. Для немецкого - НЕТ: заглавная буква там
    # различает слова, и «Kollektiv» (существительное) с «kollektiv»
    # (прилагательное) считать вместе значит выдумать расползание на ровном
    # месте - на корпусе это дало 54 вхождения вместо пяти.
    'COUNT_CI': True,
    'PAIRS': [],
    # Пары орфографических вариантов считаются ТОЧНО по границе слова даже
    # там, где термины считаются по основе: пара «este / éste» с допуском
    # окончания склеивает esta, estos, estas и теряет смысл.
    'PAIRS_COUNT': 'exact',     # 'exact' | 'term'
    # На каком тексте искать расползание терминов.
    #   'clean' - без дословных цитат: язык официального ПЕРЕВОДА акта, где
    #             текст акта законно говорит своим словом (грузинский);
    #   'raw'   - на всём: язык АУТЕНТИЧНОГО текста акта, где расхождение
    #             внутри цитаты есть настоящий сигнал (испанский, французский).
    'GLOSSARY_ON': 'clean',
    'PAIRS_TITLE': 'ОРФОГРАФИЧЕСКИЕ ВАРИАНТЫ',
    'TICS': [],
    'TIC_MIN': 10,
    # Считать обороты без учёта регистра. Нужно там, где оборот регулярно
    # открывает предложение с заглавной: французское «En outre», «Par
    # ailleurs». Без этого половина вхождений теряется.
    'TICS_CI': False,
    'GLOSSARY': {},
    # Класс знаков, соседство с которыми НЕ считается границей слова.
    # По умолчанию «буква, цифра, дефис» - годится для латиницы, кириллицы,
    # мхедрули, арабицы и CJK.
    #
    # Деванагари требует своего: матры, вирама и анусвара в Python не входят
    # в \w (это комбинирующие знаки, isalnum() == False), поэтому после
    # каждой матры возникает ложная «граница слова». На хинди-пилоте это
    # дало 20 ложных вхождений слова «фонд» из 20 - все внутри слова
    # «представитель». Проверка при этом молчала: она печатала не ошибку, а
    # правдоподобное число.
    'BOUNDARY': H.DEFAULT_EDGE,
    'COUNT_OVERRIDE': {},       # {вариант: функция(текст) -> число}
    'CALQUES': [],
    'SPACE_BEFORE_PUNCT': ',.',  # знаки, перед которыми пробел - дефект
    'REPEAT_LETTERS': None,      # класс букв для «повтор слова», None - выкл
    'REPEAT_MIN': 3,             # минимальная длина повторяемого слова
    # Слова, законно идущие подряд: немецкое «die die», «das das» в
    # придаточных - норма, а не опечатка.
    'REPEAT_SKIP': (),
    'ALLOWED': set(),            # кодпойнты, законные в этом языке
    'EXTRA_BAD': {},             # кодпойнты, запрещённые дополнительно
    'QUOTES': (H.GUILLEMET_OPEN, H.GUILLEMET_CLOSE),
    'QUOTES_NAME': 'кавычки',
    'SPACE_IN_QUOTES': False,    # во французском пробел внутри - норма
    'PAIRED': [],                # [(знак, парный, подпись)] - испанские ¿ ¡
    'FORBIDDEN_WORDS': [],
    'CAPACITY': [],
    'CAPACITY_TITLE': 'ПРАВОСПОСОБНОСТЬ, ДЕЕСПОСОБНОСТЬ, ПРАВОСУБЪЕКТНОСТЬ',
    'LONG_SENT': 60,
    'SENT_START': None,          # класс знаков, с которых начинается фраза
    # Знаки конца фразы. У письменностей со своей пунктуацией они свои:
    # китайская точка 。 - отдельный знак, и без неё корпус состоит из одного
    # предложения длиной в файл, а проверка длины показывает «чисто».
    'SENT_END': '.!?',
    'HARD_LOCKS': [],
    'SOFT_LOCKS': [],
    'QUOTE_SRC': None,
    'SOURCE_NOTE': 'каждую сверить с текстом акта',
    'EXTRA_SECTIONS': [],        # [(заголовок, функция(ctx))]
}


class Conf(object):
    """Конфигурация языка с подставленными значениями по умолчанию."""

    def __init__(self, lang):
        self.LANG = lang
        mod = importlib.import_module('audit_conf.%s' % lang)
        self._mod = mod
        for k, v in DEFAULTS.items():
            setattr(self, k, getattr(mod, k, v))
        # Опечатка в имени поля молча выключает проверку: конфигурация просто
        # не будет прочитана, а отчёт скажет «чисто». Это уже случалось,
        # поэтому здесь ассерт, а не предупреждение. Вспомогательные величины
        # внутри конфигурации пишутся с подчёркивания - тогда они не попадают
        # под проверку и видно, что они не поля.
        unknown = [k for k in dir(mod)
                   if k.isupper() and not k.startswith('_')
                   and k not in DEFAULTS and k != 'LANG'
                   and not isinstance(getattr(mod, k), type(re))]
        assert not unknown, (
            'в audit_conf/%s.py объявлено то, чего механика не знает: %s. '
            'Либо это опечатка в имени поля, либо вспомогательная величина - '
            'тогда назвать её с подчёркивания.'
            % (lang, ', '.join(sorted(unknown))))
        assert self.COUNT in ('word', 'flex', 'stem', 'sub'), (
            'audit_conf/%s.py: COUNT=%r - такой модели словоформы нет'
            % (lang, self.COUNT))
        # На письменности без пробелов счёт «строго по границе слова» не
        # находит НИЧЕГО: слева и справа от термина стоит такой же иероглиф,
        # то есть \w. Раздел 1 напечатал бы «чисто» при любом смешении, и это
        # тот самый молчаливый провал, ради которого здесь ассерты.
        assert not (self.COUNT == 'sub' and self.PAIRS_COUNT == 'exact'
                    and self.PAIRS), (
            "audit_conf/%s.py: при COUNT='sub' нужен PAIRS_COUNT='term'. "
            "Счёт по границе слова на письменности без пробелов даёт ноль "
            "вхождений всегда, и раздел 1 покажет «чисто» вместо смешения."
            % lang)
        assert not (self.COUNT == 'sub' and self.LETTERS == H.LATIN), (
            "audit_conf/%s.py: при COUNT='sub' поле LETTERS обязано быть "
            "классом своего письма (H.CJK), а не латиницей: от него зависят "
            "длина предложения, начало фразы и повтор слова." % lang)


class Ctx(object):
    """Тексты корпуса в двух видах плюс конфигурация - то, что нужно разделам."""

    def __init__(self, conf, texts):
        self.conf = conf
        self.texts = texts                       # как есть
        self.clean = {n: unquoted(conf, s) for n, s in texts.items()}
        self.allw = ' '.join(texts.values())     # весь корпус как есть
        self.allc = ' '.join(self.clean.values())  # весь корпус без цитат


def load(lang):
    d = os.path.join(REPO, lang)
    assert os.path.isdir(d), d
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith('.md') and f[0].isdigit():
            out[f] = io.open(os.path.join(d, f), encoding='utf-8').read()
    m = os.path.join(REPO, '_manifest', '%s-manifest.md' % lang)
    if os.path.isfile(m):
        out['manifest'] = io.open(m, encoding='utf-8').read()
    assert out, 'нет мастеров в %s - переводить ещё нечего' % d
    assert all(t.strip() for t in out.values()), 'пустой файл на входе'
    return out


def unquoted(conf, s):
    """Текст без дословных цитат из актов, без кода и адресов.

    Цитата воспроизводит слова подлинника, и они бывают не нашими: грузинский
    текст статьи 22 Пакта говорит ასოციაცია там, где термин корпуса -
    გაერთიანება. Править цитату нельзя, а считать её расползанием - ложная
    тревога.
    """
    o, c = conf.QUOTES
    s = re.sub(re.escape(o) + r'[^' + re.escape(c) + r']*' + re.escape(c), ' ', s)
    s = re.sub(r'`[^`]*`|\((?:https?|mailto):[^)]*\)|\bhttps?://\S+', ' ', s)
    return s


# Латинская вставка внутри текста без пробелов: адрес, имя, номер контракта,
# DAO, SBT. Перед счётом подстроки она заменяется ПРОБЕЛОМ, а не удаляется.
# Удалять нельзя: между «参与» и «治理» стоит DAO, и после удаления получилась
# бы последовательность «参与治理», которой в тексте нет, - счёт подстроки
# нашёл бы её как настоящую и показал расползание термина на ровном месте.
_LATIN_RUN = re.compile(r'[0-9A-Za-z][0-9A-Za-z._%+\-/:@]*')


def nospace_text(text):
    """Текст письменности без пробелов, очищенный от латинских вставок."""
    return _LATIN_RUN.sub(' ', text)


def counter(conf):
    """Функция счёта по модели словоформы языка - см. поле COUNT."""
    def n(text, w):
        f = conf.COUNT_OVERRIDE.get(w)
        if f:
            return f(text)
        # Письменность без пробелов проверяется ПЕРВОЙ, до ветки с цифрой:
        # в «第22条» цифра есть, но границы слова вокруг нет и не будет, и
        # счёт по границе дал бы ноль при любом числе вхождений.
        if conf.COUNT == 'sub':
            w = w.strip()
            # Латинский термин (DAO, SBT, Earthlings) считаем по границе
            # ЛАТИНСКОГО слова и на исходном тексте. Не подстрокой - иначе он
            # находился бы внутри других латинских слов; и не обычным word() -
            # тот берёт границу как «не \w», а соседний иероглиф это тоже \w,
            # так что в 参与DAO治理 он не нашёл бы ничего. См. H.ascii_word.
            if w.isascii():
                return len(re.findall(H.ascii_word(w), text))
            return nospace_text(text).count(w)
        # Написанное с цифрой считаем по границе слова при любой модели:
        # у «22-бис» нет окончания, и допуск ловит 122-бис.
        if conf.COUNT == 'word' or re.search(r'[0-9]', w):
            return len(re.findall(H.word(w, conf.BOUNDARY), text))
        if conf.COUNT == 'stem':
            return len(re.findall(
                H.stem(w, conf.LETTERS, conf.STEM_EXTRA, conf.STEM_PREFIX),
                text))
        # Язык со своей границей считает окончание СВОИМИ буквами, а не \w:
        # у деванагари окончание состоит из комбинирующих знаков, которых в
        # \w нет вовсе, и общая ветка потеряла бы все косвенные формы.
        if conf.BOUNDARY != H.DEFAULT_EDGE:
            return len(re.findall(
                H.flex(w, conf.LETTERS, conf.FLEX_EXTRA, conf.BOUNDARY),
                text, re.I if conf.COUNT_CI else 0))
        return len(re.findall(
            r'(?<![\w-])' + re.escape(w.strip()) +
            r'\w{0,%d}(?![\w-])' % conf.FLEX_EXTRA, text,
            re.I if conf.COUNT_CI else 0))
    return n


def exact(text, w):
    """Счёт строго по границе слова, без допуска окончания."""
    return len(re.findall(H.word(w), text))


def sentences(conf, text):
    """Предложения внутри абзаца, а не через весь файл.

    Резать сразу по всему тексту нельзя: абзац, следующий за точкой и
    начинающийся с врезки, дефиса списка или буквы, приклеивается к
    предыдущему, и счётчик выдаёт несуществующие предложения длиной в
    полстраницы.
    """
    start = conf.SENT_START or (conf.LETTERS + 'A-Z*' + re.escape(conf.QUOTES[0]))
    # После китайской точки 。 пробела нет - он уже внутри ширины глифа.
    # Требовать \s+ на письменности без пробелов значит не найти ни одной
    # границы: весь файл окажется одним предложением, и проверка длины
    # напечатает «чисто» на тексте, где длина не проверена вовсе.
    gap = r'\s*' if conf.COUNT == 'sub' else r'\s+'
    body = re.sub(r'`[^`]*`|\[[^\]]*\]\([^)]*\)|^\|.*$|^#+ .*$', ' ',
                  text, flags=re.M)
    for para in re.split(r'\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)', body):
        para = ' '.join(para.split())
        if not para:
            continue
        for s in re.split(r'(?<=[' + re.escape(conf.SENT_END) + r'])' +
                          gap + r'(?=[' + start + r'])', para):
            yield s


# --------------------------------------------------------------------------
# Разделы отчёта. Каждый берёт Ctx и печатает свой кусок.
# --------------------------------------------------------------------------

def sec_pairs(ctx):
    conf = ctx.conf
    n = counter(conf) if conf.PAIRS_COUNT == 'term' else exact
    print('\n=== 1. %s ===' % conf.PAIRS_TITLE)
    found = 0
    for a, b in conf.PAIRS:
        na, nb = n(ctx.allc, a), n(ctx.allc, b)
        if na and nb:
            found += 1
            wa = sorted(k for k, s in ctx.clean.items() if n(s, a))
            wb = sorted(k for k, s in ctx.clean.items() if n(s, b))
            print('  СМЕШЕНИЕ %-16s %3d %s' % (a.strip(), na, ','.join(wa)[:52]))
            print('           %-16s %3d %s' % (b.strip(), nb, ','.join(wb)[:52]))
    if not found:
        print('  чисто')


def sec_tics(ctx):
    conf = ctx.conf
    hay = ctx.allw.lower() if conf.TICS_CI else ctx.allw
    key = (lambda t: t.lower()) if conf.TICS_CI else (lambda t: t)
    print('\n=== 2. ОБОРОТЫ-ТИКИ (>= %d вхождений) ===' % conf.TIC_MIN)
    shown = 0
    for t in sorted(conf.TICS, key=lambda x: -hay.count(key(x))):
        c = hay.count(key(t))
        if c >= conf.TIC_MIN:
            inf = sum(1 for s in ctx.texts.values()
                      if key(t) in (s.lower() if conf.TICS_CI else s))
            print('  %4d x  "%s"  (файлов: %d)' % (c, t, inf))
            shown += 1
    if not shown:
        print('  чисто')


def sec_glossary(ctx):
    """Расползание считаем по ОЧИЩЕННОМУ тексту.

    Цитата из акта, употребившая своё слово, расползанием не является:
    править её нельзя, и печатать её каждый прогон значит приучить не читать
    этот раздел.
    """
    n = counter(ctx.conf)
    where = ctx.allc if ctx.conf.GLOSSARY_ON == 'clean' else ctx.allw
    sub = ctx.conf.COUNT == 'sub'
    print('\n=== 3. РАСПОЛЗАНИЕ ТЕРМИНОВ ===')
    drift = 0
    for ru, variants in sorted(ctx.conf.GLOSSARY.items()):
        used = [(v, n(where, v)) for v in variants]
        # Счёт подстроки находит короткий вариант внутри длинного: 无效 сидит
        # внутри 自始无效, 权利 внутри 权利能力. Без поправки норма корпуса и её
        # конкурент показывают одинаковое число, и раздел печатает расползание
        # там, где написано ровно одно слово. Вычитаем вхождения тех вариантов
        # той же группы, которые содержат данный как часть себя.
        if sub:
            counts = dict(used)
            used = [(v, c - sum(counts.get(o, 0) for o in counts
                                if o != v and v in o))
                    for v, c in used]
        used = [(v, c) for v, c in used if c > 0]
        if len(used) > 1:
            drift += 1
            print('  %-24s %s'
                  % (ru, '  |  '.join('%s=%d' % (v, c) for v, c in used)))
    if not drift:
        print('  чисто')


def sec_calques(ctx):
    print('\n=== 4. КАЛЬКИ ===')
    found = 0
    for pat, fix in ctx.conf.CALQUES:
        hits = [(k, len(re.findall(pat, s))) for k, s in ctx.texts.items()]
        hits = [(k, c) for k, c in hits if c]
        if hits:
            found += 1
            print('  %-36s %3d  -> %s'
                  % (pat[:36], sum(c for _, c in hits), fix))
            print('        %s'
                  % ', '.join('%s:%d' % (k, c) for k, c in hits)[:110])
    if not found:
        print('  чисто')


def sec_mech(ctx):
    conf = ctx.conf
    print('\n=== 5. МЕХАНИКА ===')
    # Двойной пробел - дефект набора, КРОМЕ пустой ячейки таблицы: строка
    # `|  | Общественное движение | Народ |` в документе 02 набрана так на
    # всех восьми языках, и это разметка, а не опечатка. Без исключения
    # раздел печатал одну и ту же ложную строку в каждом отчёте.
    checks = [('двойной пробел', r'(?<!\|)[^\n|] {2,}[^\n|]')]
    if conf.SPACE_BEFORE_PUNCT:
        checks.append(('пробел перед знаком',
                       r' [' + re.escape(conf.SPACE_BEFORE_PUNCT) + r'](?:\s|$)'))
    if conf.REPEAT_LETTERS:
        if conf.COUNT == 'sub':
            # Без пробелов повтор стоит вплотную (的的), а границы слова нет
            # ни слева, ни справа: соседний иероглиф - тоже \w, и проверка с
            # (?<![\w-]) не сработала бы ни разу.
            checks.append(('повтор слова',
                           r'([' + conf.REPEAT_LETTERS +
                           r']{%d,})\1' % conf.REPEAT_MIN))
        else:
            checks.append(('повтор слова',
                           r'(?<![\w-])([' + conf.REPEAT_LETTERS +
                           r']{%d,}) \1(?![\w-])' % conf.REPEAT_MIN))
    skip = set(w.lower() for w in conf.REPEAT_SKIP)
    found = 0
    for name, s in sorted(ctx.texts.items()):
        for label, pat in checks:
            m = re.findall(pat, s)
            if label == 'повтор слова' and skip:
                m = [x for x in m if x.lower() not in skip]
            if m:
                found += 1
                print('  %-30s %-24s %d  %s'
                      % (name[:30], label, len(m), str(m[:3])[:56]))
    if not found:
        print('  чисто')


def sec_typo(ctx):
    conf = ctx.conf
    bad = dict(H.BAD_CHARS)
    for cp in conf.ALLOWED:
        bad.pop(cp, None)
    bad.update(conf.EXTRA_BAD)
    print('\n=== 6. ТИПОГРАФИКА ===')
    hits = collections.Counter()
    for name, s in sorted(ctx.texts.items()):
        for ch in s:
            if ord(ch) in bad:
                hits['%s: %s' % (name[:24], bad[ord(ch)])] += 1
    if hits:
        for k, v in sorted(hits.items()):
            print('  %-52s %d' % (k, v))
    else:
        print('  чисто')
    o, c = conf.QUOTES
    a, b = ctx.allw.count(o), ctx.allw.count(c)
    print('  %s: открывающих %d, закрывающих %d%s'
          % (conf.QUOTES_NAME, a, b, '' if a == b else '   <-- НЕ СОВПАДАЕТ'))
    # Пробел внутри кавычек: во французском он ОБЯЗАТЕЛЕН, в испанском,
    # немецком и грузинском - дефект. Проверка одна, но перевёрнутая, и
    # перепутать её значит объявить норму языка ошибкой.
    if o == c:
        # Кавычки симметричны (английские прямые ASCII): какая из них
        # открывающая, из знака не видно, и проверка «пробел внутри» меряет
        # пробел после ЗАКРЫВАЮЩЕЙ, то есть норму. У английского она давала
        # 416 ложных строк - отчёт с такой строкой перестают читать.
        print('  пробел внутри не проверяется: кавычки симметричны')
    elif conf.SPACE_IN_QUOTES:
        tight = (len(re.findall(re.escape(o) + r'\S', ctx.allw)) +
                 len(re.findall(r'\S' + re.escape(c), ctx.allw)))
        print('  кавычек БЕЗ пробела внутри: %d%s'
              % (tight, '' if not tight else '   <-- проверить'))
    else:
        loose = (len(re.findall(re.escape(o) + r' ', ctx.allw)) +
                 len(re.findall(r' ' + re.escape(c), ctx.allw)))
        print('  кавычек с пробелом внутри: %d%s'
              % (loose, '' if not loose else '   <-- убрать'))
    # Парность знаков, которые обязаны идти вдвоём: испанские ¿ и ¡.
    # Считаем по тексту без адресов: '?' в 'safe.global/home?safe=' не
    # вопросительный знак и пары не требует.
    for inv, direct, label in conf.PAIRED:
        for name, s in sorted(ctx.clean.items()):
            x, y = s.count(inv), s.count(direct)
            if x != y:
                print('  %-26s %s: %s=%d, %s=%d   <-- НЕ СОВПАДАЕТ'
                      % (name[:26], label, inv, x, direct, y))
        print('  всего %s: %s=%d, %s=%d'
              % (label, inv, ctx.allc.count(inv), direct, ctx.allc.count(direct)))


def sec_name(ctx):
    print('\n=== 7. ИМЯ НАРОДА НЕ ПЕРЕВОДИТСЯ ===')
    hits = [(k, m.group(0)) for k, s in sorted(ctx.texts.items())
            for pat in ctx.conf.FORBIDDEN_WORDS for m in re.finditer(pat, s)]
    print('  ' + (str(hits)[:400] if hits
                  else 'чисто (везде Earthlings и earthling латиницей)'))


def sec_capacity(ctx):
    n = counter(ctx.conf)
    print('\n=== 8. %s ===' % ctx.conf.CAPACITY_TITLE)
    for w in ctx.conf.CAPACITY:
        where = [k for k, s in sorted(ctx.texts.items()) if n(s, w)]
        if where:
            print('  %-24s %3d раз  %s'
                  % (w, n(ctx.allw, w), ','.join(where)[:60]))


def sec_long(ctx):
    conf = ctx.conf
    # На письменности без пробелов длину меряем знаками своего письма, а не
    # split(): там весь абзац - одно «слово», и порог не срабатывает никогда.
    # Единицу печатаем в заголовке: молчаливая смена меры уже дороже, чем
    # лишнее слово в отчёте.
    nospace = conf.COUNT == 'sub'
    unit = 'знаков' if nospace else 'слов'
    letters = re.compile('[' + conf.LETTERS + ']')
    print('\n=== 9. ДЛИННЫЕ ПРЕДЛОЖЕНИЯ (> %d %s) ===' % (conf.LONG_SENT, unit))
    found = 0
    for name, s in sorted(ctx.texts.items()):
        for sent in sentences(conf, s):
            w = len(letters.findall(sent)) if nospace else len(sent.split())
            if w > conf.LONG_SENT:
                found += 1
                print('  %-28s %3d %s  %s...' % (name[:28], w, unit, sent[:80]))
    if not found:
        print('  чисто')


def sec_locks(ctx):
    """Замки словаря решений: то, чего нельзя написать ни при каких условиях.

    HARD - законного вхождения не бывает. SOFT - бывает, и тогда третьим
    элементом идёт регулярное выражение законного окружения: если оно есть
    в 60 знаках вокруг находки, находка не печатается. Без этого фильтра
    отчёт состоит из ложных строк, а отчёт, в котором каждая строка ложная,
    перестают читать на второй сессии.
    """
    print('\n=== 10. ЗАМКИ ===')
    hard = 0
    for pat, why in ctx.conf.HARD_LOCKS:
        for name, s in sorted(ctx.texts.items()):
            for m in re.finditer(pat, s):
                hard += 1
                c = ' '.join(s[max(0, m.start() - 45):m.end() + 45].split())
                print('  ДЕФЕКТ %-20s %-22s %s'
                      % (m.group(0)[:20], name[:22], c[:76]))
                print('         %s' % why)
    if not hard:
        print('  жёсткие замки: чисто')
    soft, skipped = collections.Counter(), 0
    for lock in ctx.conf.SOFT_LOCKS:
        pat, why = lock[0], lock[1]
        excuse = lock[2] if len(lock) > 2 else None
        for name, s in sorted(ctx.texts.items()):
            for m in re.finditer(pat, s):
                if excuse and re.search(
                        excuse, s[max(0, m.start() - 60):m.end() + 60]):
                    skipped += 1
                    continue
                soft[(m.group(0), name, why)] += 1
    print('  снято по законному окружению: %d' % skipped)
    if soft:
        print('  на ручной разбор (законно только о государстве, не о нас):')
        for (w, name, why), c in sorted(soft.items()):
            print('    %-20s %-22s %2d  %s' % (w[:20], name[:22], c, why[:56]))
    else:
        print('  мягкие замки: чисто')


def sec_quotes(ctx):
    conf = ctx.conf
    if not conf.QUOTE_SRC:
        return
    print('\n=== 11. ЦИТАТЫ, КОТОРЫЕ НАДО СВЕРЯТЬ С АКТОМ ===')
    o = conf.QUOTES[0]
    q = 0
    for name, s in sorted(ctx.texts.items()):
        for para in re.split(r'\n\s*\n', s):
            if re.search(conf.QUOTE_SRC, para) and o in para:
                q += 1
                print('  %-24s %s...' % (name[:24], ' '.join(para.split())[:104]))
    print('  всего: %d - %s' % (q, conf.SOURCE_NOTE))


SECTIONS = [sec_pairs, sec_tics, sec_glossary, sec_calques, sec_mech]
TAIL = [sec_typo, sec_name, sec_capacity, sec_long, sec_locks, sec_quotes]


def audit(lang):
    conf = Conf(lang)
    ctx = Ctx(conf, load(lang))
    print('язык: %s%s   файлов: %d, слов: %d'
          % (lang, (' (%s)' % conf.TITLE) if conf.TITLE else '',
             len(ctx.texts), len(ctx.allw.split())))
    for fn in SECTIONS:
        fn(ctx)
    for title, fn in conf.EXTRA_SECTIONS:
        print('\n=== %s ===' % title)
        fn(ctx)
    for fn in TAIL:
        fn(ctx)
    return ctx


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--all' in sys.argv:
        here = os.path.join(REPO, '_tools', 'audit_conf')
        langs = sorted(f[:-3] for f in os.listdir(here)
                       if f.endswith('.py') and not f.startswith('_'))
    else:
        langs = args or ['ka']
    for lang in langs:
        report = os.path.join(REPO, '_tools', 'audit-report-%s.txt' % lang)
        console, sys.stdout = sys.stdout, Tee(report, sys.stdout)
        try:
            audit(lang)
            print('\nполный отчёт в UTF-8: %s'
                  % os.path.relpath(report, REPO))
        finally:
            sys.stdout.flush()
            sys.stdout.close()
            sys.stdout = console


if __name__ == '__main__':
    main()
