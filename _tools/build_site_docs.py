# -*- coding: utf-8 -*-
"""Сборка живых страниц корпуса earth-lings-site из .md-мастеров.

md2doc.py даёт оформление и разметку текста, но выдаёт самодостаточный файл
без обвязки сайта. Живой документ на сайте несёт сверх этого:
  - title / description / robots / og:* / twitter:* / canonical / JSON-LD
  - hreflang на девять языков + x-default
  - навигацию «предыдущий/следующий документ» в конце страницы
  - счётчик umami

Этот сборщик берёт оформление из md2doc, а обвязку - из живого файла (или из
явно переданных данных, если документа на сайте ещё нет), и пишет готовую
страницу в documents/<lang>/.

CSS не дублируется в каждый файл: правила вынимаются из шаблона md2doc и
пишутся в css/docs-statute.css один раз - стиль остаётся тем же буква в букву.

Использование:
  python build_site_docs.py --css                 только пересобрать CSS
  python build_site_docs.py 05                    один документ
  python build_site_docs.py all                   весь корпус
"""
import io, os, re, sys, html, json, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md2doc

HERE = os.path.dirname(os.path.abspath(__file__))
# Мастера лежат в этом же репозитории, по языкам: ru/NN-slug.md.
REPO = os.path.abspath(os.path.join(HERE, '..'))
MD_DIR = os.path.join(REPO, 'ru')
# Репозиторий сайта. По умолчанию - соседняя папка рядом с этой: клонировали
# оба репозитория рядом, и всё работает. Переопределяется переменной окружения,
# если они лежат врозь. Захардкоженный путь одной машины в публичном
# репозитории делал скрипт неработающим у всех, кроме одного человека.
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
DOCS = os.path.join(SITE, 'documents', 'ru')
CSS_PATH = os.path.join(SITE, 'css', 'docs-statute.css')
ORIGIN = 'https://earth-lings.org'

assert os.path.isdir(MD_DIR), MD_DIR
assert os.path.isdir(DOCS), (
    'не найден репозиторий сайта: %s\n'
    'Ожидается earth-lings-site рядом с этим репозиторием. Если он лежит в '
    'другом месте - EARTHLINGS_SITE=/путь/к/earth-lings-site' % DOCS)


# Язык - параметр сборки, а не константа. Мастера лежат в <repo>/<lang>/,
# готовые страницы - в <site>/documents/<lang>/. Русский остаётся значением по
# умолчанию у каждой функции: так добавление языка не может изменить того, что
# собиралось раньше.
def md_dir(lang='ru'):
    return os.path.join(REPO, lang)


def docs_dir(lang='ru'):
    return os.path.join(SITE, 'documents', lang)

# Номер документа -> имя мастера. Отдельный список имён не нужен: имя
# выводится из пары «номер - слаг», заданной ниже в SLUGS, и она же служит
# адресом страницы. Одна таблица вместо двух - расходиться нечему.
def corpus_file(num, lang='ru'):
    return '%s-%s.md' % (num, SLUGS[lang][num])

# Смысловые адреса. Номер остаётся: он переживает переименование документа
# (13 августа документ 31 сменил название, а 14 августа - документ 26, и адрес
# это пережил), слово несёт смысл для человека, получившего ссылку в письме.
# Слаг фиксируется один раз и при переименовании документа НЕ меняется.
# Только строчная латиница, цифры и дефис: кириллица в письме превращается в
# %D0%BF%D1%80 и ссылка перестаёт читаться.
#
# Языки, которых здесь нет, живут на числовых адресах и получат слаги в свой
# синк. Это не забытый хвост, а порядок работ: слаг задаётся вместе с переводом.
SLUGS = {
    'ru': {
        '01': 'deklaraciya',
        '03': 'etika',
        '04': 'pravovoe-obosnovanie',
        '05': 'ustav',
        '07': 'dao',
        '08': 'soty',
        '09': 'kaznachejstvo',
        '10': 'earthlings-coin',
        '11': 'nezavisimyj-sovet',
        '12': 'cifrovaya-platforma',
        '14': 'put-earthling',
        '15': 'sbt-pasport',
        '16': 'biometricheskaya-verifikaciya',
        '17': 'chto-dalshe',
        '19': 'dorozhnaya-karta',
        '20': 'uchreditelnyj-period',
        '22': 'yuridicheskaya-informaciya',
        '23': 'o-nas',
        '26': 'pravovye-vozrazheniya',
        '27': 'chastye-voprosy',
        '28': 'politika-konfidencialnosti',
        '29': 'polzovatelskoe-soglashenie',
        '30': 'subekt-prava',
        '31': 'rabochaya-povestka',
        '32': 'gde-my-sejchas',
    },
    # Английский. Слаги выведены из имён мастеров в en/ и сверены с
    # перелинковкой внутри самих документов: 107 внутренних ссылок, расхождений
    # нет. Придумывать здесь ничего нельзя - ссылки в текстах уже написаны.
    'en': {
        '01': 'declaration',
        '03': 'ethics',
        '04': 'legal-basis',
        '05': 'charter',
        '07': 'dao',
        '08': 'cells',
        '09': 'treasury',
        '10': 'earthlings-coin',
        '11': 'independent-council',
        '12': 'digital-platform',
        '14': 'the-earthling-path',
        '15': 'sbt-passport',
        '16': 'biometric-verification',
        '17': 'what-may-happen-next',
        '19': 'roadmap',
        '20': 'the-founding-period',
        '22': 'legal-information',
        '23': 'about-us',
        '26': 'objections-and-answers',
        '27': 'frequently-asked-questions',
        '28': 'privacy-policy',
        '29': 'terms-of-use',
        '30': 'how-a-subject-of-law-arises',
        '31': 'working-agenda',
        '32': 'where-we-are-now',
    },
}


def doc_file(num, lang='ru'):
    """Имя файла документа: со слагом, если для языка он задан."""
    slug = SLUGS.get(lang, {}).get(num)
    return '%s%s-%s.html' % (lang, num, slug) if slug else '%s%s.html' % (lang, num)


def doc_href(num, lang='ru'):
    return '/documents/%s/%s' % (lang, doc_file(num, lang))


def doc_file_old(num, lang='ru'):
    """Прежнее числовое имя - нужно для переезда и карты редиректов."""
    return '%s%s.html' % (lang, num)


# порядок чтения корпуса = порядок главного меню; на нём строится «Далее»
CHAIN = ['01', '05', '04', '26', '30', '12', '07', '08', '09', '10', '11',
         '14', '15', '16', '03', '27', '19', '20', '32', '17', '31', '23',
         '22', '28', '29']

# Обвязка берётся из живой страницы, но для переименованных и новых
# документов её задаём здесь - иначе пересборка вернёт старые описания.
OVERRIDES = {
    '32': {
        'title': 'Где мы сейчас | Народ Earthlings',
        'og_title': 'Где мы сейчас | Народ Earthlings',
        'description': 'Где мы сейчас: какой код и какие данные Earthlings публикует, '
                       'что закрыто, по какой причине и что любой человек может проверить '
                       'самостоятельно.',
        'og_description': 'Какой код и какие данные Earthlings публикует, что закрыто и '
                          'по какой причине.',
    },
    # Переименован 2026-08-14 из «Правовые возражения и ответы».
    '26': {
        'title': 'Возражения и ответы | Earthlings',
        'og_title': 'Возражения и ответы | Earthlings',
        'description': 'Возражения против конструкции народа Earthlings - о сепаратизме, '
                       'суверенитете, плутократии в DAO, взносе, неизменяемом ядре и праве '
                       'говорить от чьего-либо имени - с ответами и с перечнем того, что мы '
                       'опровергнутым не считаем.',
        'og_description': 'Возражения против конструкции народа Earthlings и ответы на них, '
                          'включая те, что мы опровергнутыми не считаем.',
    },
    # Обвязка оставалась от редакции «Новый народ для новой эпохи» и вдобавок
    # смешивала русское описание с английским. Переписана 2026-08-14.
    '04': {
        'title': 'Правовое обоснование | Earthlings',
        'og_title': 'Правовое обоснование | Earthlings',
        'description': 'Правовое обоснование народа Earthlings: свобода объединения, право '
                       'на самоопределение, признаки народа и открытые вопросы международного '
                       'права - с источниками и с прямым указанием того, что правом пока не '
                       'решено.',
        'og_description': 'Свобода объединения, самоопределение, признаки народа и то, что '
                          'международным правом пока не решено.',
    },
    # Заголовок намеренно длиннее H1: «Частые вопросы» в выдаче ни о чём не
    # говорит. Записано сюда, чтобы предупреждение о расхождении не срабатывало
    # на том, что сделано осознанно.
    '27': {
        'title': 'Ответы на частые вопросы | Earthlings',
        'og_title': 'Ответы на частые вопросы | Earthlings',
        'description': 'Народ Earthlings отвечает на частые вопросы об управлении, экономике, '
                       'идентичности и этике - как устроено, кто контролирует, как защищены '
                       'данные.',
        'og_description': 'Народ Earthlings отвечает на частые вопросы об управлении, '
                          'экономике, идентичности и этике.',
    },
    '17': {
        'title': 'Что может произойти дальше | Earthlings',
        'og_title': 'Что может произойти дальше | Earthlings',
        'description': 'Возможности, которые открыты народу Earthlings сегодня и могут '
                       'открыться при росте: у каждой названо условие и механизм, а рядом - '
                       'то, что может пойти не так.',
        'og_description': 'Возможности, условия и то, что может пойти не так. Не прогноз '
                          'и не обещание - перечень того, что существует.',
    },
}

# Английская обвязка. Заголовки здесь не заданы намеренно: они выводятся из H1
# документа и потому разойтись с ним не могут. Описания - зеркало русских: где
# по-русски стоит содержательное описание, оно переведено; где шаблон - шаблон.
# Сочинять по-английски то, чего нет по-русски, значит завести вторую редакцию
# позиционирования, которую никто не сверял.
_OFFICIAL = '%s - an official document of the Earthlings people.'
OVERRIDES_EN = {
    '01': {'description': _OFFICIAL % 'The Earthlings Declaration of Self-Determination'},
    '03': {'description': _OFFICIAL % 'Earthlings Ethics'},
    '04': {'description':
           'The legal basis of the Earthlings people: freedom of association, the right of '
           'self-determination, the features of a people and the open questions of '
           'international law - with sources, and with a direct statement of what the law '
           'has not yet decided.',
           'og_description':
           'Freedom of association, self-determination, the features of a people, and what '
           'international law has not yet decided.'},
    '05': {'description': _OFFICIAL % 'Earthlings Charter'},
    '07': {'description': _OFFICIAL % 'The Earthlings DAO: principles, architecture and governance'},
    '08': {'description': _OFFICIAL % 'Earthlings Cells - the system of projects and cooperation'},
    '09': {'description': _OFFICIAL % 'The Earthlings Treasury'},
    '10': {'description': _OFFICIAL % 'Earthlings Coin: the full documentation'},
    '11': {'description': _OFFICIAL % 'The Earthlings Independent Council'},
    '12': {'description': _OFFICIAL % 'The Earthlings Digital Platform'},
    '14': {'description': _OFFICIAL % 'The Earthling Path'},
    '15': {'description': _OFFICIAL % 'The earthling SBT passport'},
    '16': {'description': _OFFICIAL % 'The Earthlings Biometric Verification Policy'},
    '17': {'description':
           'The possibilities open to the Earthlings people today and those that may open '
           'with growth: each with its condition and its mechanism named, and beside them '
           'what may go wrong.',
           'og_description':
           'Possibilities, conditions, and what may go wrong. Not a forecast and not a '
           'promise - a list of what exists.'},
    '19': {'description': _OFFICIAL % 'Roadmap of the Transitional Period'},
    '20': {'description':
           'The Earthlings founding period: proposals are accepted on the whole corpus of '
           'twenty-five documents - the Declaration, the Charter and the rest - from '
           '7 September to 6 December 2026, the record on 20 December, the vote on the '
           'Declaration on 3 January 2027. What is open to discussion, what is not up for '
           'discussion, and how to take part.'},
    '22': {'description': _OFFICIAL % 'Legal Information'},
    '23': {'description': _OFFICIAL % 'About Us'},
    '26': {'description':
           'Objections to the construction of the Earthlings people - on separatism, '
           'sovereignty, plutocracy in the DAO, the contribution, the unamendable core and '
           'the right to speak on anyone\'s behalf - with answers, and with a list of what '
           'we do not regard as refuted.',
           'og_description':
           'Objections to the construction of the Earthlings people and the answers to '
           'them, including those we do not regard as refuted.'},
    '27': {'description':
           'The Earthlings people answers frequent questions about governance, the economy, '
           'identity and ethics - how it works, who controls it, how data are protected.',
           'og_description':
           'The Earthlings people answers frequent questions about governance, the economy, '
           'identity and ethics.'},
    '28': {'description': _OFFICIAL % 'Privacy Policy of the Earthlings People'},
    '29': {'description': _OFFICIAL % 'Terms of Use of the Earthlings People'},
    '30': {'description':
           'Theses of the Earthlings people: why international law developed doctrines on '
           'the existence of collective subjects but scarcely worked out their voluntary '
           'constitution - and why that gap does not make the emergence of a people '
           'unlawful.'},
    '31': {'description':
           'The working agenda of the Earthlings people: a specialist examination of one '
           'possible model of a future world order through the metaphor of an operating '
           'system. A complement to states, not a replacement.'},
    '32': {'description':
           'Where we are now: what code and what data Earthlings publishes, what is closed, '
           'for what reason, and what anyone can check for themselves.',
           'og_description':
           'What code and what data Earthlings publishes, what is closed and for what '
           'reason.'},
}

# Обвязка своя у каждого языка: описание страницы - это текст, а не настройка.
OVERRIDES_BY_LANG = {'ru': OVERRIDES, 'en': OVERRIDES_EN}

# Можно ли переносить обвязку с уже лежащей на сайте страницы. Можно, только
# если она - прежняя сборка того же текста. Английские страницы остались от
# вытесненного перевода, поэтому для них - нет.
WRAPPER_FROM_PAGE = {'ru': True, 'en': False}


def overrides(lang='ru'):
    return OVERRIDES_BY_LANG.get(lang, {})


# Документы, которым нужен свой лист стилей сверх общего.
EXTRA_CSS_BY_DOC = {'31': ['docs-agenda.css']}

# Блоки, которые не выражаются в markdown (схемы): лежат отдельными файлами
# и подставляются в тело по маркеру [[BLOCK-имя]], оставленному в .md.
FRAG_DIR = os.path.join(HERE, 'fragments')


def load_fragments(num, lang='ru'):
    if not os.path.isdir(FRAG_DIR):
        return {}
    out = {}
    for f in sorted(os.listdir(FRAG_DIR)):
        m = re.match(r'%s%s-(.+)\.html$' % (lang, num), f)
        if m:
            out['[[BLOCK-%s]]' % m.group(1)] = io.open(
                os.path.join(FRAG_DIR, f), encoding='utf-8').read().strip()
    return out


# языки, на которых документ существует (для hreflang)
ALL_LANGS = ['ar', 'de', 'en', 'es', 'fr', 'hi', 'ka', 'ru', 'zh']
# 17 и 20 были только по-русски; английские мастера появились 2026-08-15.
LANGS_BY_DOC = {'17': ['en', 'ru'], '20': ['en', 'ru'], '32': ['en', 'ru']}

# Строки интерфейса страницы. Их немного, и держать их здесь честнее, чем
# городить локализацию: язык, которого тут нет, соберётся с русскими словами
# в оглавлении и навигации, и это будет видно сразу.
UI = {
    'ru': {
        'toc': 'Содержание',
        'prev': '← Назад',
        'next': 'Далее →',
        'nav_aria': 'Навигация по документам',
        'all_docs': 'Все документы',
    },
    'en': {
        'toc': 'Contents',
        'prev': '← Back',
        'next': 'Next →',
        'nav_aria': 'Document navigation',
        'all_docs': 'All documents',
    },
}


def ui(lang, key):
    assert lang in UI, (
        'нет строк интерфейса для языка %r: добавьте его в UI, иначе страница '
        'соберётся с русскими словами в оглавлении и навигации' % lang)
    return UI[lang][key]

# ---------------------------------------------------------------- CSS

EXTRA_CSS = u"""
/* ------------------------------------------------ подзаголовок документа */
.doc-subtitle {
  margin: 1.5rem auto 0; max-width: 34em; color: var(--ink-soft);
  font-size: clamp(1.02rem,2.2vw,1.18rem); line-height: 1.5; font-style: italic;
}
.doc-subtitle strong { color: var(--ink-soft); font-weight: 400; }

/* ------------------------------------------------ навигация по корпусу
   Ссылки на соседние документы и на библиотеку остаются в разметке: меню
   рисует скрипт, и без этого блока страница не имеет ни одной ссылки,
   которую увидит поисковик без JS. Человеку блок не показываем - по
   корпусу он ходит через меню. */
.seo-prev-next {
  display: none; gap: 12px; align-items: stretch; max-width: 1040px;
  margin: 0 auto; padding: 28px clamp(20px,5vw,40px) 56px;
  font-family: var(--serif); font-size: 15px;
}
.seo-prev-next a {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 14px 20px; border: 1px solid var(--rule); border-radius: 4px;
  color: var(--navy); text-decoration: none; background: var(--ivory);
  transition: border-color .15s, background .15s;
}
.seo-prev-next a:hover { border-color: var(--gold); background: #fff; }
.seo-prev-next .pn-side { flex: 1; display: block; }
.seo-prev-next .pn-next { text-align: right; }
.seo-prev-next .pn-label {
  display: block; font-family: var(--mono); font-size: 11px;
  letter-spacing: .18em; text-transform: uppercase; color: var(--gold);
  margin-bottom: 5px;
}
.seo-prev-next .pn-name { display: block; font-weight: 600; color: var(--navy); }
@media (max-width: 600px) {
  .seo-prev-next { flex-wrap: wrap; }
  .seo-prev-next .pn-side { flex: 1 1 100%; }
}
"""


ROOT = 'statute'          # класс обёртки документа


def scope_css(css, root=ROOT):
    """Ограничить правила областью документа.

    Тот же лист стилей подключён на всём сайте: встроенный просмотрщик
    выбрасывает <head> документа и вставляет его тело в общую страницу, так
    что стили обязаны приезжать заранее. Без ограничения области правила для
    body, p, ul переопределили бы оформление всего сайта.
    """
    out, i = [], 0
    while i < len(css):
        # блок @media (и любой другой @-блок с вложенными правилами)
        m = re.compile(r'@[\w-]+[^{]*\{').search(css, i)
        n = re.compile(r'([^{}@]+)\{([^{}]*)\}').search(css, i)
        if m and (not n or m.start() < n.start()):
            depth, j = 1, m.end()
            while depth:
                ch = css[j]
                depth += 1 if ch == '{' else (-1 if ch == '}' else 0)
                j += 1
            out.append(css[i:m.start()])
            out.append(m.group(0))
            out.append(scope_css(css[m.end():j - 1], root))
            out.append('}')
            i = j
            continue
        if not n:
            out.append(css[i:])
            break
        out.append(css[i:n.start()])
        sels = []
        for sel in n.group(1).split(','):
            s = sel.strip()
            if not s:
                continue
            if s in (':root', 'html', 'body'):
                sels.append('.%s' % root)
            elif s == '*':
                sels.append('.%s, .%s *' % (root, root))
            elif s.startswith('.%s' % root):
                sels.append(s)
            else:
                sels.append('.%s %s' % (root, s))
        out.append('%s{%s}' % (', '.join(sels), n.group(2)))
        i = n.end()
    return ''.join(out)


def build_css():
    """Правила из шаблона md2doc + добавки сборщика в один внешний файл."""
    m = re.search(r'<style>(.*?)</style>', md2doc.TEMPLATE, re.S)
    assert m, 'в шаблоне md2doc не найден блок <style>'
    css = m.group(1).replace('{{', '{').replace('}}', '}')
    assert '--page:' in css and '.toc-item' in css, 'CSS извлечён неполностью'
    head = ('/* Оформление корпуса документов. Источник - шаблон\n'
            '   Продвижение/12_Документы_ФИНАЛ/_tools/md2doc.py: правила вынесены\n'
            '   из него один в один, чтобы страница на сайте и файл, собранный\n'
            '   скриптом напрямую, выглядели одинаково. Править здесь руками\n'
            '   нечего - изменения вносятся в md2doc.py и пересобираются.\n'
            '   Все правила ограничены областью .%s: тот же лист подключён на\n'
            '   всём сайте ради встроенного просмотрщика документов. */\n' % ROOT)
    body_rule = ('body.%s{margin:0;background:#ece5d6}\n'
                 '.%s{background:#ece5d6}\n' % (ROOT, ROOT))
    out = head + body_rule + scope_css(css.strip()) + '\n' + scope_css(EXTRA_CSS)
    io.open(CSS_PATH, 'w', encoding='utf-8', newline='\n').write(out)
    return len(out)


# ---------------------------------------------------------------- обвязка

def read_wrapper(num, lang='ru'):
    """Достать из живого документа то, что нельзя потерять при пересборке."""
    # Но только там, где прежняя страница - предыдущая сборка ТОГО ЖЕ текста.
    # Английские страницы на сайте остались от прежнего, вытесненного перевода:
    # у них другие заголовки («Legal Justification» вместо «Legal Basis») и
    # описания прежней редакции. Переносить такую обвязку - значит опубликовать
    # новый текст под старым именем. Берём её из OVERRIDES, а заголовок - из H1.
    if not WRAPPER_FROM_PAGE.get(lang, True):
        return dict(overrides(lang).get(num, {})) or None
    # На переезде со числовых адресов на смысловые нового файла ещё нет,
    # а обвязку терять нельзя - читаем прежний.
    p = os.path.join(docs_dir(lang), doc_file(num, lang))
    if not os.path.isfile(p):
        p = os.path.join(docs_dir(lang), doc_file_old(num, lang))
    w = {}
    if os.path.isfile(p):
        s = io.open(p, encoding='utf-8').read()

        def meta(pat):
            m = re.search(pat, s)
            return html.unescape(m.group(1)) if m else None

        w = {
            'title': meta(r'<title>([^<]*)</title>'),
            'description': meta(r'<meta name="description" content="([^"]*)"'),
            'og_description': meta(r'<meta property="og:description" content="([^"]*)"'),
            'og_title': meta(r'<meta property="og:title" content="([^"]*)"'),
        }
    w.update(overrides(lang).get(num, {}))
    return w or None


def head_html(num, doc_title, w, lang='ru'):
    """Шапка страницы: заголовки, описания, канонический адрес, JSON-LD, hreflang."""
    url = ORIGIN + doc_href(num, lang)
    title = w['title'] if w and w.get('title') else '%s | Earthlings' % doc_title
    # Обвязка переносится с прежней сборки, поэтому переименование документа в
    # неё молча не попадает: так ru26 полгода отдавал в <title> старое имя, а
    # ru04 - название редакции, которой давно нет. Ругаемся вслух; лечится
    # записью в OVERRIDES.
    if num not in overrides(lang) and not title.startswith(doc_title):
        sys.stderr.write(
            'ВНИМАНИЕ %s%s: <title> "%s" не совпадает с заголовком документа "%s". '
            'Обвязка осталась от прежней редакции - добавить запись в OVERRIDES.\n'
            % (lang, num, title, doc_title))
    desc = (w or {}).get('description') or ''
    og_desc = (w or {}).get('og_description') or desc
    og_title = (w or {}).get('og_title') or title
    esc = lambda x: html.escape(x or '', quote=True)

    ld = {
        '@context': 'https://schema.org', '@type': 'Article',
        'headline': doc_title,
        'author': {'@type': 'Organization', 'name': 'Earthlings', 'url': ORIGIN},
        'publisher': {'@type': 'Organization', 'name': 'Earthlings',
                      'logo': {'@type': 'ImageObject', 'url': ORIGIN + '/images/logo.png'}},
        'mainEntityOfPage': url,
        'image': ORIGIN + '/images/og-image.jpg',
    }

    langs = LANGS_BY_DOC.get(num, ALL_LANGS)
    alts = ''.join(
        '<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, ORIGIN, doc_href(num, l))
        for l in langs)
    xdef = 'en' if 'en' in langs else langs[0]
    alts += ('<link rel="alternate" hreflang="x-default" href="%s%s">\n'
             % (ORIGIN, doc_href(num, xdef)))

    parts = [
        '<!DOCTYPE html>', '<html lang="%s">' % lang, '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % esc(title),
        '<meta name="description" content="%s">' % esc(desc),
        '<link rel="stylesheet" href="/css/docs-statute.css?v=1">',
        # Шапка сайта - fixed, поэтому текст ушёл бы под неё: отступ сверху
        # равен её высоте плюс два сантиметра воздуха. overflow-x гасит
        # горизонтальную полосу: подвал растянут приёмом margin:0 -50vw, а
        # 100vw шире содержимого на ширину вертикального скроллбара.
        "<style>body{margin:0;background:#ece5d6;overflow-x:clip}"
        ".statute{padding-top:calc(var(--header-height,64px) + 76px)}</style>",
        SHELL_ASSETS,
    ] + [
        '<link rel="stylesheet" href="/css/%s?v=1">' % css for css in EXTRA_CSS_BY_DOC.get(num, [])
    ] + [
        '<meta name="robots" content="index, follow">',
        '<meta property="og:type" content="article">',
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % esc(og_title),
        '<meta property="og:description" content="%s">' % esc(og_desc),
        '<meta property="og:image" content="%s/images/og-image.jpg">' % ORIGIN,
        '<meta property="og:site_name" content="Earthlings">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % esc(og_title),
        '<meta name="twitter:image" content="%s/images/og-image.jpg">' % ORIGIN,
        '<link rel="canonical" href="%s">' % url,
        '<script type="application/ld+json">',
        json.dumps(ld, ensure_ascii=False, separators=(',', ':')),
        '</script>',
        alts.rstrip(),
        '</head>',
    ]
    return '\n'.join(parts)


# ---------------------------------------------------------------- оболочка

# Документ - самостоятельная страница, и открывается он теперь обычным
# переходом, а не поверх главной. Значит шапку с меню и переключателем языка
# страница обязана нести сама, иначе из документа некуда идти.
SHELL_ASSETS = '\n'.join([
    '<link rel="stylesheet" href="/css/fonts-ui.css?v=1">',
    '<link rel="stylesheet" href="/css/modern/critical.css?v=21">',
    '<link rel="stylesheet" href="/css/modern/components.css?v=56">',
    '<link rel="stylesheet" href="/css/modern/content.css?v=37">',
])

SHELL_TAGS = '\n'.join([
    '<earth-header id="main-header">',
    '<earth-navigation id="main-nav" slot="navigation"></earth-navigation>',
    '<earth-mobile-menu-toggle id="mobile-toggle" slot="mobile-toggle"></earth-mobile-menu-toggle>',
    '</earth-header>',
    '<earth-side-menu id="side-menu"></earth-side-menu>',
])

# Переключатель языка в шапке меняет тексты интерфейса, но не адрес. На
# странице документа это бессмысленно: нужен тот же документ на другом языке.
# Если на выбранном языке документа нет - ведём в библиотеку этого языка.
LANG_SWITCH = """<script>
var SLUG = %s;
/* Страница документа сама объявляет свой язык. Приложение берёт язык из
   localStorage и без этой строки навязало бы прошлый выбор: немецкий
   документ открывался бы с русским меню. */
(function () {
  var l = document.documentElement.lang;
  if (l) try { localStorage.setItem('earthlings-language', l); } catch (e) {}
})();
document.addEventListener('language-changed', function (e) {
  var lang = e.detail && e.detail.language;
  if (!lang) return;
  /* Хвост со слагом необязателен: языки переезжают на смысловые адреса по
     одному, и русский документ уже лежит по ru01-deklaraciya.html, а немецкий
     пока по de01.html. Слаги этого документа по языкам - в SLUG ниже; языка
     там нет - значит адрес числовой. */
  var m = location.pathname.match(/\\/documents\\/[a-z]{2}\\/[a-z]{2}(\\d\\d)(?:-[a-z0-9-]+)?\\.html$/);
  if (!m) return;
  var have = (document.body.dataset.langs || '').split(',');
  var url;
  if (have.indexOf(lang) >= 0) {
    var s = SLUG[lang];
    url = '/documents/' + lang + '/' + lang + m[1] + (s ? '-' + s : '') + '.html';
  } else {
    url = '/documents/' + lang + '/index.html';
  }
  if (url !== location.pathname) location.assign(url);
});
</script>
<script type="module" src="/js/modern/main.js?v=84"></script>"""

UMAMI = ('<!--umami-start--><script>if(window.self===window.top){var s=document.createElement("script");'
         's.defer=true;s.src="https://stats.earth-lings.org/script.js";'
         's.setAttribute("data-website-id","badb2091-1880-4933-bf4e-8d7be1f7ce44");'
         'document.body.appendChild(s);}</script><!--umami-end-->')

HOME_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true"><path d="M3 11.5L12 3l9 8.5"/><path d="M5 10v10h5v-6h4v6h5V10"/></svg>')


def prev_next_html(num, titles, lang='ru'):
    """Ссылки на соседние документы корпуса в порядке чтения."""
    if num not in CHAIN:
        return ''
    i = CHAIN.index(num)
    prev = CHAIN[i - 1] if i > 0 else None
    nxt = CHAIN[i + 1] if i < len(CHAIN) - 1 else None
    out = ['<!--seo-prev-next-start-->',
           '<nav class="seo-prev-next" aria-label="%s">' % ui(lang, 'nav_aria')]
    if prev:
        out.append('<a class="pn-side" href="%s" rel="prev">'
                   '<span class="pn-label">%s</span>'
                   '<span class="pn-name">%s</span></a>'
                   % (doc_href(prev, lang), ui(lang, 'prev'), html.escape(titles[prev])))
    else:
        out.append('<span class="pn-side"></span>')
    out.append('<a href="/documents/%s/index.html" rel="up" aria-label="%s" '
               'title="%s">%s</a>'
               % (lang, ui(lang, 'all_docs'), ui(lang, 'all_docs'), HOME_SVG))
    if nxt:
        out.append('<a class="pn-side pn-next" href="%s" rel="next">'
                   '<span class="pn-label">%s</span>'
                   '<span class="pn-name">%s</span></a>'
                   % (doc_href(nxt, lang), ui(lang, 'next'), html.escape(titles[nxt])))
    else:
        out.append('<span class="pn-side"></span>')
    out.append('</nav>')
    out.append('<!--seo-prev-next-end-->')
    return '\n'.join(out)


# ---------------------------------------------------------------- тело

SUBTITLE_RE = re.compile(r'^\*\*(.+)\*\*$')


def pop_subtitle(doc):
    """Первая строка после H1, набранная жирным, - это подзаголовок документа.

    В md2doc такого понятия нет, она стала бы обычным абзацем. Забираем её из
    вступления и рисуем под заголовком, как на прежних страницах сайта.
    """
    lead = doc['lead']
    if not lead:
        return ''
    kind, val = lead[0]
    if kind != 'p' or len(val) != 1:
        return ''
    m = SUBTITLE_RE.match(val[0].strip())
    if not m:
        return ''
    doc['lead'] = lead[1:]
    return md2doc.inline(m.group(1))


def build_doc(num, md_path, titles, fragments=None, lang='ru'):
    md = io.open(md_path, encoding='utf-8').read()
    assert md.strip(), 'пустой исходник: %s' % md_path
    doc = md2doc.parse(md)
    assert doc['title'], 'не найден заголовок H1: %s' % md_path

    subtitle = pop_subtitle(doc)
    title_html = html.escape(doc['title'])
    head = '<header class="doc-head col"><h1 class="doc-title">%s</h1>' % title_html
    if subtitle:
        head += '<p class="doc-subtitle">%s</p>' % subtitle
    head += '<div class="rule-double"></div></header>'

    n_head = (sum(len(p['articles']) for p in doc['parts'])
              + len([p for p in doc['parts'] if p['label'] or p['title']]))
    toc = ('<nav class="toc col" aria-label="%s">'
           '<h2 class="toc-title">%s</h2>%s'
           '</nav>' % (ui(lang, 'toc'), ui(lang, 'toc'), md2doc.render_toc(doc))
           ) if n_head >= 5 else ''

    body = md2doc.render_body(doc)
    fragments = fragments or load_fragments(num, lang)
    if fragments:
        for marker, frag in fragments.items():
            assert marker in body, 'маркер %s не найден в теле %s' % (marker, num)
            body = body.replace('<p>%s</p>' % marker, frag).replace(marker, frag)

    # Внешняя обёртка нужна и отдельной странице, и встроенному просмотрщику:
    # он вставляет в общую страницу только содержимое body, поэтому класс с
    # body туда не доедет, а с div - доедет.
    # data-langs перечисляет языки, на которых документ существует: по нему
    # переключатель языка решает, вести на тот же документ или в библиотеку.
    page = '\n'.join([
        head_html(num, doc['title'], read_wrapper(num, lang), lang),
        '<body data-langs="%s">' % ','.join(LANGS_BY_DOC.get(num, ALL_LANGS)),
        SHELL_TAGS,
        '<div class="%s">' % ROOT,
        '<div class="sheet">',
        head, toc, body,
        '</div>',
        prev_next_html(num, titles, lang),
        '</div>',
        '<earth-footer id="main-footer"></earth-footer>',
        LANG_SWITCH % json.dumps(
            {l: SLUGS[l][num] for l in SLUGS if num in SLUGS[l]},
            ensure_ascii=True, sort_keys=True, separators=(',', ':')),
        UMAMI,
        '</body>',
        '</html>',
        '',
    ])
    return doc, page


def md_title(path):
    for line in io.open(path, encoding='utf-8'):
        if line.startswith('# '):
            return line[2:].strip()
    raise AssertionError('нет H1: %s' % path)


def sync_library(titles, dry=False, lang='ru'):
    """Названия в библиотеке берутся из самих документов.

    Держать их отдельным списком - значит рано или поздно разойтись: так уже
    случилось с семью записями. Правится один раз при каждой сборке.
    """
    path = os.path.join(docs_dir(lang), 'index.html')
    assert os.path.isfile(path), path
    s = io.open(path, encoding='utf-8').read()
    changed = []

    def fix(m):
        href, num, old = m.group(1), m.group(2), m.group(3)
        new = html.escape(titles.get(num, ''), quote=False) or old
        want = doc_href(num, lang)
        if new == old and href == want:
            return m.group(0)
        if new != old:
            changed.append((num, old, new))
        return ('<a href="%s"><span class="n">%s</span><span class="t">%s</span></a>'
                % (want, num, new))

    out = re.sub(r'<a href="(/documents/%s/%s\d\d(?:-[a-z0-9-]+)?\.html)">'
                 r'<span class="n">(\d\d)</span><span class="t">([^<]*)</span></a>'
                 % (lang, lang), fix, s)
    assert out.count('<span class="t">') >= 20, 'библиотека разобрана неверно'
    # Пишем по факту различия, а не по списку changed: в нём только смены
    # названий, а адреса меняются молча, и при переезде на слаги файл остался
    # бы со старыми ссылками.
    if out != s and not dry:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
    return changed


def write_redirect_map():
    """Карта 301 со старых числовых адресов на смысловые.

    Пишется сборщиком, а не руками: карта, которую правят отдельно от корпуса,
    расходится с ним на первом же переименовании. nginx подключает её одной
    директивой - см. nginx/README-redirects.txt.

    Старые адреса живут вечно. На них ведут уже разосланные письма и
    опубликованные статьи, и удалить их значит сломать чужие ссылки.
    """
    lines = ['# Собирается build_site_docs.py. Руками не править.',
             '# Формат: <старый путь> <новый путь>;']
    n = 0
    for lang in sorted(SLUGS):
        for num in sorted(SLUGS[lang]):
            lines.append('/documents/%s/%s %s;' % (lang, doc_file_old(num, lang),
                                                   doc_href(num, lang)))
            n += 1
    path = os.path.join(SITE, 'nginx', 'redirects-docs.map')
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    return n


def write_slug_module():
    """Тот же слаг для меню, подвала и бокового меню - из одной таблицы.

    Иначе адрес пришлось бы держать в двух местах, на питоне и на javascript,
    и они разошлись бы ровно так же, как разошлись названия в библиотеке.
    """
    body = (
        '/* Собирается build_site_docs.py из таблицы SLUGS. Руками не править. */\n'
        'export const DOC_SLUGS = %s;\n'
        'export function docPath(lang, doc) {\n'
        '  const s = DOC_SLUGS[lang] && DOC_SLUGS[lang][doc];\n'
        '  return "/documents/" + lang + "/" + lang + doc + (s ? "-" + s : "") + ".html";\n'
        '}\n' % json.dumps(SLUGS, ensure_ascii=True, sort_keys=True, indent=2)
    )
    path = os.path.join(SITE, 'js', 'modern', 'shared', 'doc-slugs.js')
    assert os.path.isdir(os.path.dirname(path)), path
    io.open(path, 'w', encoding='utf-8', newline='\n').write(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docs', nargs='*', help='номера документов или all')
    ap.add_argument('--css', action='store_true', help='пересобрать только CSS')
    ap.add_argument('--dry', action='store_true', help='не писать файлы')
    ap.add_argument('--lang', default='ru', help='язык сборки (по умолчанию ru)')
    a = ap.parse_args()
    lang = a.lang
    md, docs = md_dir(lang), docs_dir(lang)
    assert os.path.isdir(md), 'нет мастеров языка %r: %s' % (lang, md)
    assert os.path.isdir(docs), 'нет каталога страниц языка %r: %s' % (lang, docs)
    assert lang in SLUGS, (
        'для языка %r не заданы слаги в SLUGS. Без них страницы лягут по '
        'числовым адресам, а перелинковка внутри документов ведёт на '
        'смысловые - получатся битые ссылки.' % lang)

    n = build_css()
    print('CSS  css/docs-statute.css  %d байт' % n)
    if a.css:
        return

    targets = CHAIN if (not a.docs or a.docs == ['all']) else a.docs
    missing = [d for d in targets if not os.path.isfile(os.path.join(md, corpus_file(d, lang)))]
    if missing:
        print('нет .md-мастера: %s - пропускаю' % ', '.join(missing))
        targets = [d for d in targets if d not in missing]

    titles = {d: md_title(os.path.join(md, corpus_file(d, lang)))
              for d in CHAIN if os.path.isfile(os.path.join(md, corpus_file(d, lang)))}
    # Если мастеров вдруг не видно - неверный путь, переименование, не та
    # ветка, - заглушки «Документ NN» уходят в библиотеку и затирают живые
    # названия. Так и случилось при переезде корпуса в отдельный репозиторий.
    # Лучше остановиться, чем испортить страницу.
    assert len(titles) >= 20, (
        'найдено мастеров: %d из %d. Ожидается почти весь корпус - проверьте '
        'каталог мастеров (%s). Сборка остановлена, чтобы не записать в '
        'библиотеку заглушки вместо названий.' % (len(titles), len(CHAIN), md))
    for d in CHAIN:
        titles.setdefault(d, 'Документ %s' % d)

    for num in targets:
        src = os.path.join(md, corpus_file(num, lang))
        doc, page = build_doc(num, src, titles, lang=lang)
        dst = os.path.join(docs, doc_file(num, lang))
        if not a.dry:
            io.open(dst, 'w', encoding='utf-8', newline='\n').write(page)
        arts = sum(len(p['articles']) for p in doc['parts'])
        print('OK   %s%s  %-42s частей: %2d, разделов: %3d, %3d КБ'
              % (lang, num, os.path.basename(src)[:42],
                 len([p for p in doc['parts'] if p['label'] or p['title']]),
                 arts, len(page.encode('utf-8')) // 1024))

    for num, old, new in sync_library(titles, a.dry, lang):
        print('библиотека %s%s: %s  ->  %s' % (lang, num, old, new))

    if not a.dry:
        n = write_redirect_map()
        print('редиректы  nginx/redirects-docs.map  строк: %d' % n)
        write_slug_module()
        print('слаги      js/modern/shared/doc-slugs.js')


if __name__ == '__main__':
    main()
