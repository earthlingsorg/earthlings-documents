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
import chrome

HERE = os.path.dirname(os.path.abspath(__file__))
# Мастера лежат в этом же репозитории, по языкам: ru/NN-slug.md.
REPO = os.path.abspath(os.path.join(HERE, '..'))

# Консоль Windows отдаёт cp866 или cp1251, и в них нет ни умлаутов, ни ß, ни
# грузинских букв. Печать имени немецкого файла роняла сборку на предпоследнем
# шаге - страницы уже записаны, а карта редиректов и doc-slugs.js уже нет.
# Меняем не кодировку, а поведение при непечатаемом символе: кириллица в
# русской консоли остаётся читаемой, чужая буква превращается в '?'.
try:
    sys.stdout.reconfigure(errors='replace')
    sys.stderr.reconfigure(errors='replace')
except (AttributeError, ValueError):  # не консоль либо старый Python
    pass

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


# Тема сборки. 'legacy' - боевой сайт, каким он есть; 'v2' - новый, под дизайн
# epic.org. Разница только в оформлении и обвязке: текст, адреса, hreflang,
# JSON-LD и порядок чтения общие, потому что источник один - те же мастера.
# Адреса страниц в обеих темах совпадают знак в знак: подмена сайта должна быть
# сменой корня в nginx, а не переписыванием ссылок.
THEME = 'legacy'


def docs_dir(lang='ru'):
    if THEME == 'v2':
        return os.path.join(SITE, '_v2', 'documents', lang)
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
        '02': 'grazhdanskij-golos',
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
        '02': 'civic-voice',
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
    # Немецкий. Слаги выведены из имён мастеров в de/ и совпадают с внутренней
    # перелинковкой немецких документов. Умляуты и ß в слагах не ставим:
    # транслитерируем по немецкой почтовой норме (ä→ae, ö→oe, ü→ue, ß→ss),
    # иначе ссылка ломается в почте, в мессенджерах и в старых обозревателях.
    'de': {
        '01': 'erklaerung',
        '02': 'buergerstimme',
        '03': 'ethik',
        '04': 'rechtsgrundlage',
        '05': 'charta',
        '07': 'dao',
        '08': 'zellen',
        '09': 'schatzkammer',
        '10': 'earthlings-coin',
        '11': 'unabhaengiger-rat',
        '12': 'digitale-plattform',
        '14': 'weg-des-earthling',
        '15': 'sbt-pass',
        '16': 'biometrische-pruefung',
        '19': 'fahrplan',
        '20': 'gruendungsphase',
        '22': 'rechtliche-hinweise',
        '23': 'ueber-uns',
        '26': 'einwaende-und-antworten',
        '27': 'haeufige-fragen',
        '28': 'datenschutzerklaerung',
        '29': 'nutzungsbedingungen',
        '30': 'entstehung-des-rechtssubjekts',
        '31': 'arbeitsagenda',
        '32': 'wo-wir-jetzt-stehen',
    },
    # Французский. Слаги выведены из имён мастеров в fr/. Диакритика в адрес
    # не идёт: é/è/ê -> e, à -> a, ç -> c. Причина та же, что у умляутов в
    # немецком: адрес с диакритикой ломается в почте и мессенджерах.
    'fr': {
        '01': 'declaration',
        '02': 'voix-citoyenne',
        '03': 'ethique',
        '04': 'base-juridique',
        '05': 'charte',
        '07': 'dao',
        '08': 'cellules',
        '09': 'tresorerie',
        '10': 'earthlings-coin',
        '11': 'conseil-independant',
        '12': 'plateforme-numerique',
        '14': 'chemin-de-l-earthling',
        '15': 'passeport-sbt',
        '16': 'verification-biometrique',
        '19': 'feuille-de-route',
        '20': 'periode-constituante',
        '22': 'mentions-legales',
        '23': 'qui-sommes-nous',
        '26': 'objections-et-reponses',
        '27': 'questions-frequentes',
        '28': 'politique-de-confidentialite',
        '29': 'conditions-d-utilisation',
        '30': 'naissance-du-sujet-de-droit',
        '31': 'agenda-de-travail',
        '32': 'ou-nous-en-sommes',
    },
    # Испанский. Слаги выведены из имён мастеров в es/. Диакритика в адрес
    # не идёт: á/é/í/ó/ú -> a/e/i/o/u, ñ -> n. Причина та же, что у умляутов
    # в немецком: адрес с диакритикой ломается в почте и мессенджерах.
    'es': {
        '01': 'declaracion',
        '02': 'voz-ciudadana',
        '03': 'etica',
        '04': 'base-juridica',
        '05': 'carta',
        '07': 'dao',
        '08': 'celulas',
        '09': 'tesoreria',
        '10': 'earthlings-coin',
        '11': 'consejo-independiente',
        '12': 'plataforma-digital',
        '14': 'camino-del-earthling',
        '15': 'pasaporte-sbt',
        '16': 'verificacion-biometrica',
        '19': 'hoja-de-ruta',
        '20': 'periodo-constituyente',
        '22': 'aviso-legal',
        '23': 'quienes-somos',
        '26': 'objeciones-y-respuestas',
        '27': 'preguntas-frecuentes',
        '28': 'politica-de-privacidad',
        '29': 'condiciones-de-uso',
        '30': 'nacimiento-del-sujeto-de-derecho',
        '31': 'agenda-de-trabajo',
        '32': 'donde-estamos-ahora',
    },
    # Грузинский. Слаг - английский слаг без изменений, и это решение, а не
    # экономия. Мхедрули в адресе превращается в %E1%83%A5, а ссылку
    # пересылают почтой и в мессенджерах. Романизацию грузинского названия
    # брать нельзя по другой причине: конкурирующих систем несколько
    # (национальная 2002 года, BGN/PCGN, ISO 9984), они дают разные написания
    # одного слова, а адрес фиксируется навсегда и живёт в разосланных
    # письмах. Английский слаг снимает выбор целиком.
    'ka': {
        '01': 'declaration',
        '02': 'civic-voice',
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
    # Китайский. Слаг латинский и совпадает с английским: иероглиф в адресе
    # превращается в %E4%B8%AD и ссылка перестаёт читаться в письме. Пиньинь
    # не берём - тональной омонимии много, разбивка на слоги спорна, а выигрыша
    # в понятности нет. Правило раздела 14 инструкции для zh, ar, hi и ka.
    'zh': {
        '01': 'declaration',
        '02': 'civic-voice',
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
    # Арабский. Слаг латинский и совпадает с английским по тому же правилу
    # раздела 14 инструкции, что у zh, hi и ka: арабская вязь в адресе
    # превращается в проценты, а ссылку пересылают почтой и в мессенджерах.
    # Транслитерация арабского не берётся - систем несколько, написание
    # спорно, а выигрыша в понятности нет.
    'ar': {
        '01': 'declaration',
        '02': 'civic-voice',
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


# Документы, снятые с корпуса. Слаг снятого документа не выбрасывается: его
# адрес обязан вести туда, куда переехало содержание, иначе ломаются уже
# разосланные ссылки - то же правило, что и для числовых адресов, см.
# write_redirect_map.
#
# 17 «Что может произойти дальше» снят 2026-08-25 (решение Артура 2026-08-23).
# Шесть его разделов из семи были перекрыты документом 02 полнее; седьмой, о
# тех, кто ещё не родился, перенесён в документ 02, часть VII, разделом 17.
RETIRED = {
    '17': {
        'to': '02',
        'slugs': {'ru': 'chto-dalshe',
                  'en': 'what-may-happen-next',
                  'de': 'was-kommt-als-naechstes',
                  'fr': 'ce-qui-peut-suivre',
                  'es': 'que-puede-pasar-despues',
                  'zh': 'what-may-happen-next',
                  'ar': 'what-may-happen-next',
                  'ka': 'what-may-happen-next'},
    },
}

# порядок чтения корпуса = порядок главного меню; на нём строится «Далее»
CHAIN = ['01', '02', '05', '04', '26', '30', '12', '07', '08', '09', '10', '11',
         '14', '15', '16', '03', '27', '19', '20', '32', '31', '23',
         '22', '28', '29']

# Обвязка берётся из живой страницы, но для переименованных и новых
# документов её задаём здесь - иначе пересборка вернёт старые описания.
OVERRIDES = {
    # Документ 02 заведён 2026-08-21. Он объясняет, ради чего написано
    # остальное, и потому читается сразу за Декларацией.
    '02': {
        'title': u'Гражданский голос | Народ Earthlings',
        'og_title': u'Гражданский голос | Народ Earthlings',
        'description': u'Почему гражданский голос сегодня можно не слышать, не споря по существу, '
                       u'что Earthlings строят взамен и какими ступенями такой голос набирает вес.',
        'og_description': u'Счёт сломан, а не канал. Что это значит и что с этим делают Earthlings.',
    },
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
}

# Английская обвязка. Заголовки здесь не заданы намеренно: они выводятся из H1
# документа и потому разойтись с ним не могут. Описания - зеркало русских: где
# по-русски стоит содержательное описание, оно переведено; где шаблон - шаблон.
# Сочинять по-английски то, чего нет по-русски, значит завести вторую редакцию
# позиционирования, которую никто не сверял.
_OFFICIAL = '%s - an official document of the Earthlings people.'
OVERRIDES_EN = {
    '01': {'description': _OFFICIAL % 'The Earthlings Declaration of Self-Determination'},
    '02': {'description':
           'Why a civic voice can be ignored today without being argued with on the '
           'merits, what the Earthlings are building instead, and by what steps such '
           'a voice gains weight.',
           'og_description':
           'What is broken is the count, not the channel. What that means and what '
           'the Earthlings do about it.'},
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

# Немецкий. `amtlich` не берём: оно означает исходящий от органа власти, а у
# народа органов власти нет. `offiziell` говорит ровно то, что нужно, - документ
# принят народом и говорит от его имени.
_OFFICIAL_DE = '%s - ein offizielles Dokument des Volkes der Earthlings.'

OVERRIDES_DE = {
    '01': {'description': _OFFICIAL_DE % 'Die Erklärung der Selbstbestimmung der Earthlings'},
    '02': {'description':
           'Warum eine Bürgerstimme heute überhört werden kann, ohne ihr in der Sache '
           'zu widersprechen, was die Earthlings stattdessen bauen und über welche '
           'Stufen eine solche Stimme Gewicht gewinnt.',
           'og_description':
           'Kaputt ist die Zählung, nicht der Kanal. Was das heißt und was die '
           'Earthlings damit tun.'},
    '03': {'description': _OFFICIAL_DE % 'Die Ethik der Earthlings'},
    '04': {'description':
           'Die Rechtsgrundlage des Volkes der Earthlings: die Vereinigungsfreiheit, das '
           'Selbstbestimmungsrecht, die Merkmale eines Volkes und die offenen Fragen des '
           'Völkerrechts - mit Quellen und mit der unmittelbaren Angabe dessen, was das '
           'Recht noch nicht entschieden hat.',
           'og_description':
           'Vereinigungsfreiheit, Selbstbestimmung, die Merkmale eines Volkes und das, was '
           'das Völkerrecht noch nicht entschieden hat.'},
    '05': {'description': _OFFICIAL_DE % 'Die Charta der Earthlings'},
    '07': {'description': _OFFICIAL_DE % 'Die DAO der Earthlings: Grundsätze, Architektur und Verwaltung'},
    '08': {'description': _OFFICIAL_DE % 'Die Zellen der Earthlings - das System der Projekte und der Zusammenarbeit'},
    '09': {'description': _OFFICIAL_DE % 'Die Schatzkammer der Earthlings'},
    '10': {'description': _OFFICIAL_DE % 'Earthlings Coin: die vollständige Dokumentation'},
    '11': {'description': _OFFICIAL_DE % 'Der Unabhängige Rat der Earthlings'},
    '12': {'description': _OFFICIAL_DE % 'Die digitale Plattform der Earthlings'},
    '14': {'description': _OFFICIAL_DE % 'Der Weg des Earthling'},
    '15': {'description': _OFFICIAL_DE % 'Der SBT-Pass des Earthling'},
    '16': {'description': _OFFICIAL_DE % 'Die Richtlinie der biometrischen Prüfung der Earthlings'},
    '19': {'description': _OFFICIAL_DE % 'Der Fahrplan der Übergangszeit'},
    '20': {'description':
           'Die Gründungsphase der Earthlings: Vorschläge werden zum gesamten Bestand von '
           'fünfundzwanzig Dokumenten angenommen - zur Erklärung, zur Charta und zu den '
           'übrigen - vom 7. September bis zum 6. Dezember 2026, die Niederschrift am '
           '20. Dezember, die Abstimmung über die Erklärung am 3. Januar 2027. Was zur '
           'Erörterung steht, was nicht zur Erörterung steht und wie man teilnimmt.'},
    '22': {'description': _OFFICIAL_DE % 'Rechtliche Hinweise'},
    '23': {'description': _OFFICIAL_DE % 'Über uns'},
    '26': {'description':
           'Einwände gegen den Bau des Volkes der Earthlings - zu Separatismus, Souveränität, '
           'Plutokratie in der DAO, zum Beitrag, zum unabänderlichen Kern und zum Recht, in '
           'irgendjemandes Namen zu sprechen - mit Antworten und mit einer Liste dessen, was '
           'wir nicht für widerlegt halten.',
           'og_description':
           'Einwände gegen den Bau des Volkes der Earthlings und die Antworten darauf, '
           'einschließlich derer, die wir nicht für widerlegt halten.'},
    '27': {'description':
           'Das Volk der Earthlings beantwortet häufige Fragen zu Verwaltung, Wirtschaft, '
           'Identität und Ethik - wie es arbeitet, wer es kontrolliert, wie die Daten '
           'geschützt sind.',
           'og_description':
           'Das Volk der Earthlings beantwortet häufige Fragen zu Verwaltung, Wirtschaft, '
           'Identität und Ethik.'},
    '28': {'description': _OFFICIAL_DE % 'Die Datenschutzerklärung des Volkes der Earthlings'},
    '29': {'description': _OFFICIAL_DE % 'Die Nutzungsbedingungen des Volkes der Earthlings'},
    '30': {'description':
           'Thesen des Volkes der Earthlings: warum das Völkerrecht Lehren über das Bestehen '
           'kollektiver Träger entwickelt, ihre freiwillige Konstituierung aber kaum '
           'ausgearbeitet hat - und warum diese Lücke die Entstehung eines Volkes nicht '
           'rechtswidrig macht.'},
    '31': {'description':
           'Die Arbeitsagenda des Volkes der Earthlings: eine fachliche Zerlegung eines '
           'möglichen Modells künftiger Weltordnung durch die Metapher eines '
           'Betriebssystems. Eine Ergänzung der Staaten und kein Ersatz.'},
    '32': {'description':
           'Wo wir jetzt stehen: welchen Code und welche Daten Earthlings veröffentlicht, was '
           'geschlossen ist, aus welchem Grund, und was sich jeder selbst überprüfen kann.',
           'og_description':
           'Welchen Code und welche Daten Earthlings veröffentlicht, was geschlossen ist und '
           'aus welchem Grund.'},
}

_OFFICIAL_FR = '%s - un document officiel du peuple des Earthlings.'

OVERRIDES_FR = {
    '01': {'description': _OFFICIAL_FR % "La Déclaration des Earthlings sur l'autodétermination"},
    '02': {'description':
           "Pourquoi la voix citoyenne peut aujourd'hui être ignorée sans être "
           'contestée sur le fond, ce que les Earthlings construisent à la place et '
           'par quels degrés cette voix gagne du poids.',
           'og_description':
           "Ce qui est cassé, c'est le compte, pas le canal. Ce que cela veut dire "
           'et ce que les Earthlings en font.'},
    '03': {'description': _OFFICIAL_FR % "L'éthique des Earthlings"},
    '04': {'description':
           'La base juridique du peuple des Earthlings: la liberté d\'association, le droit '
           'à l\'autodétermination, les caractères d\'un peuple et les questions ouvertes du '
           'droit international - avec les sources, et en disant directement ce que le droit '
           'n\'a pas encore tranché.',
           'og_description':
           "Liberté d'association, autodétermination, caractères d'un peuple et ce que le "
           "droit international n'a pas encore tranché."},
    '05': {'description': _OFFICIAL_FR % 'La Charte des Earthlings'},
    '07': {'description': _OFFICIAL_FR % 'La DAO des Earthlings: principes, architecture et gouvernance'},
    '08': {'description': _OFFICIAL_FR % 'Les cellules des Earthlings - le système des projets et de la coopération'},
    '09': {'description': _OFFICIAL_FR % 'La Trésorerie des Earthlings'},
    '10': {'description': _OFFICIAL_FR % 'Earthlings Coin: la documentation complète'},
    '11': {'description': _OFFICIAL_FR % 'Le Conseil indépendant des Earthlings'},
    '12': {'description': _OFFICIAL_FR % 'La plateforme numérique des Earthlings'},
    '14': {'description': _OFFICIAL_FR % "Le chemin de l'earthling"},
    '15': {'description': _OFFICIAL_FR % "Le passeport SBT de l'earthling"},
    '16': {'description': _OFFICIAL_FR % 'La politique de vérification biométrique des Earthlings'},
    '19': {'description': _OFFICIAL_FR % 'La feuille de route de la période de transition'},
    '20': {'description':
           'La période constituante des Earthlings: les propositions sont reçues sur '
           'l\'ensemble des vingt-cinq documents - la Déclaration, la Charte et les autres - '
           'du 7 septembre au 6 décembre 2026, le relevé le 20 décembre, le vote sur la '
           'Déclaration le 3 janvier 2027. Ce qui est en discussion, ce qui ne l\'est pas et '
           'comment participer.'},
    '22': {'description': _OFFICIAL_FR % 'Mentions légales'},
    '23': {'description': _OFFICIAL_FR % 'Qui sommes-nous'},
    '26': {'description':
           'Les objections à la construction du peuple des Earthlings - sur le séparatisme, '
           'la souveraineté, la ploutocratie dans la DAO, la cotisation, le noyau intangible '
           'et le droit de parler au nom de qui que ce soit - avec les réponses et avec la '
           'liste de ce que nous ne tenons pas pour réfuté.',
           'og_description':
           'Les objections à la construction du peuple des Earthlings et les réponses, y '
           'compris celles que nous ne tenons pas pour réfutées.'},
    '27': {'description':
           'Le peuple des Earthlings répond aux questions fréquentes sur la gouvernance, '
           'l\'économie, l\'identité et l\'éthique: comment il fonctionne, qui le contrôle, '
           'comment les données sont protégées.',
           'og_description':
           'Le peuple des Earthlings répond aux questions fréquentes sur la gouvernance, '
           "l'économie, l'identité et l'éthique."},
    '28': {'description': _OFFICIAL_FR % 'La politique de confidentialité du peuple des Earthlings'},
    '29': {'description': _OFFICIAL_FR % "Les conditions d'utilisation du peuple des Earthlings"},
    '30': {'description':
           'Thèses du peuple des Earthlings: pourquoi le droit international a développé des '
           'doctrines sur l\'existence des sujets collectifs mais n\'a presque pas élaboré '
           'leur constitution volontaire - et pourquoi cette lacune ne rend pas illicite la '
           'naissance d\'un peuple.'},
    '31': {'description':
           'L\'agenda de travail du peuple des Earthlings: une analyse spécialisée d\'un '
           'modèle possible de l\'ordre mondial à venir, par la métaphore d\'un système '
           'd\'exploitation. Un complément aux États et non leur remplacement.'},
    '32': {'description':
           'Où nous en sommes: quel code et quelles données les Earthlings publient, ce qui '
           'est fermé, pour quelle raison, et ce que chacun peut vérifier lui-même.',
           'og_description':
           'Quel code et quelles données les Earthlings publient, ce qui est fermé et pour '
           'quelle raison.'},
}

_OFFICIAL_ES = '%s - un documento oficial del pueblo Earthlings.'

OVERRIDES_ES = {
    '01': {'description': _OFFICIAL_ES % 'La Declaración Earthlings sobre la libre determinación'},
    '02': {'description':
           'Por qué hoy se puede no escuchar la voz ciudadana sin discutirla en el '
           'fondo, qué construyen los Earthlings a cambio y por qué escalones esa voz '
           'gana peso.',
           'og_description':
           'Lo roto es el recuento, no el canal. Qué significa y qué hacen los '
           'Earthlings al respecto.'},
    '03': {'description': _OFFICIAL_ES % 'La ética de los Earthlings'},
    '04': {'description':
           'La base jurídica del pueblo Earthlings: la libertad de asociación, el derecho '
           'de libre determinación, los rasgos de un pueblo y las cuestiones abiertas del '
           'derecho internacional - con las fuentes, y diciendo de manera expresa lo que el '
           'derecho no ha resuelto todavía.',
           'og_description':
           'Libertad de asociación, libre determinación, rasgos de un pueblo y lo que el '
           'derecho internacional no ha resuelto todavía.'},
    '05': {'description': _OFFICIAL_ES % 'La Carta de los Earthlings'},
    '07': {'description': _OFFICIAL_ES % 'La DAO de los Earthlings: principios, arquitectura y gobierno'},
    '08': {'description': _OFFICIAL_ES % 'Las células de los Earthlings - el sistema de proyectos y de cooperación'},
    '09': {'description': _OFFICIAL_ES % 'La Tesorería de los Earthlings'},
    '10': {'description': _OFFICIAL_ES % 'Earthlings Coin: la documentación completa'},
    '11': {'description': _OFFICIAL_ES % 'El Consejo Independiente de los Earthlings'},
    '12': {'description': _OFFICIAL_ES % 'La plataforma digital de los Earthlings'},
    '14': {'description': _OFFICIAL_ES % 'El camino del earthling'},
    '15': {'description': _OFFICIAL_ES % 'El pasaporte SBT del earthling'},
    '16': {'description': _OFFICIAL_ES % 'La política de verificación biométrica de los Earthlings'},
    '19': {'description': _OFFICIAL_ES % 'La hoja de ruta del período de transición'},
    '20': {'description':
           'El período constituyente de los Earthlings: las propuestas se reciben sobre los '
           'veinticinco documentos - la Declaración, la Carta y los demás - del 7 de '
           'septiembre al 6 de diciembre de 2026, el compendio el 20 de diciembre, la '
           'votación de la Declaración el 3 de enero de 2027. Qué se discute, qué no y cómo '
           'participar.'},
    '22': {'description': _OFFICIAL_ES % 'Aviso legal'},
    '23': {'description': _OFFICIAL_ES % 'Quiénes somos'},
    '26': {'description':
           'Las objeciones a la construcción del pueblo Earthlings - sobre el separatismo, '
           'la soberanía, la plutocracia en la DAO, la cuota, el núcleo intangible y el '
           'derecho a hablar en nombre de alguien - con sus respuestas y con la lista de lo '
           'que no damos por refutado.',
           'og_description':
           'Las objeciones a la construcción del pueblo Earthlings y sus respuestas, '
           'incluidas las que no damos por refutadas.'},
    '27': {'description':
           'El pueblo Earthlings responde a las preguntas frecuentes sobre el gobierno, la '
           'economía, la identidad y la ética: cómo funciona, quién lo controla, cómo se '
           'protegen los datos.',
           'og_description':
           'El pueblo Earthlings responde a las preguntas frecuentes sobre el gobierno, la '
           'economía, la identidad y la ética.'},
    '28': {'description': _OFFICIAL_ES % 'La política de privacidad del pueblo Earthlings'},
    '29': {'description': _OFFICIAL_ES % 'Las condiciones de uso del pueblo Earthlings'},
    '30': {'description':
           'Tesis del pueblo Earthlings: por qué el derecho internacional ha desarrollado '
           'doctrinas sobre la existencia de sujetos colectivos pero apenas ha elaborado su '
           'constitución voluntaria, y por qué esa laguna no hace ilícito el nacimiento de '
           'un pueblo.'},
    '31': {'description':
           'La agenda de trabajo del pueblo Earthlings: un análisis especializado de un '
           'modelo posible del orden mundial venidero, mediante la metáfora de un sistema '
           'operativo. Un complemento a los Estados y no su sustitución.'},
    '32': {'description':
           'Dónde estamos ahora: qué código y qué datos publican los Earthlings, qué está '
           'cerrado, por qué motivo y qué puede verificar cualquiera por sí mismo.',
           'og_description':
           'Qué código y qué datos publican los Earthlings, qué está cerrado y por qué '
           'motivo.'},
}

_OFFICIAL_KA = '%s - Earthlings-ის ხალხის ოფიციალური დოკუმენტი.'

OVERRIDES_KA = {
    '01': {'description': _OFFICIAL_KA % 'Earthlings-ის დეკლარაცია თვითგამორკვევის შესახებ'},
    '03': {'description': _OFFICIAL_KA % 'Earthlings-ის ეთიკა'},
    '04': {'description':
           'Earthlings-ის ხალხის სამართლებრივი საფუძველი: გაერთიანების თავისუფლება, '
           'თვითგამორკვევის უფლება, ხალხის ნიშნები და საერთაშორისო სამართლის ღია '
           'საკითხები - წყაროებით და იმის პირდაპირი მითითებით, რაც სამართალს ჯერ '
           'არ გადაუწყვეტია.',
           'og_description':
           'გაერთიანების თავისუფლება, თვითგამორკვევა, ხალხის ნიშნები და ის, რაც '
           'საერთაშორისო სამართალს ჯერ არ გადაუწყვეტია.'},
    '05': {'description': _OFFICIAL_KA % 'Earthlings-ის ქარტია'},
    '07': {'description': _OFFICIAL_KA % 'Earthlings-ის DAO: პრინციპები, არქიტექტურა და მართვა'},
    '08': {'description': _OFFICIAL_KA % 'Earthlings-ის უჯრედები - პროექტებისა და თანამშრომლობის სისტემა'},
    '09': {'description': _OFFICIAL_KA % 'Earthlings-ის ხაზინა'},
    '10': {'description': _OFFICIAL_KA % 'Earthlings Coin: სრული დოკუმენტაცია'},
    '11': {'description': _OFFICIAL_KA % 'Earthlings-ის დამოუკიდებელი საბჭო'},
    '12': {'description': _OFFICIAL_KA % 'Earthlings-ის ციფრული პლატფორმა'},
    '14': {'description': _OFFICIAL_KA % 'earthling-ის გზა'},
    '15': {'description': _OFFICIAL_KA % 'earthling-ის SBT-პასპორტი'},
    '16': {'description': _OFFICIAL_KA % 'Earthlings-ის ბიომეტრიული ვერიფიკაციის პოლიტიკა'},
    '19': {'description': _OFFICIAL_KA % 'გარდამავალი პერიოდის საგზაო რუკა'},
    '20': {'description':
           'Earthlings-ის დამფუძნებელი პერიოდი: წინადადებები მიიღება ოცდახუთივე '
           'დოკუმენტზე - დეკლარაციაზე, ქარტიაზე და დანარჩენებზე - 2026 წლის 7 '
           'სექტემბრიდან 6 დეკემბრამდე, კრებული 20 დეკემბერს, დეკლარაციის კენჭისყრა '
           '2027 წლის 3 იანვარს. რა განიხილება, რა არა და როგორ მივიღოთ მონაწილეობა.'},
    '22': {'description': _OFFICIAL_KA % 'იურიდიული ინფორმაცია'},
    '23': {'description': _OFFICIAL_KA % 'ჩვენ შესახებ'},
    '26': {'description':
           'შედავებები Earthlings-ის ხალხის კონსტრუქციის წინააღმდეგ - სეპარატიზმზე, '
           'სუვერენიტეტზე, პლუტოკრატიაზე DAO-ში, შენატანზე, უცვლელ ბირთვსა და '
           'ვინმეს სახელით ლაპარაკის უფლებაზე - პასუხებით და იმის ჩამონათვალით, რასაც '
           'გაქარწყლებულად არ ვთვლით.',
           'og_description':
           'შედავებები Earthlings-ის ხალხის კონსტრუქციის წინააღმდეგ და პასუხები მათზე, '
           'მათ შორის ის, რასაც გაქარწყლებულად არ ვთვლით.'},
    '27': {'description':
           'Earthlings-ის ხალხი პასუხობს ხშირ კითხვებს მართვის, ეკონომიკის, '
           'იდენტობისა და ეთიკის შესახებ: როგორ არის მოწყობილი, ვინ აკონტროლებს, '
           'როგორ არის დაცული მონაცემები.',
           'og_description':
           'Earthlings-ის ხალხი პასუხობს ხშირ კითხვებს მართვის, ეკონომიკის, '
           'იდენტობისა და ეთიკის შესახებ.'},
    '28': {'description': _OFFICIAL_KA % 'Earthlings-ის ხალხის კონფიდენციალურობის პოლიტიკა'},
    '29': {'description': _OFFICIAL_KA % 'Earthlings-ის ხალხის მომხმარებლის შეთანხმება'},
    '30': {'description':
           'Earthlings-ის ხალხის თეზისები: რატომ შეიმუშავა საერთაშორისო სამართალმა '
           'დოქტრინები კოლექტიური სუბიექტების არსებობაზე, მაგრამ თითქმის არ შეიმუშავა '
           'მათი ნებაყოფლობითი დაფუძნება, და რატომ არ ხდის ეს ხარვეზი ხალხის '
           'წარმოშობას მართლსაწინააღმდეგოდ.'},
    '31': {'description':
           'Earthlings-ის ხალხის სამუშაო დღის წესრიგი: მომავალი მსოფლიო წესრიგის '
           'ერთ-ერთი შესაძლო მოდელის ვიწროსპეციალური გარჩევა ოპერაციული სისტემის '
           'მეტაფორით. სახელმწიფოების დამატება და არა მათი ჩანაცვლება.'},
    '32': {'description':
           'სად ვართ ახლა: რომელ კოდსა და რომელ მონაცემებს აქვეყნებს Earthlings, რა '
           'არის დახურული, რა მიზეზით და რისი შემოწმება შეუძლია ნებისმიერს '
           'დამოუკიდებლად.',
           'og_description':
           'რომელ კოდსა და რომელ მონაცემებს აქვეყნებს Earthlings, რა არის დახურული '
           'და რა მიზეზით.'},
}

# Обвязка своя у каждого языка: описание страницы - это текст, а не настройка.
_OFFICIAL_ZH = '%s——Earthlings 人民的官方文件。'

# Китайский. Описания - текст, а не настройка: переведены, а не скопированы.
# Типографика китайская: полноширинные знаки, тире 破折号 двумя U+2014.
OVERRIDES_ZH = {
    '01': {'description': _OFFICIAL_ZH % 'Earthlings 自决宣言'},
    '02': {'description':
           '为什么今天可以不听公民的声音，却不必在实质上与之争辩；Earthlings 拿什么'
           '来代替；以及这样的声音经由哪些台阶获得分量。',
           'og_description':
           '坏掉的是计数，不是渠道。这是什么意思，Earthlings 又做了什么。'},
    '03': {'description': _OFFICIAL_ZH % 'Earthlings 伦理准则'},
    '04': {'description':
           'Earthlings 人民的法律依据：结社自由、自决权、人民的特征，以及国际法上'
           '尚未解决的问题——附出处，并直接说明法律尚未决定的是什么。',
           'og_description':
           '结社自由、自决、人民的特征，以及国际法尚未决定的东西。'},
    '05': {'description': _OFFICIAL_ZH % 'Earthlings 宪章'},
    '07': {'description': _OFFICIAL_ZH % 'Earthlings DAO'},
    '08': {'description': _OFFICIAL_ZH % 'Earthlings 蜂巢单元'},
    '09': {'description': _OFFICIAL_ZH % 'Earthlings 司库'},
    '10': {'description': _OFFICIAL_ZH % 'Earthlings Coin'},
    '11': {'description': _OFFICIAL_ZH % 'Earthlings 独立理事会'},
    '12': {'description': _OFFICIAL_ZH % 'Earthlings 数字平台'},
    '14': {'description': _OFFICIAL_ZH % 'earthling 之路'},
    '15': {'description': _OFFICIAL_ZH % 'earthling SBT 护照'},
    '16': {'description': _OFFICIAL_ZH % '生物特征验证政策'},
    '19': {'description': _OFFICIAL_ZH % 'Earthlings 路线图'},
    '20': {'description':
           '创立期：文本如何开放接受建议，什么不予讨论，期限如何安排，'
           '以及《宣言》如何付诸表决。',
           'og_description': '建议、期限，以及《宣言》如何付诸表决。'},
    '22': {'description': _OFFICIAL_ZH % '法律信息'},
    '23': {'description':
           '关于我们：著作、治理、资金与公开验证——附可核实的链上地址。',
           'og_description': '著作、治理、资金与公开验证。'},
    '26': {'description':
           '针对 Earthlings 人民的法律异议与逐条答复——包括我们无话可答的那些。',
           'og_description': '法律异议与逐条答复，包括我们无话可答的那些。'},
    '27': {'description': _OFFICIAL_ZH % '常见问题'},
    '28': {'description': _OFFICIAL_ZH % '隐私政策'},
    '29': {'description': _OFFICIAL_ZH % '使用条款'},
    '30': {'description':
           '法律主体如何产生：从实践到规范的路径，以及为什么人类这一层级'
           '至今没有形式。',
           'og_description': '法律主体如何产生，以及人类这一层级为什么没有形式。'},
    '31': {'description': _OFFICIAL_ZH % 'Earthlings 工作议程'},
    '32': {'description':
           '我们现在在哪里：已经做成的、尚未做成的，以及现在还只能靠我们的话'
           '而不是靠技术的东西。',
           'og_description': '已经做成的、尚未做成的，以及还只能靠我们的话的东西。'},
}

# Арабский. Термины - из действующей редакции словаря (раздел 6А), а не из первой:
# взнос `رسم الانضمام`, а не `الاشتراك` (тот значит регулярный членский); признаки
# народа `المقومات`, а не `العلامات` (то знак, симптом); субъект права `شخص` из
# `أشخاص القانون`, а не `ذات`. «Официальный» - `رسمي`, слово статьи 111 Устава ООН;
# на аутентичность текста оно не претендует, для неё в корпусе свой оборот.
# Три вещи, которых нет ни у одного другого языка. Латиница отделяется пробелами с
# обеих сторон: в RTL слипание `Earthlings` с приставочной частицей глазами не видно,
# а разводить татвилем нельзя - он в жёстких замках, там же и арабо-индийские цифры,
# поэтому числа только ASCII. Огласовки не ставятся: в метаописании они не нужны,
# а фразы построены так, чтобы без них не возникало разночтения.
# Регистра букв в арабском нет, и различает только латиница: `Earthlings` - имя
# народа, `earthling` - участник.
_OFFICIAL_AR = '%s - وثيقة رسمية من وثائق شعب Earthlings.'

OVERRIDES_AR = {
    '01': {'description': _OFFICIAL_AR % 'إعلان Earthlings لتقرير المصير'},
    '02': {'description':
           'لماذا يمكن اليوم عدم سماع الصوت المدني دون منازعته في الجوهر، وما الذي '
           'يبنيه Earthlings بدلاً من ذلك، وبأي درجات يكتسب هذا الصوت وزناً.',
           'og_description':
           'المكسور هو العدّ لا القناة. ما معنى ذلك وما الذي يفعله Earthlings حياله.'},
    '03': {'description': _OFFICIAL_AR % 'أخلاقيات Earthlings'},
    '04': {'description':
           'الأساس القانوني لشعب Earthlings: حرية تكوين الجمعيات، وحق تقرير المصير، '
           'ومقومات الشعب، والمسائل المفتوحة في القانون الدولي - بمصادرها وببيان صريح '
           'لما لم يحسمه القانون بعد.',
           'og_description':
           'حرية تكوين الجمعيات، وتقرير المصير، ومقومات الشعب، وما لم يحسمه القانون '
           'الدولي بعد.'},
    '05': {'description': _OFFICIAL_AR % 'ميثاق Earthlings'},
    '07': {'description': _OFFICIAL_AR % 'DAO Earthlings: المبادئ والبنية والحكم'},
    '08': {'description': _OFFICIAL_AR % 'خلايا Earthlings: نظام المشاريع والتعاون'},
    '09': {'description': _OFFICIAL_AR % 'خزانة Earthlings المشتركة'},
    '10': {'description': _OFFICIAL_AR % 'Earthlings Coin: الوحدة الحسابية الداخلية'},
    '11': {'description': _OFFICIAL_AR % 'مجلس Earthlings المستقل'},
    '12': {'description': _OFFICIAL_AR % 'منصة Earthlings الرقمية'},
    '14': {'description': _OFFICIAL_AR % 'طريق earthling'},
    '15': {'description': _OFFICIAL_AR % 'جواز earthling من نوع SBT'},
    '16': {'description': _OFFICIAL_AR % 'سياسة Earthlings للتحقق البيومتري'},
    '19': {'description': _OFFICIAL_AR % 'خارطة طريق الفترة الانتقالية'},
    '20': {'description':
           'الفترة التأسيسية لشعب Earthlings: باب المقترحات مفتوح على مجموعة الوثائق '
           'الخمس والعشرين كلها - الإعلان والميثاق وسائرها - من 7 أيلول/سبتمبر إلى '
           '6 كانون الأول/ديسمبر 2026، والحصيلة في 20 كانون الأول/ديسمبر، والتصويت على '
           'الإعلان في 3 كانون الثاني/يناير 2027. ما هو مفتوح للنقاش، وما لا يخضع '
           'للنقاش، وكيف تشارك.'},
    '22': {'description': _OFFICIAL_AR % 'معلومات قانونية'},
    '23': {'description': _OFFICIAL_AR % 'من نحن'},
    '26': {'description':
           'الاعتراضات على بنية شعب Earthlings - في الانفصال والسيادة وحكم الأثرياء في '
           'DAO ورسم الانضمام والنواة غير القابلة للتعديل وحق الكلام باسم أحد - مع '
           'الأجوبة عنها ومع قائمة بما يبقى غير مدحوض.',
           'og_description':
           'الاعتراضات على بنية شعب Earthlings والأجوبة عنها، بما في ذلك ما يبقى غير '
           'مدحوض.'},
    '27': {'description':
           'يجيب شعب Earthlings عن الأسئلة الشائعة في الحكم والاقتصاد والهوية '
           'والأخلاقيات: كيف يعمل هذا، ومن يحكم في الحقيقة، وكيف تحمى البيانات.',
           'og_description':
           'يجيب شعب Earthlings عن الأسئلة الشائعة في الحكم والاقتصاد والهوية '
           'والأخلاقيات.'},
    '28': {'description': _OFFICIAL_AR % 'سياسة الخصوصية لشعب Earthlings'},
    '29': {'description': _OFFICIAL_AR % 'اتفاقية الاستخدام الخاصة بشعب Earthlings'},
    '30': {'description':
           'أطروحات شعب Earthlings: لماذا طور القانون الدولي فقه وجود الأشخاص '
           'الجماعيين ولم يعالج تقريبا نشوءهم الطوعي - ولماذا لا يجعل هذا الفراغ نشوء '
           'الشعب غير مشروع.'},
    '31': {'description':
           'جدول أعمال شعب Earthlings: تحليل تخصصي لنموذج ممكن من نماذج النظام العالمي '
           'المقبل، باستعارة نظام التشغيل. تكملة للدول لا إلغاء لها.'},
    '32': {'description':
           'أين نحن الآن: أي شفرة وأي بيانات ينشرها شعب Earthlings، وما هو مغلق، ولأي '
           'سبب، وما الذي يستطيع أي إنسان أن يتحقق منه بنفسه.',
           'og_description':
           'أي شفرة وأي بيانات ينشرها شعب Earthlings، وما هو مغلق ولأي سبب.'},
}

OVERRIDES_BY_LANG = {'ru': OVERRIDES, 'en': OVERRIDES_EN, 'de': OVERRIDES_DE,
                     'fr': OVERRIDES_FR, 'es': OVERRIDES_ES, 'ka': OVERRIDES_KA,
                     'zh': OVERRIDES_ZH, 'ar': OVERRIDES_AR}

# Можно ли переносить обвязку с уже лежащей на сайте страницы. Можно, только
# если она - прежняя сборка того же текста. Английские страницы остались от
# вытесненного перевода, поэтому для них - нет.
# Немецкие страницы на сайте остались от перевода 27 июля, вытесненного этими
# мастерами, - обвязку с них брать нельзя ровно по той же причине, что и с
# английских.
# Французские страницы на сайте остались от прежнего круга перевода,
# вытесненного этими мастерами, - обвязку с них брать нельзя по той же
# причине, что и с английских и немецких.
# Грузинские страницы на сайте остались от прежнего круга перевода: с тех пор
# русские мастера переписаны, Декларация пересобрана на пять частей и
# одиннадцать статей, состав корпуса изменился. Ярлык «gold standard» говорит о
# качестве того текста, а не о его соответствии нынешнему русскому, и обвязку
# с этих страниц брать нельзя ровно по той же причине, что и с остальных.
# Арабские страницы на сайте остались от прежнего круга перевода - обвязку
# с них брать нельзя ровно по той же причине, что и с остальных.
WRAPPER_FROM_PAGE = {'ru': True, 'en': False, 'de': False, 'fr': False,
                    'es': False, 'ka': False, 'zh': False, 'ar': False}


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
# Грузинский исключён из документа 02 на время заморозки: мастер
# ka/02-civic-voice.md не закоммичен. Тем же списком фильтруется меню,
# поэтому на грузинских страницах пункта не будет - и ссылки в никуда тоже.
LANGS_BY_DOC = {'02': ['ar', 'de', 'en', 'es', 'fr', 'ru', 'zh'],
                '20': ['ar', 'de', 'en', 'es', 'fr', 'ka', 'ru', 'zh'],
                '32': ['ar', 'de', 'en', 'es', 'fr', 'ka', 'ru', 'zh']}

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
    'de': {
        'toc': 'Inhalt',
        'prev': '← Zurück',
        'next': 'Weiter →',
        'nav_aria': 'Navigation durch die Dokumente',
        'all_docs': 'Alle Dokumente',
    },
    'fr': {
        'toc': 'Sommaire',
        'prev': '← Retour',
        'next': 'Suivant →',
        'nav_aria': 'Navigation dans les documents',
        'all_docs': 'Tous les documents',
    },
    'es': {
        'toc': 'Índice',
        'prev': '← Atrás',
        'next': 'Siguiente →',
        'nav_aria': 'Navegación por los documentos',
        'all_docs': 'Todos los documentos',
    },
    # Заглавных букв в мхедрули нет, и строки интерфейса набраны строчными:
    # прописная в начале - явление чужого письма. Регистр надстрочников рисует
    # CSS, и для грузинского браузер показывает его как мтаврули.
    'ka': {
        'toc': 'შინაარსი',
        'prev': '← უკან',
        'next': 'შემდეგი →',
        'nav_aria': 'დოკუმენტებში ნავიგაცია',
        'all_docs': 'ყველა დოკუმენტი',
    },
    'zh': {
        'toc': '目录',
        'prev': '← 上一篇',
        'next': '下一篇 →',
        'nav_aria': '文件导航',
        'all_docs': '全部文件',
    },
    # Арабский - единственный язык корпуса, который читается справа налево, и
    # СТРЕЛКИ ЗДЕСЬ ЗЕРКАЛЬНЫЕ. U+2190 и U+2192 не входят в число символов,
    # которые двунаправленный алгоритм отражает сам (в отличие от скобок), так
    # что скопированная у соседнего языка стрелка «назад» будет показывать
    # вперёд. «Назад» получает →, «Далее» получает ←.
    # Место стрелки в строке остаётся прежним - в начале у «назад», в конце у
    # «далее»: стрелка знак нейтрального направления, и в правостороннем абзаце
    # начало строки и есть правый край. Разметку менять не нужно.
    'ar': {
        'toc': 'المحتويات',
        'prev': '→ السابق',
        'next': 'التالي ←',
        'nav_aria': 'التنقل بين الوثائق',
        'all_docs': 'كل الوثائق',
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

    if THEME == 'v2':
        # Три листа и один скрипт на 950 байт - всё оформление страницы.
        # Встроенного <style> нет: шапка не fixed, отступ сверху не нужен.
        assets = chrome.font_preloads(lang) + [
            '<link rel="stylesheet" href="/css/tokens.css">',
            '<link rel="stylesheet" href="/css/chrome.css">',
            '<link rel="stylesheet" href="/css/doc.css">',
            '<script defer src="/js/chrome.js"></script>',
        ]
        for css in EXTRA_CSS_BY_DOC.get(num, []):
            # Особые стили пока есть только у документа 31 (схемы «Рабочей
            # повестки»), и они написаны на токенах прежней темы. Молча
            # выбрасывать их нельзя: страница соберётся, а схемы поедут.
            if os.path.isfile(os.path.join(SITE, '_v2', 'css', css)):
                assets.append('<link rel="stylesheet" href="/css/%s">' % css)
            else:
                sys.stderr.write(
                    'ВНИМАНИЕ %s%s: нет _v2/css/%s - схемы документа останутся '
                    'без оформления. Лист написан на токенах прежней темы и '
                    'ждёт переноса.\n' % (lang, num, css))
    else:
        assets = [
            '<link rel="stylesheet" href="/css/docs-statute.css?v=1">',
            # Шапка сайта - fixed, поэтому текст ушёл бы под неё: отступ сверху
            # равен её высоте плюс два сантиметра воздуха. overflow-x гасит
            # горизонтальную полосу: подвал растянут приёмом margin:0 -50vw, а
            # 100vw шире содержимого на ширину вертикального скроллбара.
            "<style>body{margin:0;background:#ece5d6;overflow-x:clip}"
            ".statute{padding-top:calc(var(--header-height,64px) + 76px)}</style>",
            SHELL_ASSETS,
        ] + ['<link rel="stylesheet" href="/css/%s?v=1">' % css
             for css in EXTRA_CSS_BY_DOC.get(num, [])]

    parts = [
        '<!DOCTYPE html>',
        '<html lang="%s"%s>' % (lang, ' dir="rtl"' if lang in chrome.RTL else ''),
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % esc(title),
        '<meta name="description" content="%s">' % esc(desc),
    ] + assets + [
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
    # Соседа ищем не по номеру в цепочке, а по первому, который у ЭТОГО языка
    # действительно есть. Иначе «далее» уводит на несобранную страницу: так
    # вышло 2026-08-23, когда документ 02 встал вторым, а грузинский из него
    # исключён заморозкой - грузинская Декларация начала предлагать переход в
    # никуда. Цепочка одна на все языки, а состав у языков разный, и это
    # расхождение будет всякий раз, когда язык отстаёт.
    def near(step):
        j = i + step
        while 0 <= j < len(CHAIN):
            if has_doc(CHAIN[j], lang):
                return CHAIN[j]
            j += step
        return None

    prev = near(-1)
    nxt = near(1)
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


def has_doc(num, lang):
    """Есть ли документ на этом языке - по таблице сборщика, единственной.

    Меню порождается отсюда же. На боевом сайте список языков документа лежал
    ещё и в constants.js, и 17 августа 2026 они разошлись: немецкий читатель не
    мог дойти по меню до документов 17, 20 и 32, хотя все три страницы отдавали
    200. Второго источника здесь нет по построению.
    """
    return lang in LANGS_BY_DOC.get(num, ALL_LANGS)


def build_doc_v2(num, doc, head, toc, body, titles, lang):
    """Страница в новом оформлении: статическая обвязка вместо веб-компонентов.

    Скрипта, который рисует меню, здесь нет: шапка и подвал приезжают готовым
    HTML из chrome.py. Переключатель языка - настоящие ссылки, поэтому и
    LANG_SWITCH не нужен: переключать нечего, ссылка ведёт куда надо сама.
    """
    href = lambda n: doc_href(n, lang)                     # noqa: E731
    have = lambda n: has_doc(n, lang)                      # noqa: E731

    def lang_url(code):
        # Языка, на котором документа нет, в переключателе не прячем: читатель
        # ищет свой язык, а не этот документ. Ведём в библиотеку его языка.
        if has_doc(num, code):
            return doc_href(num, code)
        return '/documents/%s/index.html' % code

    return '\n'.join([
        head_html(num, doc['title'], read_wrapper(num, lang), lang),
        '<body>',
        chrome.header_html(lang, doc_href=href, lang_url=lang_url,
                           home_url='/%s/' % lang, has_doc=have, active_doc=num),
        '<main class="%s" id="main">' % ROOT,
        '<div class="sheet">',
        head, toc, body,
        '</div>',
        prev_next_html(num, titles, lang),
        '</main>',
        chrome.footer_html(lang, doc_href=href, has_doc=have),
        UMAMI,
        '</body>',
        '</html>',
        '',
    ])


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

    if THEME == 'v2':
        return doc, build_doc_v2(num, doc, head, toc, body, titles, lang)

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
    # Недостающие документы дописываются, а не только переименовываются.
    # Раньше эта функция умела лишь править существующие строки, и всякий
    # новый документ приходилось вносить в девять файлов руками. Так и вышло:
    # 2026-08-23 обход показал, что «Гражданского голоса» нет ни в одной
    # библиотеке, а семи языкам не хватает ещё трёх документов - 17, 20 и 32,
    # которые появились у них позже, чем собиралась библиотека. Список
    # строится из CHAIN и has_doc, то есть из тех же двух источников, что и
    # меню: третьему списку взяться неоткуда.
    have = set(re.findall(r'<span class="n">(\d\d)</span>', out))
    want = [n for n in CHAIN if has_doc(n, lang) and n in titles]
    added = [n for n in want if n not in have]
    for num in sorted(added):
        row = ('    <li><a href="%s"><span class="n">%s</span>'
               '<span class="t">%s</span></a></li>\n'
               % (doc_href(num, lang), num,
                  html.escape(titles[num], quote=False)))
        later = [(m.start(), m.group(1))
                 for m in re.finditer(r'    <li><a href="[^"]*">'
                                      r'<span class="n">(\d\d)</span>', out)
                 if m.group(1) > num]
        if later:
            out = out[:later[0][0]] + row + out[later[0][0]:]
        else:
            k = out.rindex('</ul>')
            out = out[:k] + row + out[k:]
    if added:
        changed.extend((n, '', titles[n]) for n in sorted(added))

    # Снятые документы вычёркиваются. Зеркало предыдущего куска: научив
    # библиотеку дописывать недостающее, легко забыть, что документ может и
    # уйти. 2026-08-25 ушёл документ 17, и сборка встала на проверке ниже -
    # проверка сработала, но чинить её было нечем. Список тот же: CHAIN и
    # has_doc. Страница документа при этом не пропадает бесследно - её адрес
    # ведёт в преемника, см. RETIRED и write_redirect_map.
    gone = sorted(have - set(want))
    for num in gone:
        out = re.sub(r'\s*<li><a href="[^"]*"><span class="n">%s</span>'
                     r'<span class="t">[^<]*</span></a></li>' % num, '', out)
        changed.append((num, u'снят с корпуса', u''))

    n_now = len(re.findall(r'<span class="n">\d\d</span>', out))
    assert n_now == len(want), (
        'в библиотеке %s стало %d записей, а документов у языка %d'
        % (lang, n_now, len(want)))

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

    # Снятые документы: оба их адреса, числовой и смысловой, ведут на документ,
    # куда переехало содержание. Если у языка того документа ещё нет - в
    # библиотеку этого языка: оглавление на своём языке лучше, чем 404.
    for num in sorted(RETIRED):
        to = RETIRED[num]['to']
        for lang in sorted(RETIRED[num]['slugs']):
            target = (doc_href(to, lang) if has_doc(to, lang)
                      else '/documents/%s/' % lang)
            lines.append('/documents/%s/%s%s.html %s;' % (lang, lang, num, target))
            lines.append('/documents/%s/%s%s-%s.html %s;'
                         % (lang, lang, num, RETIRED[num]['slugs'][lang], target))
            n += 2
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


HREF_RE = re.compile(
    r'<link rel="alternate" hreflang="([a-z]{2})" href="([^"]+)">')


def check_hreflang(quiet=False):
    """Не устарели ли hreflang на уже собранных страницах других языков.

    Ловушка, на которую мы уже наступили. Когда немецкий получил смысловые
    слаги, пересобрали только немецкие страницы - а hreflang перечисляет все
    девять языков, и он живёт в КАЖДОЙ странице каждого языка. В итоге 49
    русских и английских страниц полгода указывали на немецкие адреса вида
    de05.html, которые отдают 301 на de05-charta.html. Поисковик такие
    аннотации может просто не засчитать.

    Отсюда правило: слаги нового языка - это пересборка ВСЕХ языков, а не
    одного. Проверка нужна потому, что забыть это правило легче, чем помнить.
    """
    bad = []
    for lang in ALL_LANGS:
        d = os.path.join(SITE, 'documents', lang)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith('.html') or name == 'index.html':
                continue
            path = os.path.join(d, name)
            s = io.open(path, encoding='utf-8').read()
            m = re.match(r'^[a-z]{2}(\d\d)', name)
            if not m:
                continue
            num = m.group(1)
            for alt, href in HREF_RE.findall(s):
                want = ORIGIN + doc_href(num, alt)
                if alt in SLUGS and href != want:
                    bad.append((lang, name, alt, href, want))
    if bad and not quiet:
        sys.stderr.write(
            'ВНИМАНИЕ: устаревших hreflang: %d. Слаги языка меняют ссылки во '
            'ВСЕХ языках - пересоберите остальные (--lang <язык> all) или, если '
            'мастеров у языка ещё нет, почините точечно: --fix-hreflang\n'
            % len(bad))
        for row in bad[:5]:
            sys.stderr.write('  %s/%s: hreflang=%s -> %s, ожидается %s\n' % row)
        if len(bad) > 5:
            sys.stderr.write('  ... и ещё %d\n' % (len(bad) - 5))
    return bad


def fix_hreflang(dry=False):
    """Починить устаревшие hreflang там, где пересобрать страницу нечем.

    У шести языков (es, fr, zh, ar, hi, ka) мастеров .md нет - их страницы
    достались от прежнего конвейера и переедут вместе с переводом корпуса. До
    тех пор пересборка им недоступна, а неверный hreflang живёт уже сейчас.
    Правка узкая: меняется только адрес внутри самой аннотации, к тексту
    страницы не притрагиваемся.
    """
    bad = check_hreflang(quiet=True)
    by_file = {}
    for lang, name, alt, href, want in bad:
        by_file.setdefault((lang, name), []).append((alt, href, want))
    n = 0
    for (lang, name), fixes in sorted(by_file.items()):
        path = os.path.join(SITE, 'documents', lang, name)
        s = io.open(path, encoding='utf-8').read()
        before = s
        for alt, href, want in fixes:
            old = '<link rel="alternate" hreflang="%s" href="%s">' % (alt, href)
            new = '<link rel="alternate" hreflang="%s" href="%s">' % (alt, want)
            assert old in s, 'не нашёл аннотацию в %s: %s' % (path, old)
            s = s.replace(old, new)
        if s != before:
            if not dry:
                io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
            n += 1
    return n, len(bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docs', nargs='*', help='номера документов или all')
    ap.add_argument('--css', action='store_true', help='пересобрать только CSS')
    ap.add_argument('--dry', action='store_true', help='не писать файлы')
    ap.add_argument('--lang', default='ru', help='язык сборки (по умолчанию ru)')
    ap.add_argument('--theme', default='legacy', choices=('legacy', 'v2'),
                    help='оформление: legacy - боевой сайт, v2 - новый '
                         '(пишет в _v2/documents/<lang>/)')
    ap.add_argument('--fix-hreflang', action='store_true',
                    help='починить устаревшие hreflang в страницах языков, '
                         'у которых нет мастеров, и выйти')
    a = ap.parse_args()
    if a.fix_hreflang:
        n, total = fix_hreflang(a.dry)
        print('hreflang   починено страниц: %d, аннотаций: %d' % (n, total))
        return
    global THEME
    THEME = a.theme
    lang = a.lang
    md, docs = md_dir(lang), docs_dir(lang)
    assert os.path.isdir(md), 'нет мастеров языка %r: %s' % (lang, md)
    assert lang in SLUGS, (
        'для языка %r не заданы слаги в SLUGS. Без них страницы лягут по '
        'числовым адресам, а перелинковка внутри документов ведёт на '
        'смысловые - получатся битые ссылки.' % lang)

    if THEME == 'v2':
        # Каталог создаём сами: в отличие от боевого дерева, его ещё нет.
        if not os.path.isdir(docs) and not a.dry:
            os.makedirs(docs)
        assert os.path.isdir(os.path.join(SITE, '_v2', 'css')), (
            'нет _v2/css - собирать страницы новой темы не с чем')
    else:
        assert os.path.isdir(docs), 'нет каталога страниц языка %r: %s' % (lang, docs)
        n = build_css()
        print('CSS  css/docs-statute.css  %d байт' % n)
        if a.css:
            return
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

    if THEME == 'v2':
        # Библиотека, карта редиректов и doc-slugs.js - файлы боевого дерева.
        # Новая тема их не трогает: пока сайты живут рядом, правка общих файлов
        # из черновиковой сборки означала бы, что черновик меняет боевой сайт.
        print('тема v2: библиотека, карта редиректов и doc-slugs.js не трогались')
        return

    for num, old, new in sync_library(titles, a.dry, lang):
        print('библиотека %s%s: %s  ->  %s' % (lang, num, old, new))

    if not a.dry:
        n = write_redirect_map()
        print('редиректы  nginx/redirects-docs.map  строк: %d' % n)
        write_slug_module()
        print('слаги      js/modern/shared/doc-slugs.js')

    bad = check_hreflang()
    print('hreflang   проверено дерево documents/, устаревших: %d' % len(bad))


if __name__ == '__main__':
    main()
