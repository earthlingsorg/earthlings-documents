# -*- coding: utf-8 -*-
u"""Собирает PDF Обращения печатью страницы черновика браузером.

Источник один - `_v2/<язык>/address.html`, тот же файл, который встанет на
earth-lings.org/<язык>/address.html после подмены корня. Ничего не
дублируется: правится мастер Обращения, перезапускается build_home_v2.py,
перезапускается этот скрипт.

**Почему движок сменился.** Прежняя сборка была на reportlab: своя вёрстка,
свой шрифт, свои поля. Она давала красивый лист на семи языках и не могла дать
его на двух. reportlab кладёт кодпойнты подряд, а деванагари при отрисовке
переставляет знаки - краткое «и» пишется ПЕРЕД согласной, к которой относится, -
и арабская вязь требует соединения букв. Вывод получался бы не некрасивым, а
неправильным, и правдоподобно неправильным: чтобы заметить, надо знать язык.

Браузер это умеет: Chrome шьёт обе письменности сам. Решение Артура
2026-08-27 - пересобрать все девять одним движком, чтобы файлы были одной
семьёй, а не двумя.

**Что при этом потеряно, и это честно назвать.** Прежний PDF был набран
PT Serif на кремовом листе, вёрсткой по ширине. Повторить это на девяти языках
нельзя: PT Serif не покрывает ни деванагари, ни арабскую вязь, ни китайский,
ни грузинский. Одна семья возможна только на шрифтовой лесенке сайта, и теперь
PDF выглядит так же, как страница, с которой напечатан. Ушла и рамка-кнопка
вокруг последней строки: её рисовал прежний генератор, на странице её нет, и
дорисовывать в PDF то, чего нет в тексте, - это выдумывать.

**Что осталось от прежнего вида** - колонтитул: адрес сайта и номер страницы
внизу листа, PT Serif 8.5 пунктов. Его ставит не браузер: Chrome не понимает
`@bottom-center`. Ставится после печати, по странице за раз.

**Печатный лист** - `_v2/css/print.css`, подключён к странице. Что видит
человек, нажав Ctrl+P, то и лежит в файле, плюс одно добавление ниже.

**Что PDF дописывает к странице** (с 2026-10-08). Файл Обращения скачивают и
пересылают, и дальше он живёт без сайта под рукой. Поэтому под подписью
встаёт блок адресов (Декларация, документы 20 и 32, подтверждение личности,
почта), а под ним строка «Редакция текста от <дата>. Актуальная версия:
<адрес страницы>». Дата - день последнего коммита, менявшего мастер Обращения
этого языка, а не день сборки (решение оркестратора 2026-10-08): строка
отвечает на вопрос «то, что я читаю, ещё текущее?», и пересборка ради
шрифта не должна её сдвигать. Мастер с незакоммиченной правкой - сборки нет:
у такой правки ещё нет даты. Строка нужна, чтобы любой старый экземпляр сам вёл к
свежему: 2 октября файлы собрали, 5-го сдвинули даты периода, и три дня по
рукам ходили прежние даты, о чём файл никак не говорил. Блок вставляется в
HTML на лету, в саму страницу не пишется: на сайте те же адреса стоят в меню.
Набирает его браузер, как и остальной текст, - иначе вязь и деванагари снова
пришлось бы шить руками. Адреса берутся из таблицы слагов и перед печатью
проверяются ответом 200; не ответил хоть один - сборки нет.

**Откуда берутся шрифты.** `_v2` не содержит ни шрифтов письменностей, ни
картинок: в vhost для них стоит откат в общее дерево. Локальный сервер здесь
повторяет этот откат. Без него браузер получает 404 на woff2 и молча
подставляет системный шрифт - в прежнем прогоне в файл попала Nirmala UI
вместо Noto, и на другой машине тот же PDF собрался бы иначе. Поэтому 404
считаются и валят сборку.

Запуск:  python _tools/build_address_pdf.py [ru|en|de|fr|es|ka|zh|ar|hi|all]
Выход:   <репозиторий сайта>/_v2/downloads/<имя из BY_LANG>

Из внешнего нужны браузер (Chrome или Edge) и PyMuPDF.
"""

import datetime
import glob
import html
import io
import os
import re
import subprocess
import sys
import tempfile
import threading
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import fitz

from build_site_docs import doc_href

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
V2 = os.path.join(SITE, '_v2')

# Имена файлов менять нельзя: на них ведут ссылки со страниц и из писем.
# Языки нелатинских письменностей называются по-английски - так решено при
# сборке китайского и грузинского, хинди и арабский идут за ними.
BY_LANG = {
    'ru': 'obrashchenie-ru.pdf',
    'en': 'an-address-to-everyone-en.pdf',
    'de': 'eine-ansprache-an-alle-de.pdf',
    'fr': 'un-message-a-tous-fr.pdf',
    'es': 'un-mensaje-a-todos-es.pdf',
    'ka': 'an-address-to-everyone-ka.pdf',
    'zh': 'an-address-to-everyone-zh.pdf',
    'ar': 'an-address-to-everyone-ar.pdf',
    'hi': 'an-address-to-everyone-hi.pdf',
}

FOOT_FONT = os.path.join(TOOLS, 'fonts', 'PT_Serif-Web-Regular.ttf')
FOOT_TEXT = 'earth-lings.org'
FOOT_SIZE = 8.5
FOOT_COLOR = (0x5f / 255.0, 0x66 / 255.0, 0x70 / 255.0)
FOOT_UP = 34            # пунктов от низа листа

ORIGIN = 'https://earth-lings.org'
ID_URL = 'https://id.earth-lings.org'
MAIL = 'team@earth-lings.org'
AUTHOR = 'Earthlings'

# Документы блока адресов. Названия - заголовки мастеров своего языка, не
# перевод: блок обязан называть документ так же, как его назовёт сайт.
REF_DOCS = ('01', '20', '32')

# Подписи, которых в виде заголовка в корпусе нет. Слова взяты из него же:
# «подтверждение личности» - из документа 28 («страница подтверждения
# личности»), «предложения» - из документа 20 своего языка.
# Порядок: подтверждение личности, предложения и вопросы, «редакция от»,
# «актуальная версия».
LABELS = {
    'ru': (u'Подтверждение личности', u'Предложения и вопросы',
           u'Редакция текста от {date}.', u'Актуальная версия:'),
    'en': (u'Identity verification', u'Proposals and questions',
           u'Text last revised {date}.', u'Current version:'),
    'de': (u'Identitätsprüfung', u'Vorschläge und Fragen',
           u'Textfassung vom {date}.', u'Aktuelle Fassung:'),
    'fr': (u"Vérification d'identité", u'Propositions et questions',
           u'Texte dans sa version du {date}.', u'Version à jour:'),
    'es': (u'Verificación de identidad', u'Propuestas y preguntas',
           u'Texto en su versión del {date}.', u'Versión actual:'),
    'ka': (u'პირადობის დადასტურება', u'წინადადებები და კითხვები',
           u'ტექსტის რედაქცია: {date}.', u'აქტუალური ვერსია:'),
    'zh': (u'身份验证', u'建议和问题',
           u'文本修订日期：{date}。', u'最新版本：'),
    'ar': (u'التحقق من الهوية', u'المقترحات والأسئلة',
           u'آخر تعديل للنص: {date}.', u'أحدث نسخة:'),
    'hi': (u'पहचान सत्यापन', u'प्रस्ताव और प्रश्न',
           u'पाठ का संस्करण: {date}।', u'नवीनतम संस्करण:'),
}

# Даты пишутся так, как их пишет документ 20 своего языка: «22 ноября 2026
# года», «22. November 2026», «2026 წლის 22 ნოემბერი», «二〇二六年十一月二十二日».
MONTHS = {
    'ru': u'января февраля марта апреля мая июня июля августа сентября '
          u'октября ноября декабря',
    'en': u'January February March April May June July August September '
          u'October November December',
    'de': u'Januar Februar März April Mai Juni Juli August September '
          u'Oktober November Dezember',
    'fr': u'janvier février mars avril mai juin juillet août septembre '
          u'octobre novembre décembre',
    'es': u'enero febrero marzo abril mayo junio julio agosto septiembre '
          u'octubre noviembre diciembre',
    'ka': u'იანვარი თებერვალი მარტი აპრილი მაისი ივნისი ივლისი აგვისტო '
          u'სექტემბერი ოქტომბერი ნოემბერი დეკემბერი',
    'ar': u'كانون_الثاني/يناير شباط/فبراير آذار/مارس نيسان/أبريل أيار/مايو '
          u'حزيران/يونيو تموز/يوليو آب/أغسطس أيلول/سبتمبر تشرين_الأول/أكتوبر '
          u'تشرين_الثاني/نوفمبر كانون_الأول/ديسمبر',
    'hi': u'जनवरी फ़रवरी मार्च अप्रैल मई जून जुलाई अगस्त सितंबर अक्टूबर '
          u'नवंबर दिसंबर',
}
DATE_FMT = {
    'ru': u'{d} {m} {y} года', 'en': u'{d} {m} {y}', 'de': u'{d}. {m} {y}',
    'fr': u'{d} {m} {y}', 'es': u'{d} de {m} de {y}', 'ka': u'{y} წლის {d} {m}',
    'ar': u'{d} {m} {y}', 'hi': u'{d} {m} {y}',
}
ZH_DIGITS = u'〇一二三四五六七八九'


def zh_number(n):
    u"""1-31 китайскими числительными: 十, 十一, 二十二."""
    tens, ones = divmod(n, 10)
    return ((ZH_DIGITS[tens] if tens > 1 else '') + (u'十' if tens else '')
            + (ZH_DIGITS[ones] if ones or not tens else ''))


def date_text(lang, day):
    if lang == 'zh':
        return u'%s年%s月%s日' % (''.join(ZH_DIGITS[int(c)] for c in str(day.year)),
                               zh_number(day.month), zh_number(day.day))
    month = MONTHS[lang].split()[day.month - 1].replace('_', ' ')
    d = u'1er' if lang == 'fr' and day.day == 1 else str(day.day)
    return DATE_FMT[lang].format(d=d, m=month, y=day.year)


def text_date(lang):
    u"""День последнего коммита, менявшего мастер Обращения этого языка."""
    rel = '_address/%s-address.md' % lang
    git = ['git', '-C', REPO]
    dirty = subprocess.run(git + ['status', '--porcelain', '--', rel],
                           capture_output=True, text=True, check=True).stdout
    assert not dirty.strip(), (
        u'%s: мастер Обращения правлен и не закоммичен - у правки ещё нет даты '
        u'для строки редакции. Сначала коммит мастера.' % lang)
    out = subprocess.run(git + ['log', '-1', '--format=%cs', '--', rel],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert out, u'%s: у мастера Обращения нет истории в git' % lang
    return datetime.date.fromisoformat(out)


def master_title(lang, num):
    found = glob.glob(os.path.join(REPO, lang, '%s-*.md' % num))
    assert len(found) == 1, u'мастер %s/%s: найдено %d файлов' % (lang, num, len(found))
    for line in io.open(found[0], encoding='utf-8'):
        if line.startswith('# '):
            return line[2:].strip()
    raise AssertionError(u'в мастере %s нет заголовка H1' % found[0])


def address_url(lang):
    return '%s/%s/address.html' % (ORIGIN, lang)


def refs(lang):
    u"""Строки блока адресов: (подпись, адрес ссылки, видимый текст)."""
    id_label, mail_label = LABELS[lang][:2]
    rows = [(master_title(lang, n), ORIGIN + doc_href(n, lang)) for n in REF_DOCS]
    rows.append((id_label, ID_URL))
    return ([(t, u, u) for t, u in rows]
            + [(mail_label, 'mailto:' + MAIL, MAIL)])


def check_urls(langs):
    u"""Каждый адрес блока обязан отвечать 200 без переадресации."""
    urls = sorted({u for l in langs for _, u, _ in refs(l) if u.startswith('http')}
                  | {address_url(l) for l in langs})
    bad = []
    for u in urls:
        try:
            r = urllib.request.urlopen(
                urllib.request.Request(u, headers={'User-Agent': 'earthlings-pdf'}),
                timeout=30)
            if r.status != 200 or r.geturl().rstrip('/') != u.rstrip('/'):
                bad.append('%s -> %s %s' % (u, r.status, r.geturl()))
        except Exception as e:
            bad.append('%s -> %s' % (u, e))
    assert not bad, u'адреса блока не отвечают 200:\n  ' + '\n  '.join(bad)
    return len(urls)


# Печатный лист сайта (doc.css) рисует таблицам рамки и дописывает после
# каждой внешней ссылки её адрес в скобках. Для текста это верно, а в блоке
# адресов адрес уже стоит видимым - вышел бы дважды. Поэтому блок гасит оба
# правила у себя и только у себя.
REFS_CSS = (
    '.pdf-refs{margin-top:10mm;font-size:.88em;line-height:1.5;break-inside:avoid}'
    '.pdf-refs table{border-collapse:collapse;margin:0 auto;width:auto}'
    '.sheet .pdf-refs td{border:0;padding:.15em 0;vertical-align:top}'
    '.sheet .pdf-refs td:first-child{padding-inline-end:1.4em;white-space:nowrap}'
    '.sheet .pdf-refs a::after{content:none}'
    '.pdf-refs p{margin:8mm 0 0;text-align:center;font-size:.92em}')


def refs_html(lang, day):
    u"""Блок адресов и строка редакции - HTML под подписью Обращения.

    Стили свои: блок существует только в печати, в CSS сайта ему делать
    нечего. Адрес обёрнут в dir="ltr", чтобы в арабском он не перевернулся.
    """
    esc = html.escape
    rows = ''.join(
        '<tr><td>%s</td><td><a href="%s" dir="ltr">%s</a></td></tr>'
        % (esc(t), esc(u), esc(v)) for t, u, v in refs(lang))
    edition, current = LABELS[lang][2:]
    url = address_url(lang)
    return (
        '<style>%s</style><div class="pdf-refs"><table>%s</table>'
        '<p>%s %s <a href="%s" dir="ltr">%s</a></p></div>'
        % (REFS_CSS, rows, esc(edition.format(date=date_text(lang, day))),
           esc(current), esc(url), esc(url)))


# Знак и слово над заголовком первой страницы (решение Артура 2026-10-09).
# Файл ходит из рук в руки, и до этого единственным следом происхождения был
# адрес в колонтитуле. Шапку сайта для этого не включаем: chrome.css прячет
# .hdr в печати правильно - вместе со знаком там бургер и всё меню. Блок свой,
# только для печати, а слово набрано тем же классом .brand-name, что в шапке.
# Знак - чернильный вариант для светлого фона, как в шапке сайта; 120 точек в
# коробке 15 мм дают около 200 точек на дюйм. Слово не переводится ни на один
# язык; в RTL блок идёт по направлению страницы, как шапка.
MARK_IMG = '/images/logo-sm-ink.webp'
MARK_CSS = (
    '.pdf-mark{display:flex;align-items:center;justify-content:center;'
    'gap:.6rem;margin:0 0 8mm}'
    '.pdf-mark img{display:block;width:15mm;height:15mm}')
MARK_HTML = ('<style>%s</style><div class="pdf-mark">'
             '<span class="brand-name">Earthlings</span>'
             '<img src="%s" alt="" width="120" height="120"></div>'
             % (MARK_CSS, MARK_IMG))


def page_with_refs(src, lang, day):
    s = io.open(src, encoding='utf-8').read()
    m = re.search(r'<p class="sign">.*?</p>', s)
    assert m, u'%s: в странице не найдена подпись - блоку адресов негде встать' % lang
    s = s[:m.end()] + refs_html(lang, day) + s[m.end():]
    head = '<header class="doc-head">'
    assert s.count(head) == 1, u'%s: не найден заголовок - знаку негде встать' % lang
    return s.replace(head, MARK_HTML + head)

CHROMES = [
    os.environ.get('EARTHLINGS_CHROME'),
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]


def chrome_path():
    for p in CHROMES:
        if p and os.path.isfile(p):
            return p
    raise SystemExit(u'не найден браузер; укажите путь в EARTHLINGS_CHROME')


# ------------------------------------------------------------------- сервер

class Handler(SimpleHTTPRequestHandler):
    u"""Отдаёт `_v2`, при промахе - боевое дерево. Тот же откат, что в vhost."""

    misses = []
    pages = {}      # адрес -> HTML, отдаваемый вместо файла (блок адресов)

    def do_GET(self):
        body = Handler.pages.get(self.path.split('?', 1)[0])
        if body is None:
            return SimpleHTTPRequestHandler.do_GET(self)
        data = body.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def translate_path(self, path):
        rel = path.split('?', 1)[0].split('#', 1)[0].lstrip('/')
        rel = os.path.normpath(rel.replace('/', os.sep))
        if rel.startswith('..'):
            return os.path.join(V2, 'нет-такого')
        a = os.path.join(V2, rel)
        if os.path.exists(a):
            return a
        b = os.path.join(SITE, rel)
        if not os.path.exists(b):
            Handler.misses.append(path)
        return b

    def log_message(self, *a):
        pass


def serve():
    srv = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


# -------------------------------------------------------------- колонтитул

def page_text(src):
    u"""Видимый текст страницы: то, что обязано оказаться в PDF."""
    s = io.open(src, encoding='utf-8').read()
    i, j = s.find('<main'), s.find('</main>')
    assert i > 0 and j > i, (src, u'в странице не найден <main>')
    body = re.sub(r'<[^>]+>', ' ', s[i:j])
    body = re.sub(r'&[a-z]+;|&#\d+;', ' ', body)
    return re.sub(r'\s+', '', body)


def stamp(path, title, day):
    u"""Ставит колонтитул и приводит метаданные к постоянным.

    Chrome штампует в файл время печати, и один и тот же текст даёт разные
    байты при каждом прогоне. В репозитории это означало бы правку бинарника
    на каждом запуске - в том числе из хуков. Поэтому дата создания - день
    редакции текста без часов: пока мастер не правили, прогон в любой день
    даёт тот же файл.

    `/Title` заполнен с 2026-10-08: без него почта и мессенджеры показывали
    файл безымянным.
    """
    assert os.path.isfile(FOOT_FONT), FOOT_FONT
    doc = fitz.open(path)
    assert doc.page_count, u'в PDF ни одной страницы'
    font = fitz.Font(fontfile=FOOT_FONT)
    for i, page in enumerate(doc, 1):
        text = '%s    %d' % (FOOT_TEXT, i)
        w = font.text_length(text, FOOT_SIZE)
        page.insert_text(
            fitz.Point((page.rect.width - w) / 2, page.rect.height - FOOT_UP),
            text, fontfile=FOOT_FONT, fontname='ptserif',
            fontsize=FOOT_SIZE, color=FOOT_COLOR)
    when = 'D:%s000000Z' % day.strftime('%Y%m%d')
    doc.set_metadata({'producer': 'earth-lings.org', 'creator': '',
                      'title': title, 'author': AUTHOR, 'subject': '',
                      'keywords': '', 'creationDate': when, 'modDate': when})
    doc.xref_set_key(-1, 'ID', '[<00><00>]')
    # Полная пересборка файла поверх самого себя запрещена библиотекой, а
    # инкрементальная оставила бы в файле обе версии - и старую, и штампованную.
    tmp = path + '.tmp'
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    os.replace(tmp, path)
    fixed_id(path)


def fixed_id(path):
    u"""Гасит случайный идентификатор в конце файла.

    Второй элемент `/ID` библиотека пересобирает на каждом сохранении, и он
    единственное, чем два файла с одинаковым текстом отличаются друг от друга.
    Заменяется НА ТУ ЖЕ ДЛИНУ: в PDF после таблицы ссылок стоит смещение, и
    сдвиг байтов сломал бы файл.
    """
    raw = io.open(path, 'rb').read()
    # Элемент `/ID` библиотека пишет в ДВУХ видах: шестнадцатеричной строкой
    # `<...>` и литеральной `(...)`. Первая версия этой проверки знала только
    # шестнадцатеричный, а на литеральном молча выходила «идентификатора нет» -
    # и случайная величина оставалась в файле. Поймано тем, что один и тот же
    # текст дал два разных PDF: 30 байт разницы, все внутри `/ID`.
    m = re.search(br'/ID\s*\[\s*(<[0-9A-Fa-f]*>|\([^)]*\))\s*'
                  br'(<[0-9A-Fa-f]*>|\([^)]*\))\s*\]', raw)
    assert m, u'в файле не найден /ID - проверьте, чем он сохранён'
    for g in (1, 2):
        a, b = m.span(g)
        # Заменяем СОДЕРЖИМОЕ, не скобки, и ровно на ту же длину: в PDF после
        # таблицы ссылок стоит смещение, и сдвиг байтов сломал бы файл.
        raw = raw[:a + 1] + b'0' * (b - a - 2) + raw[b - 1:]
    io.open(path, 'wb').write(raw)


# ------------------------------------------------------------------ сборка

# Шрифтовая лесенка сайта. Всё, что вне её, - системный шрифт, подставленный
# браузером молча: woff2 доехал, а знака в нём нет. Блок адресов принёс в
# печать слова, которых в тексте Обращения не было, и проверка 404 такую
# подмену уже не ловит.
OWN_FONTS = re.compile(r'^(Cormorant|Montserrat|Noto|PT#20Serif)')


def font_names(doc):
    out = set()
    for x in range(1, doc.xref_length()):
        o = doc.xref_object(x)
        if '/FontDescriptor' in o and '/FontName' in o:
            m = re.search(r'/FontName\s*/(\S+)', o)
            out.add(re.sub(r'^[A-Z]{6}\+', '', m.group(1)))
    return out


def doc_title(src):
    m = re.search(r'<h1 class="doc-title">(.*?)</h1>',
                  io.open(src, encoding='utf-8').read())
    assert m, u'%s: не найден заголовок Обращения' % src
    return html.unescape(m.group(1)).strip()


def build(lang, port, browser):
    day = text_date(lang)
    src = os.path.join(V2, lang, 'address.html')
    assert os.path.isfile(src), u'нет страницы Обращения: %s' % src
    name = BY_LANG.get(lang)
    assert name, u'язык %r не назван в BY_LANG' % lang

    out = os.path.join(V2, 'downloads', name)
    assert os.path.abspath(out).startswith(os.path.abspath(V2) + os.sep), (
        u'выход обязан лежать внутри _v2: %s' % out)
    if not os.path.isdir(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))

    Handler.misses[:] = []
    Handler.pages.clear()
    Handler.pages['/%s/address.html' % lang] = page_with_refs(src, lang, day)
    profile = tempfile.mkdtemp(prefix='earthlings-print-')
    subprocess.run(
        [browser, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
         '--user-data-dir=' + profile, '--virtual-time-budget=15000',
         '--print-to-pdf=' + out,
         'http://127.0.0.1:%d/%s/address.html' % (port, lang)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)

    assert not Handler.misses, (
        u'браузер не получил %d файл(ов): шрифт подменился бы системным, знак пропал бы: %s'
        % (len(Handler.misses), ', '.join(sorted(set(Handler.misses))[:5])))
    assert os.path.isfile(out) and os.path.getsize(out) > 20000, (
        u'PDF не собрался или пуст: %s' % out)

    title = u'%s - Earthlings' % doc_title(src)
    stamp(out, title, day)

    doc = fitz.open(out)
    pages = doc.page_count
    text = ''.join(p.get_text() for p in doc)
    # Лист A4 задаёт только print.css. Пришёл Letter - браузер напечатал
    # страницу раньше, чем доехал печатный лист, и в файл попали экранные
    # стили с кнопкой «скачать PDF». Так было 2026-10-08 с en, один прогон
    # из девяти; поймала это проверка шрифтов ниже, а не 404.
    # Знак обязан лечь картинкой на первую страницу и только на неё.
    imgs = [len(p.get_images(full=True)) for p in doc]
    assert imgs[0] >= 1 and not any(imgs[1:]), (
        u'%s: картинок по страницам %s - знак не встал или встал не там'
        % (lang, imgs))
    sizes = {(round(p.rect.width), round(p.rect.height)) for p in doc}
    assert sizes == {(595, 842)}, (
        u'%s: лист %s вместо A4 - print.css не применился' % (lang, sizes))
    # Адрес без пути Chrome пишет со слешем: id.earth-lings.org/.
    links = {(l.get('uri') or '').rstrip('/') for p in doc for l in p.get_links()}
    fonts = font_names(doc)
    meta = doc.metadata
    doc.close()
    assert meta['title'] == title and meta['author'] == AUTHOR, (
        u'%s: метаданные не встали: %r' % (lang, meta))
    want_links = {u.rstrip('/') for _, u, _ in refs(lang)} | {address_url(lang)}
    assert want_links <= links, (
        u'%s: в PDF нет ссылок: %s' % (lang, ', '.join(sorted(want_links - links))))
    alien = sorted(f for f in fonts if not OWN_FONTS.match(f))
    assert fonts and not alien, (
        u'%s: в PDF попал шрифт не с лесенки сайта: %s' % (lang, ', '.join(alien)))
    assert pages >= 2, u'%s: страниц всего %d - похоже, текст не дошёл' % (lang, pages)
    assert FOOT_TEXT in text, u'%s: колонтитул не встал' % lang

    # Сколько знаков «много» - зависит от письменности: китайский говорит то же
    # самое втрое короче русского. Поэтому сверяемся не с числом, а с самой
    # страницей: в PDF обязано попасть почти всё, что на ней написано.
    want = len(page_text(src))
    got = len(text) - pages * (len(FOOT_TEXT) + 5)
    assert want and got > want * 0.8, (
        u'%s: на странице %d знаков, в PDF %d - текст дошёл не весь'
        % (lang, want, got))
    return name, pages, os.path.getsize(out) // 1024, day


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if '--theme' in sys.argv:
        i = sys.argv.index('--theme')
        if i + 1 < len(sys.argv) and sys.argv[i + 1] in args:
            args.remove(sys.argv[i + 1])
    langs = sorted(BY_LANG) if (not args or args == ['all']) else args

    assert os.path.isdir(V2), u'нет каталога черновика: %s' % V2
    assert os.path.isdir(os.path.join(SITE, 'fonts')), (
        u'нет общего каталога шрифтов - откат для woff2 работать не будет')

    browser = chrome_path()
    print('')
    print(u'адреса блока: %d, все отвечают 200' % check_urls(langs))
    srv, port = serve()
    print(u'PDF ОБРАЩЕНИЯ: печать страниц браузером')
    print('=' * 62)
    try:
        for lang in langs:
            name, pages, kb, day = build(lang, port, browser)
            print(u'  %-3s %-32s %2d стр.  %3d КБ  текст от %s'
                  % (lang, name, pages, kb, day.isoformat()))
    finally:
        srv.shutdown()
    print('=' * 62)
    print(u'собрано: %d' % len(langs))
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')
    sys.exit(main())
