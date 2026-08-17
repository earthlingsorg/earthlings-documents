# -*- coding: utf-8 -*-
u"""Обвязка нового сайта: шапка с меню и переключателем языка, подвал.

Три решения, ради которых этот модуль существует.

1. Обвязка - статический HTML, а не разметка, нарисованная скриптом.
   На боевом сайте меню рисует earth-navigation в браузере. Отсюда пустые
   языковые главные для поисковика: в `index.html` 36 КБ, а видимого текста
   без JS 3156 символов, по-английски, на странице для девяти языков. Здесь
   все ссылки лежат в HTML, и краулер видит их без единого байта скрипта.

2. Меню порождается из тех же таблиц, что и страницы.
   17 августа 2026 список языков документа разошёлся между сборщиком
   (LANGS_BY_DOC) и меню (langs в constants.js): немецкий читатель не мог
   дойти по меню до документов 17, 20 и 32, английский - до 17 и 20, хотя все
   пять страниц отдавали 200. Здесь список приходит от сборщика, второго
   источника нет.

3. Подписи берутся из живых переводов сайта, а не копируются сюда.
   Тот же файл `js/modern/translations/<язык>.json`, что и у боевого сайта.
   Ключа нет - сборка ПАДАЕТ. Молчаливая подстановка русского слова и есть то,
   из-за чего немецкое меню месяц показывало «Учредительный период».

Раскрывающиеся списки сделаны на <details>: они работают без скрипта, ходятся
с клавиатуры и озвучиваются экранными читалками как есть. JavaScript в обвязке
нужен ровно на две вещи - закрыть открытое по клику вне и по Escape.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(os.path.dirname(HERE)), 'earth-lings-site')
TRANS_DIR = os.path.join(SITE, 'js', 'modern', 'translations')

ALL_LANGS = ['ru', 'en', 'es', 'de', 'fr', 'zh', 'ar', 'hi', 'ka']
RTL = ('ar',)

# Порядок и состав меню. Повторяет NAVIGATION_DATA боевого сайта; когда новый
# сайт заменит старый, constants.js уходит, и эта таблица остаётся одна.
# Пока живут обе - их сверяет check_nav_sync.py.
SECTIONS = [
    (u'nav.declaration', '01', []),
    (u'nav.legal_base', None, [
        (u'nav.protocol', '05'),
        (u'nav.legal_basis', '04'),
        (u'nav.faq_legal', '26'),
        (u'nav.legal_gap', '30'),
        (u'nav.legal_info', '22'),
    ]),
    (u'nav.structure', None, [
        (u'nav.platform', '12'),
        (u'nav.dao', '07'),
        (u'nav.honeycombs', '08'),
        (u'nav.fund', '09'),
        (u'nav.earthlings_coin', '10'),
        (u'nav.council', '11'),
    ]),
    (u'nav.participation', None, [
        (u'nav.path', '14'),
        (u'nav.sbt_passport', '15'),
        (u'nav.ethics', '03'),
        (u'nav.faq_general', '27'),
    ]),
    (u'nav.development', None, [
        (u'nav.roadmap', '19'),
        (u'nav.founding_period', '20'),
        (u'nav.where_we_are_doc', '32'),
        (u'nav.whats_next', '17'),
        (u'nav.working_agenda', '31'),
        (u'nav.about_us', '23'),
    ]),
]

FOOTER_DOCS = [(u'footer.privacy', '28'), (u'footer.terms', '29'),
               (u'nav.biometry', '16')]

# Подписи языков в переводах не лежат: язык называется на своём языке всегда,
# независимо от того, с какой страницы на него смотрят.
LANG_LABEL = {'ru': u'Русский', 'en': u'English', 'es': u'Español',
              'de': u'Deutsch', 'fr': u'Français', 'zh': u'中文',
              'ar': u'العربية', 'hi': u'हिन्दी', 'ka': u'ქართული'}

# Единственные строки, которых в переводах сайта нет. Держим список коротким
# намеренно: zh, ar, hi и ka ждут носительской вычитки, и каждое новое слово -
# это ещё одна строка, которую придётся выверять.
EXTRA = {
    'menu': {'ru': u'Меню', 'en': u'Menu', 'es': u'Menú', 'de': u'Menü',
             'fr': u'Menu', 'zh': u'菜单', 'ar': u'القائمة', 'hi': u'मेनू',
             'ka': u'მენიუ'},
    'all_docs': {'ru': u'Все документы', 'en': u'All documents',
                 'es': u'Todos los documentos', 'de': u'Alle Dokumente',
                 'fr': u'Tous les documents', 'zh': u'全部文件',
                 'ar': u'جميع الوثائق', 'hi': u'सभी दस्तावेज़',
                 'ka': u'ყველა დოკუმენტი'},
    # Взято из EarthFooter.js боевого сайта, а не переведено заново.
    'verify': {'ru': u'Проверить подлинность', 'en': u'Verify authenticity',
               'es': u'Verificar autenticidad', 'de': u'Echtheit prüfen',
               'fr': u"Vérifier l'authenticité", 'zh': u'验证真实性',
               'ar': u'التحقق من الأصالة', 'hi': u'प्रामाणिकता सत्यापित करें',
               'ka': u'ავთენტურობის შემოწმება'},
    # Из EarthNavigation.getNavAriaLabel.
    'main_nav': {'ru': u'Основная навигация', 'en': u'Main navigation',
                 'es': u'Navegación principal', 'de': u'Hauptnavigation',
                 'fr': u'Navigation principale', 'zh': u'主导航',
                 'ar': u'التنقل الرئيسي', 'hi': u'मुख्य नेविगेशन',
                 'ka': u'მთავარი ნავიგაცია'},
    # Из INLINE_TEXTS.lang_switcher_label в constants.js.
    'lang_switcher': {'ru': u'Выбор языка', 'en': u'Choose language',
                      'es': u'Elegir idioma', 'de': u'Sprache wählen',
                      'fr': u'Choisir la langue', 'zh': u'选择语言',
                      'ar': u'اختر اللغة', 'hi': u'भाषा चुनें',
                      'ka': u'აირჩიეთ ენა'},
    # Ссылка «к содержанию» для тех, кто ходит клавиатурой. На боевом сайте её
    # нет ни на одной странице: до текста документа надо протыкать всё меню.
    'skip': {'ru': u'К содержанию', 'en': u'Skip to content',
             'es': u'Ir al contenido', 'de': u'Zum Inhalt springen',
             'fr': u'Aller au contenu', 'zh': u'跳到主要内容',
             'ar': u'تخطي إلى المحتوى', 'hi': u'मुख्य सामग्री पर जाएँ',
             'ka': u'გადასვლა შიგთავსზე'},
    # Ссылка с полосы главной на полный текст.
    'read_more': {'ru': u'Читать целиком', 'en': u'Read in full',
                  'es': u'Leer completo', 'de': u'Vollständig lesen',
                  'fr': u'Lire en entier', 'zh': u'阅读全文',
                  'ar': u'قراءة النص كاملا', 'hi': u'पूरा पढ़ें',
                  'ka': u'სრულად წაკითხვა'},
}

CTA_URL = 'https://id.earth-lings.org/verification?lang=%s'
APP_URL = 'https://app.earth-lings.org?lang=%s'
MAIL = 'info@earth-lings.org'          # в footer.email лежит несуществующий
TG = 'https://t.me/earthlings_net'     # earthlings.global - не брать оттуда

_cache = {}


def _trans(lang):
    if lang not in _cache:
        path = os.path.join(TRANS_DIR, lang + '.json')
        assert os.path.isfile(path), (
            u'нет файла переводов %s - обвязку не из чего собирать' % path)
        d = json.load(io.open(path, encoding='utf-8'))
        flat = {}
        for sec, body in d.items():
            if isinstance(body, dict):
                for k, v in body.items():
                    if not isinstance(v, dict):
                        flat['%s.%s' % (sec, k)] = v
            else:
                flat[sec] = body
        assert flat, u'файл переводов %s пуст' % path
        _cache[lang] = flat
    return _cache[lang]


def t(lang, key):
    u"""Подпись из переводов сайта. Нет ключа - падаем.

    Именно молчаливый откат к русскому слову и был причиной того, что немецкое
    меню показывало «Учредительный период». Пусть лучше не соберётся.
    """
    v = _trans(lang).get(key)
    assert v, (u'нет ключа %s в js/modern/translations/%s.json - без него '
               u'пункт меню соберётся на чужом языке' % (key, lang))
    return v


def x(lang, key):
    v = EXTRA[key].get(lang)
    assert v, u'нет строки %r для языка %r в EXTRA' % (key, lang)
    return v


def esc(s):
    return (s.replace(u'&', u'&amp;').replace(u'<', u'&lt;')
             .replace(u'>', u'&gt;').replace(u'"', u'&quot;'))


# ------------------------------------------------------------------- шапка

def header_html(lang, doc_href, lang_url, home_url=None, has_doc=None,
                active_doc=None):
    u"""Шапка страницы.

    doc_href(num)   -> адрес документа num на текущем языке
    lang_url(code)  -> адрес ЭТОЙ ЖЕ страницы на языке code
    has_doc(num)    -> есть ли документ num на текущем языке (по таблице
                       сборщика; пункта, которого нет, в меню не будет)
    """
    assert lang in ALL_LANGS, u'неизвестный язык %r' % lang
    has_doc = has_doc or (lambda num: True)
    home = home_url or ('/%s/' % lang)
    o = []
    a = o.append

    a(u'<a class="skip" href="#main">%s</a>' % esc(x(lang, 'skip')))
    a(u'<header class="hdr">')
    a(u'<div class="hdr-in">')
    a(u'<a class="brand" href="%s">'
      u'<img src="/images/logo-sm.webp" alt="Earthlings" width="40" height="40" '
      u'decoding="async">'
      u'<span class="brand-name">Earthlings</span></a>' % esc(home))

    # Бургер. На широком экране раскрыт всегда - это делает CSS, а не скрипт.
    a(u'<details class="burger">')
    a(u'<summary class="burger-btn" aria-label="%s">'
      u'<span class="burger-ico" aria-hidden="true"></span></summary>'
      % esc(x(lang, 'menu')))
    a(u'<div class="hdr-body">')

    a(u'<nav class="nav" aria-label="%s">' % esc(x(lang, 'main_nav')))
    a(u'<ul class="nav-list">')
    for key, num, items in SECTIONS:
        if num is not None:
            if not has_doc(num):
                continue
            cur = u' aria-current="page"' if num == active_doc else u''
            a(u'<li class="nav-item"><a class="nav-link" href="%s"%s>%s</a></li>'
              % (esc(doc_href(num)), cur, esc(t(lang, key))))
            continue
        live = [(k, n) for k, n in items if has_doc(n)]
        if not live:
            continue
        # Атрибута open у раздела с текущим документом нет намеренно: на
        # широком экране список раскрывается поверх страницы, и раскрытым при
        # загрузке он бы закрывал собой текст. Текущий пункт отмечен внутри
        # через aria-current, этого достаточно.
        here = u' nav-item--here' if active_doc in [n for _, n in live] else u''
        a(u'<li class="nav-item%s"><details class="dd">' % here)
        a(u'<summary class="nav-link">%s<span class="caret" aria-hidden="true">'
          u'</span></summary>' % esc(t(lang, key)))
        a(u'<ul class="dd-list">')
        for k, n in live:
            cur = u' aria-current="page"' if n == active_doc else u''
            a(u'<li><a href="%s"%s>%s</a></li>'
              % (esc(doc_href(n)), cur, esc(t(lang, k))))
        a(u'</ul></details></li>')
    a(u'</ul></nav>')

    # У epic справа от меню стоит одна кнопка - DONATE. У нас их было четыре
    # плюс две иконки соцсетей, и пять русских пунктов прописными рядом с ними
    # в строку не помещались. «Платформа», «Пробуждённый код», почта и Telegram
    # переехали в подвал; в шапке остались язык и главное действие.
    a(u'<div class="hdr-acts">')

    # Переключатель языка - настоящие ссылки, а не скрипт. На боевом сайте он
    # перезагружает страницу из JS, и связей между языковыми версиями в HTML
    # нет вообще: поисковик знает о них только из hreflang.
    a(u'<details class="dd dd--lang">')
    a(u'<summary class="act-link" aria-label="%s">%s'
      u'<span class="caret" aria-hidden="true"></span></summary>'
      % (esc(x(lang, 'lang_switcher')), lang.upper()))
    a(u'<ul class="dd-list dd-list--lang">')
    for code in ALL_LANGS:
        cur = u' aria-current="true"' if code == lang else u''
        a(u'<li><a href="%s" hreflang="%s" lang="%s"%s%s>%s</a></li>'
          % (esc(lang_url(code)), code, code,
             u' dir="rtl"' if code in RTL else u'', cur, esc(LANG_LABEL[code])))
    a(u'</ul></details>')

    a(u'<a class="cta" href="%s">%s</a>'
      % (CTA_URL % lang, esc(t(lang, 'nav.become_earthling'))))
    a(u'</div>')       # hdr-acts
    a(u'</div>')       # hdr-body
    a(u'</details>')   # burger
    a(u'</div></header>')
    return u'\n'.join(o)


# ------------------------------------------------------------------- подвал

def footer_html(lang, doc_href, has_doc=None):
    assert lang in ALL_LANGS, u'неизвестный язык %r' % lang
    has_doc = has_doc or (lambda num: True)
    o = []
    a = o.append

    a(u'<footer class="ftr">')
    a(u'<div class="ftr-in">')

    a(u'<div class="ftr-col ftr-col--brand"><span class="brand-name">Earthlings'
      u'</span></div>')

    a(u'<div class="ftr-col"><h2 class="ftr-h">%s</h2><ul class="ftr-list">'
      % esc(t(lang, 'footer.documents')))
    a(u'<li><a href="/documents/%s/index.html">%s</a></li>'
      % (lang, esc(x(lang, 'all_docs'))))
    for key, num in FOOTER_DOCS:
        if has_doc(num):
            a(u'<li><a href="%s">%s</a></li>'
              % (esc(doc_href(num)), esc(t(lang, key))))
    a(u'</ul></div>')

    a(u'<div class="ftr-col"><h2 class="ftr-h">%s</h2><ul class="ftr-list">'
      % esc(t(lang, 'nav.platform_btn')))
    a(u'<li><a href="%s">%s</a></li>'
      % (APP_URL % lang, esc(t(lang, 'nav.platform_btn'))))
    a(u'<li><a href="/awakened_code/">%s</a></li>'
      % esc(t(lang, 'nav.awakened_code')))
    a(u'<li><a href="/verification/">%s</a></li>' % esc(x(lang, 'verify')))
    a(u'</ul></div>')

    a(u'<div class="ftr-col"><h2 class="ftr-h">%s</h2><ul class="ftr-list">'
      % esc(t(lang, 'footer.contact')))
    a(u'<li><a href="mailto:%s">%s</a></li>' % (MAIL, MAIL))
    a(u'<li><a href="%s" rel="noopener">Telegram</a></li>' % TG)
    a(u'</ul></div>')

    a(u'</div>')

    # «Все права защищены» из footer.copyright не берём: корпус открыт
    # намеренно, и такая строка ему противоречит. Права - в документе 22.
    a(u'<div class="ftr-bottom"><span>© Earthlings</span>')
    if has_doc('22'):
        a(u'<a href="%s">%s</a>' % (esc(doc_href('22')),
                                    esc(t(lang, 'nav.legal_info'))))
    a(u'</div>')
    a(u'</footer>')
    return u'\n'.join(o)
