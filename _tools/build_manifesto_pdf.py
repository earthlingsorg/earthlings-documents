"""Собирает PDF Обращения из страницы черновика _v2/<язык>/manifest.html.

Источник один - тот же файл, который встанет на earth-lings.org/<язык>/manifest.html
после подмены корня. Ничего не дублируется вручную: правится мастер Обращения,
перезапускается build_home_v2.py, перезапускается этот скрипт.

Раньше источником была боевая главная mainpage/<язык>/index.html, а выходом -
боевое downloads/. Обе стороны теперь под замком: боевое дерево не правится и
не пересобирается, а его страницы застыли на 16 августа, до переименования
Манифеста в Обращение. Собранный оттуда PDF назывался бы Манифестом при уже
переименованном тексте - и это не было бы видно, пока файл не откроют.

Последняя строка «Мы выбираем друг друга» рисуется кнопкой с рамкой, и вся её
площадь - кликабельная ссылка на учредительный период. Адрес абсолютный:
PDF пересылают, и открыт он будет вне сайта.

Скрипт лежит здесь, а не в репозитории сайта, потому что там всё отслеживаемое
уезжает на боевой сервер при деплое, и `tools/` целиком в .gitignore. Из-за
этого генератор жил на одной машине и на любой другой немецкий PDF собрать было
нельзя. Соседство с build_site_docs.py естественное: тот тоже лежит здесь и
пишет в репозиторий сайта.

Запуск:  python _tools/build_manifesto_pdf.py [ru|en|de|fr|es|ka|zh]
Выход:   <репозиторий сайта>/_v2/downloads/<имя из BY_LANG>

Из внешнего нужен только reportlab (`pip install reportlab`). Шрифт лежит в
_tools/fonts/ и версионируется вместе со скриптом, поэтому сборка одинакова на
Windows, macOS и Linux и ничего ставить в систему не требуется.
"""

import html
import os
import re
import sys
from pathlib import Path

from reportlab import rl_config
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Flowable, Frame, PageTemplate, Paragraph, Spacer

# Без этого reportlab штампует в файл время сборки, и PDF выходит побайтово
# разным при одном и том же тексте. В репозитории это означало бы правку
# бинарника на каждом прогоне, включая прогоны из pre-commit хука.
rl_config.invariant = 1

# Консоль Windows живёт в однобайтовой кодировке, и попытка напечатать в неё
# грузинскую или китайскую строку роняет скрипт - уже ПОСЛЕ того, как файл
# записан. Выглядит это как провал сборки, хотя PDF собран. Печатаем с
# заменой непередаваемых знаков.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

# Репозиторий сайта. По умолчанию - соседняя папка рядом с этой, как у
# build_site_docs.py; переопределяется той же переменной окружения, чтобы не
# заводить вторую настройку на то же самое.
ROOT = Path(os.environ.get("EARTHLINGS_SITE")
            or Path(__file__).resolve().parent.parent.parent / "earth-lings-site")
assert (ROOT / "_v2").is_dir(), (
    f"не найден репозиторий сайта: {ROOT}\n"
    "Ожидается earth-lings-site рядом с этим репозиторием. Если он лежит в "
    "другом месте - EARTHLINGS_SITE=/путь/к/earth-lings-site")

# Язык - аргумент, а не константа. Разбор страницы обобщённый: он ищет
# class="lead col" и class="sign", а не русские слова, - поэтому для нового
# языка нужны только имя файла и адрес кнопки.
#
# Значение --theme из позиционных выкусывается отдельно: оно тоже без дефиса,
# и `build_manifesto_pdf.py en --theme v2` собрал бы язык "v2" - вернее, упал
# бы на BY_LANG, но по невнятной причине.
_pos = sys.argv[1:]
if "--theme" in _pos:
    _i = _pos.index("--theme")
    _pos = _pos[:_i] + _pos[_i + 2:]
LANG = "ru"
for _a in _pos:
    if not _a.startswith("-"):
        LANG = _a

# Тема принимается только ради явности: сборщики страниц берут --theme, и
# человек по привычке допишет его сюда. Значение одно. Боевую тему скрипт не
# собирает не из осторожности, а потому, что собрать её нечем: боевые страницы
# заморожены до переименования, и PDF вышел бы с прежним названием.
if "--theme" in sys.argv:
    _t = sys.argv[sys.argv.index("--theme") + 1:sys.argv.index("--theme") + 2]
    assert _t == ["v2"], (
        "тема только v2. Боевое дерево заморожено: править и пересобирать его "
        "нельзя, а его главные застыли на 16 августа, до переименования "
        "Манифеста в Обращение.")

# Имя файла и адрес учредительного периода на каждом языке свои. Языка нет в
# таблице - сборка останавливается, а не кладёт английский текст в русский файл.
#
# Имена сменились 2026-08-26 вслед за переименованием Манифеста принадлежности
# в Обращение. Прежние manifest-*/manifesto-of-belonging-* никуда не рассылались,
# поэтому ломать было нечего; на боевом дереве они остаются как были, там своя
# копия и свой замок.
#
# Тема PDF (метаданные) больше не задаётся здесь: она берётся из заголовка H1
# разобранной страницы. Семь строк на семи языках, повторяющих название
# документа, - это семь мест, где переименование можно забыть.
BY_LANG = {
    "ru": ("obrashchenie-ru.pdf",
           "/documents/ru/ru20-uchreditelnyj-period.html"),
    "en": ("an-address-to-everyone-en.pdf",
           "/documents/en/en20-the-founding-period.html"),
    # Умляуты в имени файла не ставим: ссылку на PDF пересылают почтой и в
    # мессенджерах, а там имя с ö ломается. Транслитерация почтовая - oe.
    "de": ("eine-ansprache-an-alle-de.pdf",
           "/documents/de/de20-gruendungsphase.html"),
    # Диакритику в имя файла не ставим по той же причине, что и умляуты:
    # ссылку пересылают почтой и в мессенджерах, где é ломает адрес.
    "fr": ("un-message-a-tous-fr.pdf",
           "/documents/fr/fr20-periode-constituante.html"),
    # Диакритика в имя файла не идёт по той же причине: ó ломает адрес
    # при пересылке почтой и в мессенджерах.
    "es": ("un-mensaje-a-todos-es.pdf",
           "/documents/es/es20-periodo-constituyente.html"),
    # Мхедрули в имени файла не ставим по той же причине, что умляуты и
    # диакритику: адрес пересылают почтой и в мессенджерах, а грузинская буква
    # превращается там в %E1%83%A5 и ссылка перестаёт читаться. Имя файла -
    # английское, как и слаг документа.
    "ka": ("an-address-to-everyone-ka.pdf",
           "/documents/ka/ka20-the-founding-period.html"),
    # Иероглифы в имени файла не ставим по той же причине, что мхедрули и
    # умляуты: адрес пересылают почтой и в мессенджерах, где каждый знак
    # превращается в три процентных группы и ссылка перестаёт читаться.
    "zh": ("an-address-to-everyone-zh.pdf",
           "/documents/zh/zh20-the-founding-period.html"),
}
assert LANG in BY_LANG, (
    'нет настроек для языка "%s": задайте имя файла и адрес кнопки в BY_LANG. '
    'Языки: %s' % (LANG, ", ".join(sorted(BY_LANG))))
_name, _cta_path = BY_LANG[LANG]

SRC = ROOT / "_v2" / LANG / "manifest.html"
OUT = ROOT / "_v2" / "downloads" / _name
# Пишем только внутрь _v2. Проверка стоит здесь, а не в голове: сорваться сюда
# может только опечатка в двух строках выше, и восьмая проверка preflight_all
# поймала бы её уже после записи в боевое дерево.
assert (ROOT / "_v2") in OUT.parents, "выход обязан лежать внутри _v2: %s" % OUT

SITE = "https://earth-lings.org"
CTA_URL = SITE + _cta_path

# Палитра листа - из css/docs-statute.css, чтобы PDF и страница читались одинаково.
PAGE_BG = "#fbf9f3"
NAVY = "#1d4163"
GOLD = "#8a6a2f"
INK = "#3a4046"
INK_SOFT = "#5f6670"
RULE = "#c9b48c"

# Запрещённая типографика - по числовым кодпойнтам, а не литералам:
# литералы молча портятся при передаче через heredoc и буфер обмена.
FORBIDDEN = {
    0x2014: "em-dash", 0x2013: "en-dash", 0x2212: "minus", 0x2026: "ellipsis",
    0x201C: "ldquo", 0x201D: "rdquo", 0x201E: "bdquo", 0x201F: "quote",
    0x2018: "lsquo", 0x2019: "rsquo", 0x201A: "squote", 0x201B: "squote",
    0x2039: "lsaquo", 0x203A: "rsaquo",
    0x00A0: "NBSP", 0x202F: "narrow-NBSP", 0x2009: "thin-space",
    0x2007: "figure-space", 0x2008: "punct-space", 0x200A: "hair-space",
    0x200B: "ZWSP", 0x200C: "ZWNJ", 0x2060: "word-joiner", 0xFEFF: "BOM",
}

# Родная пунктуация языка - не признак машинного текста. Немецкая пара кавычек,
# низкая открывающая (U+201E) и верхняя закрывающая (U+201C), - такая же норма
# немецкого, как ёлочки для русского. Таблица выше писалась под русский и
# английский, где обе запрещены. Английская закрывающая U+201D остаётся
# запрещённой и для немецкого: в немецком тексте она означает, что кавычки
# приехали из чужой раскладки, а не поставлены по норме.
# Китайскому нужны три знака, и они шире немецкой пары: U+2014 - это тире
# 破折号, набираемое двумя подряд (——), а U+201C/U+201D - двойные кавычки
# упрощённого письма. Парность тире и баланс кавычек проверяет
# audit_conf/zh.py, иначе разрешение стало бы дырой. Подробнее - тот же
# комментарий в check_translation.py.
ALLOWED_BY_LANG = {"de": (0x201E, 0x201C),
                   "zh": (0x2014, 0x201C, 0x201D)}
ALLOWED = ALLOWED_BY_LANG.get(LANG, ())


# Шрифт лежит в репозитории, а не берётся из системы. Так сборка не зависит
# ни от операционной системы, ни от того, что у кого установлено: результат
# одинаков везде, включая машину, где Манифест собирают впервые.
#
# Почему PT Serif, а не Gelasio - метрический клон Georgia, который напрашивался
# первым: в Gelasio НЕТ кириллицы вовсе (проверено по cmap: ни одного знака из
# диапазона 0x410-0x44F). Русский Манифест на нём стал бы страницами пустых
# квадратов. PT Serif - тоже OFL, покрывает латиницу и кириллицу целиком, и
# сделан ParaType именно под русский текст.
#
# Прежде здесь была Georgia из C:\Windows\Fonts. Она проприетарная, в
# репозиторий её не положить, и вне Windows сборка падала.
#
# Шрифт зависит от ПИСЬМЕННОСТИ, а не от языка вообще, и таблица ниже - первая
# правка этого скрипта, которая касается не данных, а выбора. Причина в том,
# что PT Serif покрывает только латиницу и кириллицу: мхедрули в нём ноль
# знаков (проверено по cmap), и грузинский Манифест на нём стал бы страницей
# пустых квадратов.
#
# Имя семейства при этом остаётся одним и тем же - "Manifest". Меняются только
# файлы начертаний. Так сделано намеренно: имена стилей ("Manifest-Bold",
# "Manifest-Italic") встречаются в разметке документа десяток раз, и заводить
# ещё и FAMILY_BY_LANG значило бы искать их все и не найти одно.
#
# Грузинский: Noto Serif Georgian, сборка Google Fonts, выпечена в статические
# начертания из переменного шрифта (reportlab переменные не понимает и берёт из
# них одно начертание, отчего жирный стал бы неотличим от обычного).
# Готовые статические файлы с notofonts.github.io взять было нельзя: в них НЕТ
# латиницы вовсе - 2 знака ASCII из 95, - и слово Earthlings, ёлочки и адрес
# earth-lings.org превратились бы в пустые квадраты. В сборке Google Fonts
# латиница есть: 58 букв и вся нужная пунктуация.
#
# Курсива у Noto Serif Georgian нет, и это не пробел сборки: наклонного
# начертания у мхедрули нет как явления, курсив здесь - привычка чужого письма.
# Курсивные лица отображены на прямые, и подпись под Манифестом по-грузински
# встанет прямой.
FONT_DIR = Path(__file__).resolve().parent / "fonts"
FAMILY = "Manifest"
_PT_SERIF = ((FAMILY, "PT_Serif-Web-Regular.ttf"),
             (FAMILY + "-Bold", "PT_Serif-Web-Bold.ttf"),
             (FAMILY + "-Italic", "PT_Serif-Web-Italic.ttf"),
             (FAMILY + "-BoldItalic", "PT_Serif-Web-BoldItalic.ttf"))
_NOTO_GEORGIAN = ((FAMILY, "NotoSerifGeorgian-Regular.ttf"),
                  (FAMILY + "-Bold", "NotoSerifGeorgian-Bold.ttf"),
                  (FAMILY + "-Italic", "NotoSerifGeorgian-Regular.ttf"),
                  (FAMILY + "-BoldItalic", "NotoSerifGeorgian-Bold.ttf"))
# Китайский: Noto Serif SC, та же лицензия OFL. Целиком шрифт в репозиторий не
# кладётся - в нём около 65 тысяч глифов и 25 МБ в переменном начертании,
# тогда как в Манифесте меньше пятисот уникальных иероглифов. В fonts/ лежит
# субсет, испечённый make_cjk_subset.py; он же печёт статические Regular и
# Bold из переменного файла, потому что переменные reportlab не понимает.
# Курсива у иероглифов нет как явления, как и у мхедрули: курсивные лица
# отображены на прямые.
_NOTO_SC = ((FAMILY, "NotoSerifSC-Regular.ttf"),
            (FAMILY + "-Bold", "NotoSerifSC-Bold.ttf"),
            (FAMILY + "-Italic", "NotoSerifSC-Regular.ttf"),
            (FAMILY + "-BoldItalic", "NotoSerifSC-Bold.ttf"))
FACES_BY_LANG = {"ka": _NOTO_GEORGIAN, "zh": _NOTO_SC}
FACES = FACES_BY_LANG.get(LANG, _PT_SERIF)

# Перенос строк. Обычный режим reportlab ломает строку по пробелам, а в
# китайском письме пробелов нет: весь абзац для него - одно слово в две тысячи
# знаков, которое не влезает во фрейм, и абзац выпадает целиком. Режим 'CJK'
# разрешает перенос между любыми двумя иероглифами. Шрифт без этого режима
# не спасает: буквы будут, а текста не будет.
WORD_WRAP = "CJK" if LANG == "zh" else None

# Правило 行首禁则: строка не начинается со знака препинания. reportlab его
# знает и умеет вешать такой знак в правое поле, но таблица у него собрана под
# японский: в ней есть 。 и 、 и нет ни одного знака, которым набирают
# упрощённое письмо. Из-за этого китайская запятая исправно уезжала в начало
# строки. Дополняем таблицу библиотеки, а не обходим её в разметке: обходить
# пришлось бы в каждом абзаце.
#
# Тире 破折号 (две штуки U+2014 подряд) в список намеренно НЕ входит. reportlab
# вешает в поле ровно один знак, и пара разъехалась бы по двум строкам - это
# хуже, чем тире в начале строки.
if LANG == "zh":
    from reportlab.lib import textsplit as _ts
    _CJK_CANNOT_START = "".join(chr(c) for c in (
        0xFF0C,  # ，полноширинная запятая
        0xFF1A,  # ：двоеточие
        0xFF1B,  # ；точка с запятой
        0xFF01,  # ！восклицательный
        0xFF1F,  # ？вопросительный
        0x201D,  # ” закрывающая двойная
        0x2019,  # ' закрывающая одинарная
        0x300B,  # 》закрывающая книжная
        0xFF09,  # ）закрывающая круглая
    ))
    _ts.ALL_CANNOT_START += _CJK_CANNOT_START


def register_fonts():
    missing = [f for _, f in FACES if not (FONT_DIR / f).is_file()]
    assert not missing, (
        "нет начертаний шрифта в %s: %s\n"
        "Шрифт версионируется вместе со скриптом; если файлов нет, репозиторий "
        "склонирован не полностью." % (FONT_DIR, ", ".join(missing)))
    for name, file in FACES:
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
    pdfmetrics.registerFontFamily(FAMILY, normal=FAMILY, bold=FAMILY + "-Bold",
                                  italic=FAMILY + "-Italic",
                                  boldItalic=FAMILY + "-BoldItalic")


def check_coverage(chunks):
    """Каждый знак текста должен быть в шрифте.

    Субсет опасен тем, что молчит: знака нет - reportlab рисует пустой
    прямоугольник и собирает файл без единой жалобы. Заметить это можно
    только глазами и только открыв PDF. Поэтому сверяем заранее и падаем с
    перечнем недостающих знаков: тихая порча превращается в громкую ошибку.
    """
    have = set()
    for name, _ in FACES:
        have |= set(pdfmetrics.getFont(name).face.charToGlyph)
    missing = sorted({ord(c) for text in chunks for c in text
                      if ord(c) not in have and not c.isspace()})
    assert not missing, (
        "в шрифте нет %d знаков текста: %s\n"
        "Если это китайский, перепеките субсет: "
        "python _tools/make_cjk_subset.py <NotoSerifSC[wght].ttf>"
        % (len(missing), " ".join("%s U+%04X" % (chr(c), c) for c in missing[:30])))


def parse_source():
    """Достаёт из страницы заголовок, абзацы, подпись и надпись кнопки."""
    assert SRC.is_file(), f"нет исходника {SRC}"
    raw = SRC.read_text(encoding="utf-8")
    assert len(raw) > 1000, "исходник подозрительно короткий"

    title = re.search(r'<h1[^>]*class="doc-title"[^>]*>(.*?)</h1>', raw, re.S)
    assert title, "не найден заголовок"
    title = strip_tags(title.group(1))

    lead = raw.split('<section class="lead col">')
    assert len(lead) == 2, "не найдена секция с текстом"
    # Режем по концу секции, а не читаем до конца файла. За </section> лежат
    # подпись, ссылка на скачивание и подвал; ссылка на скачивание внутри
    # самого PDF - бессмыслица («Скачать Обращение в PDF» на его же странице),
    # а на боевой главной она туда и попадала, пока её не выключили по классу.
    sec = lead[1].split("</section>")[0]
    blocks = re.findall(r'<p([^>]*)>(.*?)</p>', sec, re.S)
    assert blocks, "не найдены абзацы"

    # Подпись живёт вне секции - забирается отдельно, а не перебором абзацев.
    sign = re.search(r'<p class="sign">(.*?)</p>', raw, re.S)
    assert sign, "не найдена подпись"
    sign = strip_tags(sign.group(1))

    # Надпись кнопки - последний абзац секции, и он обязан быть целиком
    # полужирным. На боевой главной он был размечен class="onward" и нёс
    # ссылку; в черновике это обычный абзац мастера - **Мы выбираем друг
    # друга.** - и отличить его можно только так. Проверка не косметическая:
    # без неё призыв молча уехал бы в текст, а кнопка получила бы случайную
    # фразу. Инвариант держится на всех девяти языках.
    _cta_attrs, _cta_inner = blocks[-1]
    _cta_inner = _cta_inner.strip()
    assert _cta_inner.startswith("<strong>") and _cta_inner.endswith("</strong>"), (
        "последний абзац Обращения не выделен целиком - надпись кнопки взять "
        "неоткуда: %r" % strip_tags(_cta_inner)[:60])
    cta = strip_tags(_cta_inner)

    body = [to_rl(inner) for _attrs, inner in blocks[:-1]]
    assert len(body) > 10, f"абзацев всего {len(body)} - похоже, разбор сломался"
    return title, body, sign, cta


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def to_rl(inner):
    """HTML абзаца - в разметку reportlab: из тегов остаётся только жирный."""
    s = re.sub(r"</?strong>", lambda m: "<b>" if m.group(0) == "<strong>" else "</b>", inner)
    s = re.sub(r"<(?!/?b>)[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def check_typography(chunks):
    bad = {}
    for text in chunks:
        for ch in text:
            if ord(ch) in FORBIDDEN and ord(ch) not in ALLOWED:
                bad.setdefault(FORBIDDEN[ord(ch)], 0)
                bad[FORBIDDEN[ord(ch)]] += 1
    return bad


class LinkButton(Flowable):
    """Кнопка с рамкой; кликабельна вся площадь, не только надпись."""

    def __init__(self, text, url, font="Manifest-Bold", size=13, pad_x=26, pad_y=13):
        super().__init__()
        self.text, self.url, self.font, self.size = text, url, font, size
        self.pad_x, self.pad_y = pad_x, pad_y
        self.box_w = pdfmetrics.stringWidth(text, font, size) + pad_x * 2
        self.box_h = size + pad_y * 2

    def wrap(self, avail_w, avail_h):
        self.avail_w = avail_w
        return avail_w, self.box_h

    def draw(self):
        c = self.canv
        x = (self.avail_w - self.box_w) / 2
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.9)
        c.rect(x, 0, self.box_w, self.box_h, stroke=1, fill=0)
        c.setFillColor(NAVY)
        c.setFont(self.font, self.size)
        c.drawCentredString(self.avail_w / 2, self.pad_y + self.size * 0.24, self.text)
        # Хотспот чуть шире рамки: попасть в кнопку на телефоне должно быть легко.
        c.linkURL(self.url, (x - 2, -2, x + self.box_w + 2, self.box_h + 2),
                  relative=1, thickness=0)


class Rule(Flowable):
    """Двойное правило под заголовком - тот же приём, что .rule-double на сайте."""

    def __init__(self, width=150, gap=4):
        super().__init__()
        self.w, self.gap = width, gap

    def wrap(self, avail_w, avail_h):
        self.avail_w = avail_w
        return avail_w, self.gap + 2

    def draw(self):
        c = self.canv
        x = (self.avail_w - self.w) / 2
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.4)
        c.line(x, self.gap, x + self.w, self.gap)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(x, 0, x + self.w, 0)


class ShortRule(Flowable):
    def __init__(self, width=64):
        super().__init__()
        self.w = width

    def wrap(self, avail_w, avail_h):
        self.avail_w = avail_w
        return avail_w, 1

    def draw(self):
        c = self.canv
        x = (self.avail_w - self.w) / 2
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(x, 0, x + self.w, 0)


def build():
    register_fonts()
    title, body, sign, cta = parse_source()

    bad = check_typography([title, sign, cta] + body)
    assert not bad, f"запрещённая типографика в исходнике: {bad}"
    check_coverage([title, sign, cta] + body)

    # Режим переноса задаётся один раз здесь и раздаётся всем стилям: забыть
    # его в одном из трёх - значит получить ровно один разъехавшийся блок.
    wrap = {"wordWrap": WORD_WRAP} if WORD_WRAP else {}
    st_body = ParagraphStyle("body", fontName="Manifest", fontSize=11, leading=17.5,
                             alignment=TA_JUSTIFY, spaceAfter=10, textColor=INK,
                             firstLineIndent=0, **wrap)
    st_title = ParagraphStyle("title", fontName="Manifest-Bold", fontSize=23, leading=29,
                              alignment=TA_CENTER, textColor=NAVY, spaceAfter=0, **wrap)
    st_sign = ParagraphStyle("sign", fontName="Manifest-Italic", fontSize=10.5, leading=15,
                             alignment=TA_CENTER, textColor=INK_SOFT, **wrap)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2.6 * cm, rightMargin=2.6 * cm,
        topMargin=2.2 * cm, bottomMargin=2.0 * cm,
        title=title, author=sign, subject="%s - Earthlings" % title,
        creator="earth-lings.org", lang=LANG,
    )

    def decorate(canvas, docobj):
        canvas.saveState()
        canvas.setFillColor(PAGE_BG)
        canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
        canvas.setFont(FAMILY, 8.5)
        canvas.setFillColor(INK_SOFT)
        canvas.drawCentredString(A4[0] / 2, 1.15 * cm, f"earth-lings.org    {docobj.page}")
        canvas.linkURL(SITE, (A4[0] / 2 - 60, 1.05 * cm, A4[0] / 2 + 60, 1.05 * cm + 11),
                       relative=0, thickness=0)
        canvas.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="page", frames=[frame], onPage=decorate)])

    flow = [Paragraph(title, st_title), Spacer(1, 20), Rule(), Spacer(1, 26)]
    for p in body:
        flow.append(Paragraph(p, st_body))
    # Порядок как на странице: текст, кнопка, подпись. Подпись последней -
    # иначе она читается меткой голоса и сужает «мы» текста до команды.
    flow += [Spacer(1, 24), LinkButton(cta, CTA_URL),
             Spacer(1, 24), ShortRule(), Spacer(1, 12), Paragraph(sign, st_sign)]

    doc.build(flow)

    assert OUT.is_file() and OUT.stat().st_size > 20000, "PDF не собрался или пуст"
    print(f"собрано: {OUT.relative_to(ROOT)}  {OUT.stat().st_size // 1024} КБ")
    print(f"абзацев: {len(body)}   кнопка: {cta!r} -> {CTA_URL}")


if __name__ == "__main__":
    sys.exit(build())
