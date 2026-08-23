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
    ]),
    (u'nav.structure', None, [
        (u'nav.platform', '12'),
        (u'nav.dao', '07'),
        (u'nav.honeycombs', '08'),
        (u'nav.fund', '09'),
        (u'nav.earthlings_coin', '10'),
        (u'nav.council', '11'),
    ]),
    # «Развитие» слито с «Участием» (решение Артура 2026-08-23): пять пунктов
    # верхнего уровня перестали читаться как пять разделов, а по составу
    # «развитие» и было участием на разных сроках - что можно предложить
    # сейчас, что решается, что построено, куда идёт. Единственная запись,
    # которая рассказывала про нас, а не про участие читателя, - «О нас», и
    # она ушла в подвал. Порядок внутри - от «войти» к «куда идём».
    (u'nav.participation', None, [
        (u'nav.path', '14'),
        (u'nav.sbt_passport', '15'),
        (u'nav.founding_period', '20'),
        (u'nav.working_agenda', '31'),
        (u'nav.where_we_are_doc', '32'),
        (u'nav.roadmap', '19'),
        (u'nav.ethics', '03'),
        (u'nav.faq_general', '27'),
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
    # Ссылка с полосы Awakened Code. Не «читать целиком»: там не текст, а
    # отдельная работающая страница со своей бегущей строкой и лентами эссе,
    # и звать её «прочитать» неточно.
    'open_site': {'ru': u'Перейти', 'en': u'Open', 'es': u'Abrir',
                  'de': u'Öffnen', 'fr': u'Ouvrir', 'zh': u'前往',
                  'ar': u'انتقال', 'hi': u'खोलें', 'ka': u'გახსნა'},
    # Подписи ссылок полос главной. По одной на полосу: каждая называет своё
    # действие, а не повторяет соседнее. Переводы машинные, ждут вычитки.
    'read_manifesto': {'ru': u'Читать Манифест', 'en': u'Read the Manifesto',
                       'es': u'Leer el Manifiesto', 'de': u'Manifest lesen',
                       'fr': u'Lire le Manifeste', 'zh': u'阅读《归属宣言》',
                       'ar': u'قراءة بيان الانتماء', 'hi': u'घोषणापत्र पढ़ें',
                       'ka': u'მანიფესტის წაკითხვა'},
    'read_declaration': {'ru': u'Читать Декларацию', 'en': u'Read the Declaration',
                         'es': u'Leer la Declaración', 'de': u'Erklärung lesen',
                         'fr': u'Lire la Déclaration', 'zh': u'阅读《自决宣言》',
                         'ar': u'قراءة الإعلان', 'hi': u'घोषणा पढ़ें',
                         'ka': u'დეკლარაციის წაკითხვა'},
    'rules_and_dates': {'ru': u'Правила и сроки', 'en': u'Rules and dates',
                        'es': u'Reglas y plazos', 'de': u'Regeln und Fristen',
                        'fr': u'Règles et échéances', 'zh': u'规则与时间',
                        'ar': u'القواعد والمواعيد', 'hi': u'नियम और तिथियाँ',
                        'ka': u'წესები და ვადები'},
    'what_passport_gives': {'ru': u'Что даёт паспорт',
                            'en': u'What the passport gives',
                            'es': u'Qué da el pasaporte',
                            'de': u'Was der Pass gibt',
                            'fr': u'Ce que donne le passeport',
                            'zh': u'护照带来什么', 'ar': u'ماذا يمنح الجواز',
                            'hi': u'पासपोर्ट क्या देता है',
                            'ka': u'რას იძლევა პასპორტი'},
    'about_joining': {'ru': u'Подробно о вступлении', 'en': u'More about joining',
                      'es': u'Más sobre la incorporación',
                      'de': u'Mehr zum Beitritt',
                      'fr': u"En savoir plus sur l'adhésion",
                      'zh': u'关于加入的详情', 'ar': u'تفاصيل الانضمام',
                      'hi': u'शामिल होने के बारे में',
                      'ka': u'ვრცლად შემოერთებაზე'},
    'how_platform_works': {'ru': u'Как устроена платформа',
                           'en': u'How the platform works',
                           'es': u'Cómo funciona la plataforma',
                           'de': u'Wie die Plattform funktioniert',
                           'fr': u'Comment fonctionne la plateforme',
                           'zh': u'平台如何运作', 'ar': u'كيف تعمل المنصة',
                           'hi': u'मंच कैसे काम करता है',
                           'ka': u'როგორ მუშაობს პლატფორმა'},
    'verify_yourself': {'ru': u'Проверить самим', 'en': u'Check it yourself',
                        'es': u'Compruébelo usted mismo',
                        'de': u'Selbst nachprüfen', 'fr': u'Vérifier soi-même',
                        'zh': u'自行验证', 'ar': u'تحقق بنفسك',
                        'hi': u'स्वयं जाँचें', 'ka': u'შეამოწმეთ თავად'},
    'all_objections': {'ru': u'Все возражения и ответы',
                       'en': u'All objections and answers',
                       'es': u'Todas las objeciones y respuestas',
                       'de': u'Alle Einwände und Antworten',
                       'fr': u'Toutes les objections et réponses',
                       'zh': u'全部质疑与回应',
                       'ar': u'جميع الاعتراضات والردود',
                       'hi': u'सभी आपत्तियाँ और उत्तर',
                       'ka': u'ყველა შენიშვნა და პასუხი'},
    # Подпись лицензии в подвале. Ведёт на разъяснение CC на языке страницы.
    'corpus_licence': {'ru': u'Тексты корпуса - CC BY 4.0',
                       'en': u'Corpus texts: CC BY 4.0',
                       'de': u'Texte des Korpus: CC BY 4.0',
                       'es': u'Textos del corpus: CC BY 4.0',
                       'fr': u'Textes du corpus: CC BY 4.0',
                       'zh': u'文集文本：CC BY 4.0',
                       'ar': u'نصوص المجموعة: CC BY 4.0',
                       'hi': u'संग्रह के पाठ: CC BY 4.0',
                       'ka': u'კორპუსის ტექსტები: CC BY 4.0'},
    # Ссылка с полосы главной на полный текст.
    'read_more': {'ru': u'Читать целиком', 'en': u'Read in full',
                  'es': u'Leer completo', 'de': u'Vollständig lesen',
                  'fr': u'Lire en entier', 'zh': u'阅读全文',
                  'ar': u'قراءة النص كاملا', 'hi': u'पूरा पढ़ें',
                  'ka': u'სრულად წაკითხვა'},
    # Кнопка на полосе платформы: экран сам перелистывает туры по кругу, и
    # смену надо уметь остановить. Это не украшение, а требование: содержимое,
    # которое обновляется само дольше пяти секунд, обязано иметь способ
    # остановки (WCAG 2.2.2). Подпись меняется на 'resume', когда остановлено.
    'pause': {'ru': u'Остановить показ', 'en': u'Pause the slideshow',
              'es': u'Pausar la presentación', 'de': u'Vorführung anhalten',
              'fr': u'Mettre en pause', 'zh': u'暂停播放',
              'ar': u'إيقاف العرض مؤقتا', 'hi': u'प्रदर्शन रोकें',
              'ka': u'ჩვენების შეჩერება'},
    'resume': {'ru': u'Продолжить показ', 'en': u'Resume the slideshow',
               'es': u'Reanudar la presentación', 'de': u'Vorführung fortsetzen',
               'fr': u'Reprendre la lecture', 'zh': u'继续播放',
               'ar': u'متابعة العرض', 'hi': u'प्रदर्शन जारी रखें',
               'ka': u'ჩვენების გაგრძელება'},
}

CTA_URL = 'https://id.earth-lings.org/verification?lang=%s'
APP_URL = 'https://app.earth-lings.org?lang=%s'
# Строка прав в подвале. Знак копирайта уместен: авторские права на тексты
# действительно принадлежат, и CC BY 4.0 - лицензия поверх них, а не отказ
# от них. А вот «all rights reserved», которое стояло здесь 2026-08-23,
# снято: LICENSE корпуса разрешает копировать, переводить, переиздавать и
# цитировать документы, в том числе коммерчески, - и читатель подвала
# делал бы прямо обратный вывод. Оговорка Буэнос-Айресской конвенции
# юридически ничего не добавляет с тех пор, как все страны, которых это
# касалось, вошли в Бернскую.
COPYRIGHT = u'© 2025-2026 Earthlings'
CC_DEED = 'https://creativecommons.org/licenses/by/4.0/deed.%s'

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
    # Слово впереди, знак за ним - решение Артура 2026-08-22. Порядок в
    # разметке, а не через order в CSS: так его слышит и читалка, и
    # перестановка не разъезжается с тем, что видно глазом.
    a(u'<a class="brand" href="%s">'
      u'<span class="brand-name">Earthlings</span>'
      u'<img src="/images/logo-sm.webp" alt="" width="59" height="59" '
      u'decoding="async"></a>' % esc(home))

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
        a(u'<summary class="nav-link">%s</summary>' % esc(t(lang, key)))
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
    a(u'<summary class="act-link" aria-label="%s">%s</summary>'
      % (esc(x(lang, 'lang_switcher')), lang.upper()))
    a(u'<ul class="dd-list dd-list--lang">')
    for code in ALL_LANGS:
        cur = u' aria-current="true"' if code == lang else u''
        a(u'<li><a href="%s" hreflang="%s" lang="%s"%s%s>%s</a></li>'
          % (esc(lang_url(code)), code, code,
             u' dir="rtl"' if code in RTL else u'', cur, esc(LANG_LABEL[code])))
    a(u'</ul></details>')

    # Кнопки «Вступить» в шапке больше нет (решение Артура 2026-08-22):
    # то же действие стоит на полосе «Путь earthling», и держать его в
    # двух местах значит спрашивать дважды об одном.
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

    # Слева не логотип, а строка прав (решение Артура 2026-08-23). Прежде там
    # стояло слово «Earthlings» переливом - второй раз на странице, после
    # шапки, и без своей работы: подвал и так подписан.
    a(u'<div class="ftr-col ftr-col--brand"><p class="ftr-copy">%s<br>'
      u'<a href="%s" rel="license noopener">%s</a></p></div>'
      % (esc(COPYRIGHT), CC_DEED % lang, esc(x(lang, 'corpus_licence'))))

    # Колонка называется «Политики», а не «Документы»: в ней и лежат только
    # политики - конфиденциальности, пользования и биометрической проверки.
    # Ссылка «Все документы» снята: библиотека достижима из меню и из цепочки
    # чтения на каждой странице документа.
    a(u'<div class="ftr-col"><h2 class="ftr-h">%s</h2><ul class="ftr-list">'
      % esc(t(lang, 'footer.policies')))
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
    a(u'</ul></div>')

    a(u'<div class="ftr-col"><h2 class="ftr-h">%s</h2><ul class="ftr-list">'
      % esc(t(lang, 'footer.contact')))
    if has_doc('23'):
        a(u'<li><a href="%s">%s</a></li>'
          % (esc(doc_href('23')), esc(t(lang, 'nav.about_us'))))
    a(u'<li><a href="mailto:%s">%s</a></li>' % (MAIL, MAIL))
    a(u'<li><a href="%s" rel="noopener">Telegram</a></li>' % TG)
    a(u'</ul></div>')

    a(u'</div>')

    # Строка прав переехала наверх, в левую колонку, поэтому здесь её больше
    # нет - остаётся только ссылка на юридическую информацию, единственный
    # её адрес после того, как она ушла из меню.
    a(u'<div class="ftr-bottom">')
    if has_doc('22'):
        a(u'<a href="%s">%s</a>' % (esc(doc_href('22')),
                                    esc(t(lang, 'nav.legal_info'))))
    a(u'</div>')
    a(u'</footer>')
    return u'\n'.join(o)
