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

3. Подписи берутся из таблицы переводов, а не копируются сюда.
   `_v2/i18n/<язык>.json`. Ключа нет - сборка ПАДАЕТ. Молчаливая подстановка
   русского слова и есть то, из-за чего немецкое меню месяц показывало
   «Учредительный период». До 2026-08-25 таблица читалась из боевого дерева,
   `js/modern/translations/`, и это был необъявленный блокер подмены: в день
   замены корня каталог исчезает, и обвязка перестаёт собираться.

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
# Подписи меню лежат в дереве НОВОГО сайта, а не боевого. До 2026-08-25 они
# читались из js/modern/translations/ - каталога, который исчезнет вместе с
# боевым сайтом в день подмены, и обвязка перестала бы собираться. Копия
# сделана один раз; расходиться ей не с чем, потому что боевое дерево с того
# же дня заморожено и не правится.
TRANS_DIR = os.path.join(SITE, '_v2', 'i18n')

ALL_LANGS = ['ru', 'en', 'es', 'de', 'fr', 'zh', 'ar', 'hi', 'ka']
RTL = ('ar',)

# Порядок и состав меню. Повторяет NAVIGATION_DATA боевого сайта; когда новый
# сайт заменит старый, constants.js уходит, и эта таблица остаётся одна.
# Пока живут обе - их сверяет check_nav_sync.py.
SECTIONS = [
    (u'nav.declaration', '01', []),
    # «Гражданский голос» стоит первым, и это не вкус, а правило, записанное
    # строкой выше CHAIN в сборщике: порядок чтения корпуса = порядок главного
    # меню. В цепочке он идёт вторым, сразу за Декларацией и ПЕРЕД Уставом, а
    # раздел «Правовая база» - это ровно та же цепочка без Декларации. Значит
    # без него раздел просто не совпадал с порядком чтения.
    #
    # Решение Артура 2026-08-25. Прежняя попытка поставить документ отдельным
    # пунктом верхнего уровня провалилась по ширине шапки: шестой пункт не
    # собирался при 1248px (французский -52 пикселя, испанский -13). Внутри
    # выпадающего списка этого ограничения нет - панель во всю ширину.
    #
    # Оговорка, которую стоит помнить: это единственный документ раздела,
    # который ничего не устанавливает, и он сам говорит об этом во втором
    # абзаце. Читатель, открывший «Правовую базу», первым встречает текст,
    # который объясняет и предполагает. Порядок чтения считает это верным:
    # без него Устав читается как процедура непонятно чего.
    (u'nav.legal_base', None, [
        (u'nav.civic_voice', '02'),
        (u'nav.protocol', '05'),
        (u'nav.legal_basis', '04'),
        (u'nav.faq_legal', '26'),
        (u'nav.legal_gap', '30'),
    ]),
    # SBT-паспорт стоит первым, и раздел от этого упорядочен по зависимости, а
    # не по порядку чтения (решение Артура 2026-08-25): на паспорте держится
    # всё остальное в этом разделе - голос в DAO, доля в казне, участие в
    # сотах, доступ к платформе. Без него они не работают ни одним пунктом.
    #
    # Цена названа прямо: в цепочке чтения паспорт стоит между «Путём
    # earthling» и «Биометрической верификацией» - вступил, получил, проверился.
    # В меню эта тройка теперь разорвана, и новичок, ищущий «как получить
    # паспорт», пойдёт искать его в «Участии». Цепочка не менялась: «Далее» на
    # страницах по-прежнему читает 14 -> 15 -> 16.
    (u'nav.structure', None, [
        (u'nav.sbt_passport', '15'),
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
    #
    # Правки 2026-08-25: «Этика Earthlings» встала первой, SBT-паспорт ушёл в
    # «Устройство», «Частые вопросы» - в подвал. Раздел от этого открывается не
    # входом, а тем, каковы мы: сначала на что человек соглашается, потом как
    # войти и что решается сейчас.
    (u'nav.participation', None, [
        (u'nav.ethics', '03'),
        (u'nav.path', '14'),
        (u'nav.founding_period', '20'),
        (u'nav.working_agenda', '31'),
        (u'nav.where_we_are_doc', '32'),
        (u'nav.roadmap', '19'),
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
    # Описание страницы библиотеки. Боевые библиотеки его имеют, но у трёх
    # языков там потеряна диакритика («vollstandige», «bibliotheque»,
    # «biblioteca» без ударений) - собраны они были до того, как это стали
    # проверять. Здесь строки написаны заново.
    'library_desc': {
        'ru': u'Полная библиотека документов народа Earthlings: Декларация, '
              u'Устав, правовое обоснование, устройство и экономика.',
        'en': u"The complete library of the Earthlings people's documents: "
              u'the Declaration, the Charter, the legal basis, the structure '
              u'and the economy.',
        'de': u'Die vollständige Dokumentenbibliothek des Volkes der Earthlings: '
              u'die Erklärung, die Charta, die Rechtsgrundlage, der Aufbau und '
              u'die Wirtschaft.',
        'es': u'La biblioteca completa de documentos del pueblo Earthlings: la '
              u'Declaración, la Carta, la base jurídica, la estructura y la '
              u'economía.',
        'fr': u'La bibliothèque complète des documents du peuple des Earthlings: '
              u'la Déclaration, la Charte, la base juridique, la structure et '
              u"l'économie.",
        'zh': u'Earthlings 人民文件的完整文库：《宣言》、宪章、法律依据、组织结构与经济。',
        'ar': u'المكتبة الكاملة لوثائق شعب Earthlings: الإعلان، والميثاق، '
              u'والأساس القانوني، والبنية والاقتصاد.',
        'hi': u'Earthlings जन के दस्तावेज़ों का पूर्ण संग्रह: घोषणा, '
              u'चार्टर, विधिक आधार, संरचना और अर्थव्यवस्था।',
        'ka': u'Earthlings-ის ხალხის დოკუმენტების სრული ბიბლიოთეკა: დეკლარაცია, '
              u'ქარტია, სამართლებრივი საფუძველი, მოწყობა და ეკონომიკა.',
    },
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
    'read_manifesto': {'ru': u'Читать Обращение', 'en': u'Read the Address',
                       'es': u'Leer el mensaje', 'de': u'Ansprache lesen',
                       'fr': u'Lire le message', 'zh': u'阅读《致所有人》',
                       'ar': u'قراءة الرسالة', 'hi': u'संबोधन पढ़ें',
                       'ka': u'მიმართვის წაკითხვა'},
    'read_declaration': {'ru': u'Читать Декларацию', 'en': u'Read the Declaration',
                         'es': u'Leer la Declaración', 'de': u'Erklärung lesen',
                         'fr': u'Lire la Déclaration', 'zh': u'阅读《Earthlings 宣言》',
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
    # Подпись сокращена до одного слова (решение Артура 2026-08-23):
    # «проверить самим» обещало проверку, а ведёт ссылка в документ, где
    # написано, что и как проверяется.
    'verify_yourself': {'ru': u'Изучить', 'en': u'Explore',
                        'es': u'Explorar',
                        'de': u'Ansehen', 'fr': u'Explorer',
                        'zh': u'查看', 'ar': u'استعراض',
                        'hi': u'देखें', 'ka': u'გაცნობა'},
    # Колонка эссе в подвале. Пока пуста: ссылки Артур даст позже, и до тех
    # пор под заголовком ничего нет - см. FOOTER_ESSAYS.
    'essays': {'ru': u'Эссе', 'en': u'Essays', 'de': u'Essays',
               'es': u'Ensayos', 'fr': u'Essais', 'zh': u'随笔',
               'ar': u'مقالات', 'hi': u'निबंध', 'ka': u'ესეები'},
    # Заголовок колонки подвала. Прежде колонка называлась «Платформа», и
    # первой ссылкой под ней стояла «Платформа» - слово дважды подряд.
    'systems': {'ru': u'Системы', 'en': u'Systems', 'de': u'Systeme',
                'es': u'Sistemas', 'fr': u'Systèmes', 'zh': u'系统',
                'ar': u'الأنظمة', 'hi': u'प्रणालियाँ', 'ka': u'სისტემები'},
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
    # Последняя полоса главной: всё предложение и есть кнопка (решение
    # Артура 2026-08-23). Прежде под фразой стояла отдельная кнопка
    # «Вступить», и фраза кончалась словами «открыто для проверки» -
    # текст обещал одно действие, кнопка предлагала другое. Теперь
    # действие названо один раз, и им же кончается фраза.
    #
    # Это единственная строка главной, сочинённая для неё, а не взятая
    # из корпуса. Поэтому она и лежит здесь, среди строк интерфейса, а
    # не собирается из мастера: выдавать её за цитату нельзя.
    # Фраза последней полосы. Кончается на «открыто» и ничего не
    # предлагает сама: с 25 августа рядом стоит кнопка, и звать дважды -
    # значит спорить с собой. Прежний хвост «...и открыто для вступления»
    # был нужен, пока вся фраза была кнопкой.
    # Хранится ДВУМЯ ЧАСТЯМИ, и это не прихоть вёрстки. Артур задал перенос
    # для русского: «Всё, что нужно народу, чтобы действовать,» / «у
    # Earthlings уже построено и открыто». Разрыв стоит на границе между тем,
    # ЧТО нужно, и тем, ГДЕ это есть, - и такая граница есть во всех девяти
    # языках: устройство фразы всюду одно. Поэтому правило общее - разрыв
    # перед сказуемым, - а не русское исключение.
    #
    # Части, а не строка с <br> внутри: разметка в словаре означала бы, что
    # строку нельзя показать нигде, кроме этого места, - ни в письме, ни в
    # заголовке страницы, ни голосом. Собирает её тот, кто показывает.
    'join_line': {
        'ru': [u'Всё, что нужно народу, чтобы действовать,',
               u'у Earthlings уже построено и открыто'],
        'en': [u'Everything a people needs in order to act',
               u'is already built at Earthlings, and it is open'],
        'de': [u'Alles, was ein Volk zum Handeln braucht,',
               u'ist bei Earthlings bereits gebaut und offen'],
        'es': [u'Todo lo que un pueblo necesita para actuar',
               u'ya está construido en Earthlings y está abierto'],
        'fr': [u"Tout ce qu'un peuple doit avoir pour agir",
               u"est déjà construit chez Earthlings et ouvert"],
        'zh': [u'一个人民行动所需要的一切，',
               u'在 Earthlings 已经建成，并且开放'],
        'ar': [u'كل ما يحتاجه الشعب لكي يفعل',
               u'مبنيٌّ عند Earthlings بالفعل ومفتوح'],
        'hi': [u'किसी जन को कार्य करने के लिए जो कुछ चाहिए,',
               u'वह Earthlings में पहले से बना है और खुला है'],
        'ka': [u'ყველაფერი, რაც ხალხს სამოქმედოდ სჭირდება,',
               u'Earthlings-ში უკვე აშენებულია და ღიაა']},
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


# Шрифты, о которых браузеру говорят заранее.
#
# Замер 2026-08-23: стили страницы готовы к 220 мс, а запрос ПЕРВОГО шрифта
# уходит только на 320-й - браузер узнаёт о шрифтах, лишь разобрав CSS, где
# они объявлены. Сто миллисекунд текст уже нарисован запасным начертанием, и
# потом подменяется: это и видно при жёсткой перезагрузке как «сначала другие
# шрифты». Ссылка preload в самой странице убирает лишнее звено - запрос
# уходит вместе со стилями.
#
# Перечислены только те файлы, которые страница на этом языке скачает всё
# равно; лишнего трафика от этого не появляется. Латиница нужна всем, включая
# китайский и арабский: слово «Earthlings» стоит в заголовках на любом языке.
# Кириллица добавляется русскому. Подмножества для остальных письменностей не
# перечисляются: они мелкие, лежат ниже сгиба и подменой не мозолят глаз.
PRELOAD = ['Montserrat-latin.woff2', 'Cormorant-latin.woff2']
PRELOAD_BY_LANG = {'ru': ['Montserrat-cyrillic.woff2', 'Cormorant-cyrillic.woff2']}


def font_preloads(lang):
    u"""Ссылки preload для шрифтов страницы. crossorigin обязателен даже на
    своём домене: без него браузер скачает файл ВТОРОЙ раз."""
    assert lang in ALL_LANGS, u'неизвестный язык %r' % lang
    return ['<link rel="preload" as="font" type="font/woff2" crossorigin '
            'href="/fonts/%s">' % f
            for f in PRELOAD + PRELOAD_BY_LANG.get(lang, [])]


# Языки, у которых письменность своя, а не латиница с кириллицей. Лист с
# объявлениями пишет make_script_fonts.py из боевого; здесь только подключение.
SCRIPT_CSS = ('ar', 'hi', 'ka', 'zh')


def script_css(lang):
    u"""Лист @font-face письменности - только тем языкам, у кого она своя.

    Montserrat и Cormorant не несут ни арабицы, ни деванагари, ни иероглифов,
    ни мхедрули. Лесенка в tokens.css называет для них Noto, но имя в лесенке
    само по себе означает лишь «возьми у читателя»: у кого шрифт стоит - тот
    видит текст чужим шрифтом, у кого нет - квадраты. Объявление обязано лежать
    на нашей стороне.

    Подключается по языку, а не всем сразу: китайский лист весит 181 КБ, и
    возить его на русскую страницу незачем.
    """
    assert lang in ALL_LANGS, u'неизвестный язык %r' % lang
    if lang not in SCRIPT_CSS:
        return []
    # Проверка на существование, а не на веру. Ссылка на отсутствующий лист не
    # роняет страницу: браузер получает 404, молча берёт системный шрифт, и
    # выглядит это точно так же, как до самохостинга. Заметить можно только
    # глазами и только на своей машине - то есть никогда.
    p = os.path.join(SITE, '_v2', 'css', 'fonts-%s.css' % lang)
    assert os.path.isfile(p), (
        u'нет %s - страница на языке %s осталась бы без шрифта письменности. '
        u'Собрать: python _tools/make_script_fonts.py' % (p, lang))
    return ['<link rel="stylesheet" href="/css/fonts-%s.css">' % lang]


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

# Эссе в подвале. Список пуст намеренно: место под него заведено
# 2026-08-23 по решению Артура, ссылки он даст позже. Формат записи -
# (адрес, подпись по языкам), например:
#   ('https://paragraph.xyz/@earthlings/...', {'ru': u'...', 'en': u'...'})
FOOTER_ESSAYS = []


def footer_html(lang, doc_href, has_doc=None):
    assert lang in ALL_LANGS, u'неизвестный язык %r' % lang
    has_doc = has_doc or (lambda num: True)
    o = []
    a = o.append

    a(u'<footer class="ftr">')
    a(u'<div class="ftr-in">')

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
      % esc(x(lang, 'systems')))
    a(u'<li><a href="%s">%s</a></li>'
      % (APP_URL % lang, esc(t(lang, 'nav.platform_btn'))))
    a(u'<li><a href="/awakened_code/">%s</a></li>'
      % esc(t(lang, 'nav.awakened_code')))
    a(u'</ul></div>')

    # Колонка показывается, только когда в ней есть ссылки. Пока список пуст,
    # заголовок без единой строки под ним читается не как «место занято», а
    # как поломка вёрстки. Появится первая ссылка - колонка вернётся сама.
    if FOOTER_ESSAYS:
        a(u'<div class="ftr-col"><h2 class="ftr-h">%s</h2>'
          % esc(x(lang, 'essays')))
        a(u'<ul class="ftr-list">')
        for href, label in FOOTER_ESSAYS:
            a(u'<li><a href="%s" rel="noopener">%s</a></li>'
              % (esc(href), esc(label.get(lang) or label['en'])))
        a(u'</ul>')
        a(u'</div>')

    # Колонка контактов - два способа написать живому человеку, и ничего
    # кроме. «Частые вопросы» стояли здесь с 25 августа и в тот же день ушли
    # ниже, в строку прав: они не контакт, а ответ, который уже написан, и
    # рядом с ними в нижней строке стоят два таких же готовых ответа - «О
    # нас» и «Юридическая информация».
    a(u'<div class="ftr-col"><h2 class="ftr-h">%s</h2><ul class="ftr-list">'
      % esc(t(lang, 'footer.contact')))
    a(u'<li><a href="mailto:%s">%s</a></li>' % (MAIL, MAIL))
    a(u'<li><a href="%s" rel="noopener">Telegram</a></li>' % TG)
    a(u'</ul></div>')

    a(u'</div>')

    # Внизу - строка прав слева, три ссылки справа (решение Артура
    # 2026-08-25). Ссылки собраны в одну группу, чтобы их можно было прижать
    # к правому краю одним правилом, а не отступом.
    #
    # Порядок: сначала то, чем пользуются чаще, потом то, что реже. «Частые
    # вопросы» - место, куда идут с вопросом; «О нас» - кто это делает;
    # «Юридическая информация» - формальный хвост, и хвосту место последним.
    #
    # «Частые вопросы» переехали сюда из колонки контактов в тот же день:
    # они не контакт, а готовый ответ, и рядом стоят два таких же.
    #
    # Строки «Тексты корпуса - CC BY 4.0» здесь больше нет: она была
    # единственным местом на сайте, где лицензия называлась вообще, и снять её
    # просто так значило бы оставить корпус без публичного разрешения на
    # воспроизведение. Лицензия стала нормой документа 22 «Юридическая
    # информация», раздел «Права на тексты» - и ссылка на него стоит здесь же.
    # Теперь строка действительно излишня.
    a(u'<div class="ftr-bottom">')
    a(u'<span class="ftr-copy">%s</span>' % esc(COPYRIGHT))
    a(u'<span class="ftr-legal">')
    if has_doc('27'):
        a(u'<a href="%s">%s</a>' % (esc(doc_href('27')),
                                    esc(t(lang, 'nav.faq_general'))))
    if has_doc('23'):
        a(u'<a href="%s">%s</a>' % (esc(doc_href('23')),
                                    esc(t(lang, 'nav.about_us'))))
    if has_doc('22'):
        a(u'<a href="%s">%s</a>' % (esc(doc_href('22')),
                                    esc(t(lang, 'nav.legal_info'))))
    a(u'</span>')
    a(u'</div>')
    a(u'</footer>')
    return u'\n'.join(o)
