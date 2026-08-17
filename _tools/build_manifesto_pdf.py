"""Собирает PDF Манифеста принадлежности из живой страницы mainpage/ru/index.html.

Источник один - тот же файл, который отдаётся на earth-lings.org/ru/. Ничего
не дублируется вручную: правится страница, перезапускается скрипт.

Последняя строка «Мы выбираем друг друга» рисуется кнопкой с рамкой, и вся её
площадь - кликабельная ссылка на учредительный период. Адрес абсолютный:
PDF пересылают, и открыт он будет вне сайта.

Скрипт лежит здесь, а не в репозитории сайта, потому что там всё отслеживаемое
уезжает на боевой сервер при деплое, и `tools/` целиком в .gitignore. Из-за
этого генератор жил на одной машине и на любой другой немецкий PDF собрать было
нельзя. Соседство с build_site_docs.py естественное: тот тоже лежит здесь и
пишет в репозиторий сайта.

Запуск:  python _tools/build_manifesto_pdf.py [ru|en|de]
Выход:   <репозиторий сайта>/downloads/<имя из BY_LANG>

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

# Репозиторий сайта. По умолчанию - соседняя папка рядом с этой, как у
# build_site_docs.py; переопределяется той же переменной окружения, чтобы не
# заводить вторую настройку на то же самое.
ROOT = Path(os.environ.get("EARTHLINGS_SITE")
            or Path(__file__).resolve().parent.parent.parent / "earth-lings-site")
assert (ROOT / "mainpage").is_dir(), (
    f"не найден репозиторий сайта: {ROOT}\n"
    "Ожидается earth-lings-site рядом с этим репозиторием. Если он лежит в "
    "другом месте - EARTHLINGS_SITE=/путь/к/earth-lings-site")

# Язык - аргумент, а не константа. Разбор страницы обобщённый: он ищет
# class="sign" и class="onward", а не русские слова, - поэтому для нового языка
# нужны только имя файла и адрес кнопки.
LANG = "ru"
for _a in sys.argv[1:]:
    if not _a.startswith("-"):
        LANG = _a

# Имя файла и адрес учредительного периода на каждом языке свои. Языка нет в
# таблице - сборка останавливается, а не кладёт английский текст в русский файл.
BY_LANG = {
    "ru": ("manifest-prinadlezhnosti-ru.pdf",
           "/documents/ru/ru20-uchreditelnyj-period.html",
           "Манифест народа Earthlings"),
    "en": ("manifesto-of-belonging-en.pdf",
           "/documents/en/en20-the-founding-period.html",
           "The manifesto of the Earthlings people"),
    # Умляуты в имени файла не ставим: ссылку на PDF пересылают почтой и в
    # мессенджерах, а там имя с ö ломается. Транслитерация почтовая - oe.
    "de": ("manifest-der-zugehoerigkeit-de.pdf",
           "/documents/de/de20-gruendungsphase.html",
           "Das Manifest des Volkes der Earthlings"),
}
assert LANG in BY_LANG, (
    'нет настроек для языка "%s": задайте имя файла, адрес кнопки и subject '
    'в BY_LANG. Языки: %s' % (LANG, ", ".join(sorted(BY_LANG))))
_name, _cta_path, SUBJECT = BY_LANG[LANG]

SRC = ROOT / "mainpage" / LANG / "index.html"
OUT = ROOT / "downloads" / _name

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
ALLOWED_BY_LANG = {"de": (0x201E, 0x201C)}
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
FONT_DIR = Path(__file__).resolve().parent / "fonts"
FAMILY = "Manifest"
FACES = ((FAMILY, "PT_Serif-Web-Regular.ttf"),
         (FAMILY + "-Bold", "PT_Serif-Web-Bold.ttf"),
         (FAMILY + "-Italic", "PT_Serif-Web-Italic.ttf"),
         (FAMILY + "-BoldItalic", "PT_Serif-Web-BoldItalic.ttf"))


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
    blocks = re.findall(r'<p([^>]*)>(.*?)</p>', lead[1], re.S)
    assert blocks, "не найдены абзацы"

    body, sign, cta = [], None, None
    for attrs, inner in blocks:
        if 'class="sign"' in attrs:
            sign = strip_tags(inner)
        elif 'class="onward"' in attrs:
            cta = strip_tags(inner)
        elif 'class="get-pdf"' in attrs:
            # Ссылка на скачивание принадлежит странице, а не тексту. Внутри
            # самого PDF строка «Скачать манифест в PDF» - бессмыслица, а
            # попадала она туда с тех пор, как блок появился на странице.
            continue
        else:
            body.append(to_rl(inner))

    assert sign, "не найдена подпись"
    assert cta, "не найдена надпись кнопки"
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

    st_body = ParagraphStyle("body", fontName="Manifest", fontSize=11, leading=17.5,
                             alignment=TA_JUSTIFY, spaceAfter=10, textColor=INK,
                             firstLineIndent=0)
    st_title = ParagraphStyle("title", fontName="Manifest-Bold", fontSize=23, leading=29,
                              alignment=TA_CENTER, textColor=NAVY, spaceAfter=0)
    st_sign = ParagraphStyle("sign", fontName="Manifest-Italic", fontSize=10.5, leading=15,
                             alignment=TA_CENTER, textColor=INK_SOFT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2.6 * cm, rightMargin=2.6 * cm,
        topMargin=2.2 * cm, bottomMargin=2.0 * cm,
        title=title, author=sign, subject=SUBJECT,
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
