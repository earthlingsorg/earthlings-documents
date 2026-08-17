# -*- coding: utf-8 -*-
u"""Языковая главная нового сайта: чередование полос, как на epic.org.

Зачем страница переделывается. Сейчас `/ru/`, `/en/` и остальные семь адресов
отдают ОДИН И ТОТ ЖЕ `index.html` с английскими метаданными, а текст дорисовывает
скрипт из `mainpage/<язык>/index.html`. Для краулера без JS все девять языковых
главных пусты. Здесь у каждого языка свой файл, полный в HTML, с заголовком и
описанием на своём языке.

Что на полосах. Порядок задан Артуром: белая, тёмно-синяя, белая, голубая,
тёмно-синяя, и на них Манифест, Учредительный период, Декларация. Четвёртую и
пятую он оставил на моё усмотрение - там правовая база и путь earthling с
кнопкой действия: снизу вверх это «кто мы - что происходит сейчас - чем это
учреждается - на каком праве это стоит - как войти».

Текст не сочиняется. Лид каждой полосы - первые абзацы соответствующего мастера
слово в слово. Заголовок - его H1. Отсебятины на главной быть не должно: это
самая читаемая страница сайта, и голос на ней должен быть тот же, что в корпусе.

Собирается два файла на язык:
  _v2/<язык>/index.html     - полосы
  _v2/<язык>/manifest.html  - Манифест целиком, набранный как документ

Использование:
  python build_home_v2.py            все языки, для которых есть мастера
  python build_home_v2.py ru         один язык
  python build_home_v2.py --dry      ничего не записывать
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md2doc                                              # noqa: E402
import chrome as C                                         # noqa: E402
from build_site_docs import (SITE, REPO, ORIGIN, ROOT, doc_href, has_doc,
                             ALL_LANGS, md_dir, corpus_file, SLUGS)  # noqa: E402

MANIFEST_DIR = os.path.join(REPO, '_manifest')
OUT = os.path.join(SITE, '_v2')

# Полосы: (класс темы, что показываем, номера БЛОКОВ лида, якорь).
#
# Номера, а не «первые N абзацев». Корпусные документы открываются процедурно -
# «Настоящий текст представляет...», «Возраст - 18 лет», - и механический выбор
# первого абзаца ставил на главную служебные оговорки. Абзацы выбраны глазами.
#
# Считаются ВСЕ блоки мастера подряд, включая заголовки, списки и врезки. Это
# не мелочь, а условие правильности. Раньше считались только абзацы прозы, а
# проза отбиралась в том числе по длине - короче 90 знаков не абзац. Длина
# зависит от языка: русский абзац в 77 знаков выпадал, его немецкий перевод в
# 96 оставался, и один и тот же номер означал в двух языках разные абзацы.
# Английская и немецкая правовая полоса из-за этого открывались служебной
# оговоркой вместо тезиса. Якорь этого не ловил: он сверялся только с русским.
#
# Число блоков от языка не зависит: переводы зеркалят мастер блок в блок - это
# правило корпуса. Поэтому lead() требует, чтобы число блоков совпало, и падает,
# если мастера разошлись. ЯКОРЬ - начало русского блока - остаётся второй
# проверкой: он ловит правку внутри мастера, не меняющую числа блоков.
#
# Документы названы номерами: переименование документа сюда не заглядывает,
# заголовок полосы берётся из его H1.
BANDS = [
    ('white', 'manifest', [2, 3, 5],  u'Международные организации'),
    ('navy',  'doc:20',   [6, 9],     u'Сегодня Декларация существует'),
    ('white', 'doc:01',   [3, 6],     u'Настоящая редакция является'),
    ('mist',  'legal',    [15, 22],   u'Международное право умеет'),
    ('navy',  'doc:14',   [32],       u'Внутри народа паспорт'),
    # Полоса платформы: слева текст из документа 12, справа туры платформы
    # карточками. Карточки прямые намеренно - скошенные бока уже заняты
    # языковым слайдером тремя полосами выше, и повторять приём значило бы
    # сделать две разные вещи похожими.
    ('white', 'platform', [8, 9],     u'Платформа не является социальной'),
    # Как вступить: шесть шагов из документа 14, раздел 2. Полоса отвечает на
    # вопрос, который на главной больше нигде не отвечен целиком - что именно
    # происходит между «хочу» и «паспорт у меня»: анкета, проверка личности,
    # взнос, кошелёк, выпуск паспорта.
    ('mist',  'steps',    [10],       u'Иных условий не существует'),
    # Awakened Code живьём в рамке монитора. Тёмно-синяя полоса ему и нужна:
    # терминал на чёрном - его собственное оформление, и на светлой полосе
    # экран выглядел бы дырой.
    ('navy',  'awakened', [],        u''),
]

# Сколько эссе показать рядом с монитором - по стольку из левой и правой
# ленты. Названия берутся из data/sliders.json самого Awakened Code, где они
# уже лежат на девяти языках: сочинять для этой полосы нечего.
AWAKENED_ITEMS = 3

# Сколько первых фраз Манифеста идут в плакат. Ровно три: в русском,
# английском и немецком мастере это «Международные организации. Посмотрите на
# это слово внимательно. Между народами - так оно читается» - три коротких
# фразы, третья из которых и есть удар. Четвёртая уже длинная и в плакат не
# лезет ни на одном языке.
POSTER_SENTENCES = 3

# Что перечислено в правовой полосе. Порядок - от общего к частному.
LEGAL_DOCS = ['30', '04', '05', '26']
# Лид правовой полосы берём из «Как возникает субъект права»: там сказано, на
# чём всё стоит, без служебных оговорок про соотношение документов.
LEGAL_LEAD_DOC = '30'

# Подпись под Манифестом. Подписывают его авторы, а не народ (Учредительный
# период, раздел 02), поэтому здесь команда, а не «Earthlings».
SIGN = {'ru': u'Команда Earthlings', 'en': u'The Earthlings team',
        'de': u'Das Earthlings-Team'}

PDF = {
    'ru': ('/downloads/manifest-prinadlezhnosti-ru.pdf', u'Скачать Манифест в PDF'),
    'en': ('/downloads/manifesto-of-belonging-en.pdf', u'Download the Manifesto as PDF'),
    'de': ('/downloads/manifest-der-zugehoerigkeit-de.pdf', u'Manifest als PDF herunterladen'),
}


# ------------------------------------------------------------------ мастера

def read_master(path):
    assert os.path.isfile(path), u'нет мастера %s' % path
    s = io.open(path, encoding='utf-8').read()
    assert s.strip(), u'пустой мастер %s' % path
    return s


def title_of(md):
    m = re.search(r'^#\s+(.+)$', md, re.M)
    assert m, u'в мастере нет заголовка H1'
    return m.group(1).strip()


def prose(md):
    u"""Абзацы прозы мастера по порядку.

    Выброшены заголовки, цитаты, таблицы, списки, разделители, вставки схем и
    строки из одного жирного куска - это подзаголовок документа. Короче 90
    знаков тоже выброшено: такой длины бывают пункты перечня («Возраст -
    достижение возраста 18 лет»), а не абзац, которым открывают страницу.
    """
    out = []
    for block in re.split(r'\n\s*\n', md):
        b = re.sub(r'\s+', ' ', block.strip())
        if not b or b[0] in '#>|[' or b.startswith('- ') or b.startswith('* '):
            continue
        if b.startswith('---') or re.match(r'^\*\*[^*]+\*\*$', b):
            continue
        if len(b) < 90:
            continue
        out.append(b)
    assert out, u'не нашлось ни одного абзаца прозы'
    return out


def blocks(md):
    u"""Все непустые блоки мастера по порядку, без единого фильтра.

    Именно отсутствие фильтров и делает нумерацию годной для всех языков:
    любой отбор «что считать абзацем» опирается на свойства текста, а они у
    перевода другие. Число блоков же задано структурой, а структуру перевод
    повторяет блок в блок.
    """
    bs = [re.sub(r'\s+', ' ', b.strip())
          for b in re.split(r'\n\s*\n', md) if b.strip()]
    assert bs, u'в мастере нет ни одного блока'
    return bs


def is_prose(b):
    u"""Блок - обычный абзац, а не заголовок, список, врезка или разделитель.

    Проверка нужна не для отбора, а как страховка: если номер в BANDS
    промахнулся, на главную попал бы заголовок раздела или строка таблицы, и
    заметить это можно было бы только глазами на девяти языках.
    """
    if b.startswith('---') or re.match(r'^\*\*[^*]+\*\*$', b):
        return False
    return b[0] not in '#>|' and not b.startswith('- ') and not b.startswith('* ')


def lead(load, what, nums, anchor, lang):
    u"""Блоки лида по номерам, с двумя проверками.

    Первая: число блоков в мастере языка обязано совпасть с русским. Не
    совпало - переводы разошлись с мастером по структуре, и любой номер
    означает в них уже не то; сборка падает и называет документ.

    Вторая: русский блок начинается с якоря. Она ловит правку ВНУТРИ мастера,
    от которой число блоков не меняется.
    """
    ru = blocks(load(what, 'ru'))
    bs = blocks(load(what, lang)) if lang != 'ru' else ru
    assert len(bs) == len(ru), (
        u'мастер %s (%s) состоит из %d блоков, а русский - из %d. Переводы '
        u'корпуса зеркалят мастер блок в блок; раз число разошлось, номера в '
        u'BANDS указывают в этих языках на другие абзацы. Сверьте мастера.'
        % (what, lang, len(bs), len(ru)))
    for n in nums:
        assert 1 <= n <= len(bs), (
            u'в мастере %s всего %d блоков, а лид просит №%d' % (what, len(bs), n))
        assert is_prose(bs[n - 1]), (
            u'блок №%d мастера %s (%s) - не абзац, а %r. На главную попал бы '
            u'заголовок или список.' % (n, what, lang, bs[n - 1][:60]))
    got = ru[nums[0] - 1]
    assert got.startswith(anchor), (
        u'лид главной разошёлся с мастером %s: блок №%d начинается на %r, а '
        u'ожидалось %r. Мастер правили - проверьте номера в BANDS и выберите '
        u'заново.' % (what, nums[0], got[:40], anchor))
    return [bs[n - 1] for n in nums]


def md_inline(s):
    u"""Разметка внутри абзаца: жирный, курсив, ссылки, код. Того же набора
    хватает и корпусу - главная набрана тем же, чем документы."""
    s = C.esc(s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'&lt;(https?://[^&]+)&gt;', r'<a href="\1">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s


def doc_master(num, lang):
    return read_master(os.path.join(md_dir(lang), corpus_file(num, lang)))


def load(what, lang):
    u"""Мастер по имени полосы: 'manifest' или номер документа. Один вход на
    оба случая нужен затем, чтобы lead() могла сама поднять русский мастер и
    сверить с ним структуру, не зная, какая полоса её вызвала."""
    if what == 'manifest':
        return read_master(os.path.join(MANIFEST_DIR, '%s-manifest.md' % lang))
    return doc_master(what, lang)


# ------------------------------------------------------------------ страница

def head(lang, url, title, desc, path, extra_css=()):
    # path(код языка) -> адрес ЭТОЙ ЖЕ страницы на другом языке. Без него
    # hreflang на странице Манифеста вёл бы на главные других языков, то есть
    # объявлял бы переводом не тот документ.
    langs = [l for l in ALL_LANGS if os.path.isfile(
        os.path.join(MANIFEST_DIR, '%s-manifest.md' % l))]
    alts = ''.join(
        '<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, ORIGIN, path(l))
        for l in langs)
    xdef = 'en' if 'en' in langs else langs[0]
    alts += ('<link rel="alternate" hreflang="x-default" href="%s%s">\n'
             % (ORIGIN, path(xdef)))
    ld = {'@context': 'https://schema.org', '@type': 'WebPage',
          'name': title, 'description': desc, 'inLanguage': lang, 'url': url,
          'publisher': {'@type': 'Organization', 'name': 'Earthlings',
                        'url': ORIGIN}}
    css = ['<link rel="stylesheet" href="/css/tokens.css">',
           '<link rel="stylesheet" href="/css/chrome.css">',
           '<link rel="stylesheet" href="/css/doc.css">'] + list(extra_css)
    return '\n'.join([
        '<!DOCTYPE html>',
        '<html lang="%s"%s>' % (lang, ' dir="rtl"' if lang in C.RTL else ''),
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % C.esc(title),
        '<meta name="description" content="%s">' % C.esc(desc),
    ] + css + [
        '<script defer src="/js/chrome.js"></script>',
        '<meta name="robots" content="index, follow">',
        '<meta property="og:type" content="website">',
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % C.esc(title),
        '<meta property="og:description" content="%s">' % C.esc(desc),
        '<meta property="og:image" content="%s/images/og-image.jpg">' % ORIGIN,
        '<meta property="og:site_name" content="Earthlings">',
        '<meta property="og:locale" content="%s">' % lang,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % C.esc(title),
        '<meta name="twitter:image" content="%s/images/og-image.jpg">' % ORIGIN,
        '<link rel="canonical" href="%s">' % url,
        '<script type="application/ld+json">',
        json.dumps(ld, ensure_ascii=False, separators=(',', ':')),
        '</script>',
        alts.rstrip(),
        '</head>',
    ])


def wrap(lang, inner, url, title, desc, path, extra_css=()):
    href = lambda n: doc_href(n, lang)                     # noqa: E731
    have = lambda n: has_doc(n, lang)                      # noqa: E731
    return '\n'.join([
        head(lang, url, title, desc, path, extra_css),
        '<body>',
        C.header_html(lang, doc_href=href, lang_url=path,
                      home_url='/%s/' % lang, has_doc=have),
        inner,
        C.footer_html(lang, doc_href=href, has_doc=have),
        '</body>', '</html>', '',
    ])


# ------------------------------------------------------------------ полосы

def decl_title(lang):
    u"""Название Декларации на языке lang - из собранной страницы, а не из
    мастера: мастера есть только у трёх языков, а слайдер показывает девять."""
    import glob
    f = glob.glob(os.path.join(SITE, 'documents', lang, '%s01*.html' % lang))
    assert f, u'нет собранной страницы %s01 - слайдеру нечего показать' % lang
    s = io.open(f[0], encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    assert m, u'в %s нет заголовка h1' % f[0]
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip()


def langslider(lang):
    u"""Девять слайдов: название Декларации на каждом из девяти языков.

    Единственный по-настоящему свой визуальный актив сайта - корпус на девяти
    письменностях. Слайдер этим и занят: показывает их рядом и служит входом.
    Скошенные бока делает CSS, скрипта здесь нет ни строки.
    """
    o = [u'<ul class="langslider" aria-label="%s">' % C.esc(C.x(lang, 'lang_switcher'))]
    for code in C.ALL_LANGS:
        rtl = u' dir="rtl"' if code in C.RTL else u''
        o.append(u'<li class="langslide"><a href="%s" lang="%s"%s>'
                 u'<span class="langslide-lang">%s</span>'
                 u'<span class="langslide-title">%s</span></a></li>'
                 % (C.esc(doc_href('01', code)), code, rtl,
                    C.esc(C.LANG_LABEL[code]), C.esc(decl_title(code))))
    o.append(u'</ul>')
    return u'\n'.join(o)


# Даты вех учредительного периода в машинном виде. В тексте мастеров они
# написаны словами и на девяти языках по-своему, разбирать их разбором строки
# значило бы гадать. Здесь они один раз и для всех языков; число обязано
# совпасть с числом пунктов в мастере, иначе сборка падает.
PERIOD_DATES = ['2026-09-07', '2026-12-06', '2026-12-20', '2027-01-03']

# Абзац документа 04 с перечнем правовых форм. Якорь - начало русского абзаца.
FORMS_ANCHOR = u'Право предоставляет форму'


def timeline(lang):
    u"""Шкала учредительного периода: четыре вехи из раздела «Сроки».

    Пункты берутся из мастера как есть - `- **дата** - что происходит`. Такой
    же список лежит в английском и немецком мастере: корпус переводится блок в
    блок, поэтому разбор один на все языки.

    Какая веха текущая, страница не знает и знать не может: она статическая, а
    собирается раз в несколько недель. Проставить «сейчас здесь» при сборке
    значило бы соврать через месяц. Поэтому у каждой вехи стоит дата в
    машинном виде, а подсветку ставит крошечный скрипт при показе. Без него
    шкала читается полностью, просто без подсветки.
    """
    md = doc_master('20', lang)
    items = re.findall(r'^-\s+\*\*(.+?)\*\*\s+-\s+(.+)$', md, re.M)
    assert len(items) == len(PERIOD_DATES), (
        u'в мастере 20 (%s) вех %d, а дат в PERIOD_DATES %d - раздел «Сроки» '
        u'правили, шкала разошлась с текстом'
        % (lang, len(items), len(PERIOD_DATES)))
    o = [u'<ol class="timeline">']
    for (date_text, what), iso in zip(items, PERIOD_DATES):
        # у третьей вехи после первой фразы идут подробности - на шкале лишние
        first_sentence = re.split(r'(?<=[.!?])\s', what.strip())[0]
        o.append(u'<li class="tl-step" data-date="%s">'
                 u'<span class="tl-date">%s</span>'
                 u'<span class="tl-text">%s</span></li>'
                 % (iso, C.esc(date_text.strip()), md_inline(first_sentence)))
    o.append(u'</ol>')
    return u'\n'.join(o)


def ladder(lang):
    u"""Лестница правовых форм из документа 04.

    Документ перечисляет формы, которые право даёт объединениям людей - от
    брака до международной организации, - и заканчивает: на уровне
    человечества формы нет. Это и есть недостающая ступень, ради которой
    существует проект, и рисовать её выдуманной схемой было бы нечестно:
    здесь ровно слова мастера.

    Разбор один на все языки: двоеточие, перечисление через запятую, тире.
    Тире везде ASCII с пробелами - это правило типографики корпуса, а не
    удача. Число форм обязано совпасть на всех языках, иначе сборка падает.
    """
    # Номер блока ищем в русском мастере всегда, а не только когда собираем
    # русскую страницу: иначе сборка одного немецкого языка зависела бы от
    # того, собирали ли перед этим русский.
    #
    # Блоки, а не абзацы прозы: отбор прозы отбрасывает короткие строки, а
    # короткие они по-разному в разных языках, и номер уезжал бы на перевод.
    ru = blocks(doc_master('04', 'ru'))
    idx = [i for i, b in enumerate(ru) if b.startswith(FORMS_ANCHOR)]
    assert idx, (u'в мастере 04 не нашёлся абзац, начинающийся на %r - '
                 u'лестницу строить не из чего' % FORMS_ANCHOR)
    ps = blocks(doc_master('04', lang))
    assert len(ps) == len(ru), (
        u'мастер 04 (%s) состоит из %d блоков, а русский - из %d: структура '
        u'разошлась, лестница собралась бы из чужого абзаца'
        % (lang, len(ps), len(ru)))
    p = ps[idx[0]]
    head, sep, rest = p.partition(':')
    assert sep, u'в абзаце форм (%s) нет двоеточия' % lang
    enum, sep2, tail = rest.partition(' - ')
    assert sep2, u'в абзаце форм (%s) нет тире после перечисления' % lang
    forms = [x.strip() for x in enum.split(',') if x.strip()]
    assert len(forms) == 8, (
        u'в мастере 04 (%s) форм %d, а не 8: %r. Абзац правили - проверьте '
        u'разбор.' % (lang, len(forms), forms))
    # последняя фраза абзаца и есть недостающая ступень
    gap = re.split(r'(?<=[.!?])\s', tail.strip())[-1].strip()
    assert gap, u'в абзаце форм (%s) не нашлась заключительная фраза' % lang

    o = [u'<ol class="ladder">']
    for i, f in enumerate(forms):
        o.append(u'<li class="ladder-step" style="--i:%d">%s</li>'
                 % (i, C.esc(f)))
    o.append(u'<li class="ladder-step ladder-gap" style="--i:8">%s</li>'
             % C.esc(gap))
    o.append(u'</ol>')
    return u'\n'.join(o)


def poster(theme, kicker, line, body, more):
    u"""Первая полоса: Манифест плакатом.

    Крупная строка - первые фразы Манифеста слово в слово, дальше продолжение
    того же абзаца мелким в две колонки. Картинок у сайта нет ни одной, и это
    не беда: у Манифеста есть голос, и набранный крупно он работает лучше
    любой фотографии.
    """
    return u'\n'.join([
        u'<section class="band band--%s band--poster">' % theme,
        u'<div class="band-in">',
        u'<p class="band-kicker">%s</p>' % C.esc(kicker),
        u'<h1 class="poster-line">%s</h1>' % md_inline(line),
        u'<div class="poster-body">%s</div>'
        % u''.join(u'<p>%s</p>' % md_inline(p) for p in body),
        u'<a class="band-more" href="%s">%s</a>' % (C.esc(more[1]), C.esc(more[0])),
        u'</div></section>',
    ])


def awakened(theme, lang):
    u"""Полоса Awakened Code: он сам, живьём, в рамке монитора.

    Не снимок экрана и не пересказ, а настоящая страница в iframe. Три довода:
    Awakened Code переносится на новый сайт КАК ЕСТЬ (решение Артура), значит
    копии быть не должно; дублирования нет - расходиться нечему; и он правда
    живой, со своей бегущей строкой и пульсацией.

    Грузится лениво: страница остаётся лёгкой, а 130 КБ его скриптов приезжают
    только когда до полосы доскроллили. Текст полосы лежит в HTML отдельно от
    рамки, поэтому правило «страница читается без JS» держится: монитор - это
    декорация, а не содержание.

    Названия эссе берутся из его же data/sliders.json, где они уже лежат на
    девяти языках.
    """
    path = os.path.join(SITE, 'awakened_code', 'data', 'sliders.json')
    assert os.path.isfile(path), u'нет %s - полосе нечего показать' % path
    data = json.load(io.open(path, encoding='utf-8'))
    assert lang in data, (
        u'в sliders.json нет языка %r: %s' % (lang, u', '.join(sorted(data))))
    items = (data[lang].get('left', [])[:AWAKENED_ITEMS]
             + data[lang].get('right', [])[:AWAKENED_ITEMS])
    assert items, u'в sliders.json (%s) нет ни одного эссе' % lang

    li = u''.join(
        u'<li><span class="code-item-title">%s</span>'
        u'<span class="code-item-key">%s</span></li>'
        % (C.esc(x.get('title', '')), C.esc(x.get('keyPhrase', '')))
        for x in items)

    return u'\n'.join([
        u'<section class="band band--%s band--code">' % theme,
        u'<div class="band-in code-row">',
        u'<div class="code-text">',
        u'<h2 class="band-title">%s</h2>' % C.esc(C.t(lang, 'nav.awakened_code')),
        u'<ul class="code-list">%s</ul>' % li,
        u'<a class="band-more" href="/awakened_code/">%s</a>'
        % C.esc(C.x(lang, 'read_more')),
        u'</div>',
        u'<div class="monitor">',
        u'<div class="monitor-screen">',
        # embed=1 просит Awakened Code убрать свой переключатель языка и
        # кнопку «К Earthlings»: язык уже выбран страницей, а возвращаться
        # некуда - мы и так на ней.
        u'<iframe src="/awakened_code/?embed=1" loading="lazy" '
        u'title="%s"></iframe>' % C.esc(C.t(lang, 'nav.awakened_code')),
        u'</div>',
        u'<div class="monitor-neck"></div><div class="monitor-foot"></div>',
        u'</div>',
        u'</div></section>',
    ])


# Платформа лежит соседним репозиторием: сайт и платформа - разные проекты, и
# сводить их в один репозиторий незачем. Путь переопределяется переменной
# окружения, как и путь к сайту в build_site_docs.
PLATFORM = os.environ.get('EARTHLINGS_PLATFORM') or os.path.join(
    os.path.dirname(SITE), 'earthlings-platform')
PLATFORM_APP = os.path.join(PLATFORM, 'app-starter')
# Адрес тура на живой платформе. Файлы названы по образцу `cells_ru.html`.
TOUR_URL = 'https://app.earth-lings.org/assets/tours/%s/%s_%s.html'


def _plat(lang):
    u"""Раздел `tours` из словаря платформы. Именно из её словаря, а не из
    словарей сайта: эти строки принадлежат платформе, и вторая их копия на
    стороне сайта разошлась бы с первой."""
    p = os.path.join(PLATFORM_APP, 'assets', 'js', 'i18n', '%s.json' % lang)
    assert os.path.isfile(p), (
        u'нет словаря платформы %s. Полоса платформы собирается из живых '
        u'словарей соседнего репозитория; если он лежит в другом месте, '
        u'укажите его переменной EARTHLINGS_PLATFORM.' % p)
    d = json.load(io.open(p, encoding='utf-8')).get('tours')
    assert d, u'в словаре платформы %s нет раздела tours' % lang
    return d


def tour_label(lang):
    u"""Подпись над лентой - «Интерактивный тур» платформы на девяти языках."""
    v = _plat(lang).get('buttonText')
    assert v, u'в словаре платформы %s нет tours.buttonText' % lang
    return v


def tour_newtab(lang):
    u"""«Открыть в новой вкладке» - подпись ссылки в адресной строке рамки.
    Лежит у платформы готовой на девяти языках, сочинять её незачем."""
    v = _plat(lang).get('openInNewTab')
    assert v, u'в словаре платформы %s нет tours.openInNewTab' % lang
    return v


def tours(lang):
    u"""Названия туров платформы на языке lang.

    Берутся ЖИВЫМИ из словарей самой платформы, а не переписываются сюда.
    Названия разделов - вещь платформы, и вторая копия разошлась бы с первой
    ровно так же, как разошлись когда-то меню сайта и его переводы.

    Порядок задаёт русский словарь: он и есть мастер. Каждый язык обязан иметь
    все тринадцать названий и все тринадцать файлов туров, иначе на главной
    появилась бы карточка, ведущая в никуда.

    Берётся `tours.sections`, а не `tours.<id>.title` из разметки платформы:
    ключей `tours.<id>.title` в словарях нет ни одного, поэтому карточки на
    самой платформе стоят русскими на всех языках. Это её отдельный дефект,
    и чинить его надо там; здесь достаточно не повторить его.
    """
    ru = _plat(u'ru').get('sections')
    mine = _plat(lang).get('sections')
    assert ru and mine, u'в словаре платформы (%s) нет tours.sections' % lang
    out = []
    for tid in ru:
        name = mine.get(tid)
        assert name, (
            u'в словаре платформы %s нет названия тура %r - карточка встала бы '
            u'на чужом языке' % (lang, tid))
        f = os.path.join(PLATFORM_APP, 'assets', 'tours', lang,
                         '%s_%s.html' % (tid, lang))
        assert os.path.isfile(f), (
            u'нет файла тура %s - карточка вела бы в никуда' % f)
        out.append((tid, name))
    assert out, u'у платформы не нашлось ни одного тура'
    return out


def platform(theme, lang, title, lead_ps):
    u"""Полоса платформы: слева текст, справа живой тур, под ними карточки.

    В рамке идёт НАСТОЯЩАЯ страница тура с платформы, а не снимок, и туры
    сменяют друг друга по кругу. Карточки под экраном - и оглавление, и
    переключатель: нажатие меняет то, что идёт на экране, а не уводит со
    страницы.

    Карточки прямые. Языковой слайдер тремя полосами выше скошен, и повторять
    скос значило бы сделать две разные вещи на одно лицо: там девять
    письменностей одного текста, здесь тринадцать разделов работающего
    приложения. Разное содержание - разная форма.

    ЧТО ПРОИСХОДИТ БЕЗ СКРИПТА. Рамка помечена hidden и не показывается вовсе:
    пустой экран с кнопкой, которая ничего не делает, хуже, чем его отсутствие.
    Остаётся текст и тринадцать карточек обычными ссылками на туры - полоса
    читается и работает целиком. Скрипт только поднимает рамку и перехватывает
    нажатия. Правило «страница не зависит от JS» этим не нарушено: экран -
    декорация, содержание лежит в разметке.

    Кнопка остановки не украшение: показ, который сам меняется дольше пяти
    секунд, обязан иметь способ остановки (WCAG 2.2.2). Наведение и фокус
    останавливают его тоже, но одного наведения мало - с клавиатуры и с
    сенсорного экрана его нет.
    """
    items = tours(lang)
    cards = u''.join(
        u'<li class="tourcard"><a href="%s" data-tour="%s">'
        u'<span class="tourcard-n">%02d</span>'
        u'<span class="tourcard-title">%s</span></a></li>'
        % (C.esc(TOUR_URL % (lang, tid, lang)), C.esc(tid), i, C.esc(name))
        for i, (tid, name) in enumerate(items, 1))

    label = C.esc(tour_label(lang))
    first = TOUR_URL % (lang, items[0][0], lang)
    return u'\n'.join([
        u'<section class="band band--%s band--platform">' % theme,
        u'<div class="band-in">',
        u'<div class="platform-row">',
        u'<div class="platform-text">',
        u'<h2 class="band-title">%s</h2>' % C.esc(title),
        u'<div class="band-lead">%s</div>'
        % u''.join(u'<p>%s</p>' % md_inline(p) for p in lead_ps),
        u'<a class="band-more" href="%s">%s</a>'
        % (C.esc(doc_href('12', lang)), C.esc(C.x(lang, 'read_more'))),
        u'<a class="band-cta" href="%s">%s</a>'
        % (C.esc(C.APP_URL % lang), C.esc(C.t(lang, 'nav.platform_btn'))),
        u'</div>',
        # hidden снимает скрипт. Атрибут, а не класс: без скрипта рамку прячет
        # сам браузер, и ни одного правила CSS для этого не нужно.
        u'<div class="platform-screen" data-tours hidden>',
        # Рамка браузера, а не монитора: у Awakened Code двумя полосами ниже
        # монитор на подставке, и второй такой же читался бы как повтор. Здесь
        # это и честнее - в рамке действительно веб-страница, и в адресной
        # строке видно какая.
        u'<div class="browser">',
        u'<div class="browser-bar">',
        u'<span class="browser-dots" aria-hidden="true"></span>',
        u'<span class="browser-url" data-url>%s</span>'
        % C.esc(re.sub(r'^https?://', '', first)),
        u'<a class="browser-open" data-open href="%s" target="_blank" '
        u'rel="noopener">%s</a>' % (C.esc(first), C.esc(tour_newtab(lang))),
        u'</div>',
        u'<div class="browser-screen" data-screen></div>',
        u'</div>',
        u'<button type="button" class="tour-toggle" data-toggle '
        u'aria-pressed="false" data-pause="%s" data-resume="%s">%s</button>'
        % (C.esc(C.x(lang, 'pause')), C.esc(C.x(lang, 'resume')),
           C.esc(C.x(lang, 'pause'))),
        u'</div>',
        u'</div>',
        u'<p class="platform-tours-label">%s</p>' % label,
        u'<ul class="tourslider" aria-label="%s">%s</ul>' % (label, cards),
        u'</div></section>',
    ])


# Раздел «Шесть шагов» документа 14 в номерах блоков. Номера, а не поиск по
# тексту: искать «## 2.» значило бы завязаться на нумерацию разделов, а её
# правят чаще, чем состав документа. Каждый номер проверяется разбором: не
# разобралось - сборка падает.
STEPS_HEAD = 13                  # «## 2. Шесть шагов»
STEPS_FIRST, STEPS_LAST = 14, 19  # сами шаги
STEPS_NOTE = 20                  # врезка о том, что биометрия не сохраняется
REQS_FIRST, REQS_LAST = 6, 9     # четыре условия вступления, включая взнос

_STEP_RE = re.compile(r'^\*\*(\d+)\.\s*(.+?)\*\*\s*(.+)$')
_REQ_RE = re.compile(r'^\*\*(.+?)\*\*\s*-\s*(.+)$')


def steps(theme, lang, lead_ps):
    u"""Полоса «как вступить»: четыре условия, шесть шагов, слово о биометрии.

    Всё - текст мастера 14, раздел 2, слово в слово. Пересказывать процедуру
    своими словами на главной нельзя: это единственное место, где человек
    решает, отдавать ли свои документы на проверку, и расхождение между
    обещанием на главной и текстом документа здесь дороже всего.

    Живой системы регистрации в полосе НЕТ и быть не должно, хотя рамка для
    неё уже написана двумя полосами выше. Первый экран регистрации - форма с
    почтой, именем и страной, а следом камера. Форму, собирающую личные
    данные, показывают со своего адреса и ниоткуда больше: чужая страница в
    рамке - ровно то, от чего защищаются запретом на обрамление, и заводить
    у людей привычку вводить такое в рамке на другом сайте нельзя. Полоса
    ведёт на id.earth-lings.org кнопкой.
    """
    bs = blocks(doc_master('14', lang))
    ru = blocks(doc_master('14', 'ru'))
    assert len(bs) == len(ru), (
        u'мастер 14 (%s) состоит из %d блоков, а русский - из %d: раздел с '
        u'шагами собрался бы из чужих абзацев' % (lang, len(bs), len(ru)))

    head = re.sub(r'^#+\s*\d*\.?\s*', '', bs[STEPS_HEAD - 1]).strip()
    assert head and not head.startswith('#'), (
        u'блок %d мастера 14 (%s) - не заголовок раздела, а %r'
        % (STEPS_HEAD, lang, bs[STEPS_HEAD - 1][:60]))

    items = []
    for n in range(STEPS_FIRST, STEPS_LAST + 1):
        m = _STEP_RE.match(bs[n - 1])
        assert m, (
            u'блок %d мастера 14 (%s) не разобрался как шаг: %r. Раздел '
            u'«Шесть шагов» правили - проверьте номера в build_home_v2.'
            % (n, lang, bs[n - 1][:80]))
        items.append((m.group(1), m.group(2).strip().rstrip('.'), m.group(3)))
    assert len(items) == 6, u'шагов должно быть шесть, а разобралось %d' % len(items)

    reqs = []
    for n in range(REQS_FIRST, REQS_LAST + 1):
        m = _REQ_RE.match(bs[n - 1])
        assert m, (
            u'блок %d мастера 14 (%s) не разобрался как условие вступления: %r'
            % (n, lang, bs[n - 1][:80]))
        reqs.append((m.group(1), m.group(2).rstrip('.')))

    note = re.sub(r'^>\s*', '', bs[STEPS_NOTE - 1])
    assert note != bs[STEPS_NOTE - 1], (
        u'блок %d мастера 14 (%s) - не врезка: %r'
        % (STEPS_NOTE, lang, bs[STEPS_NOTE - 1][:80]))

    return u'\n'.join([
        u'<section class="band band--%s band--steps">' % theme,
        u'<div class="band-in">',
        u'<h2 class="band-title">%s</h2>' % C.esc(head),
        u'<div class="band-lead">%s</div>'
        % u''.join(u'<p>%s</p>' % md_inline(p) for p in lead_ps),
        u'<ul class="reqs">%s</ul>'
        % u''.join(u'<li><span class="req-name">%s</span>'
                   u'<span class="req-text">%s</span></li>'
                   % (C.esc(name), md_inline(text)) for name, text in reqs),
        u'<ol class="steps">%s</ol>'
        % u''.join(u'<li class="step"><span class="step-n">%s</span>'
                   u'<span class="step-name">%s</span>'
                   u'<span class="step-text">%s</span></li>'
                   % (C.esc(num), C.esc(name), md_inline(text))
                   for num, name, text in items),
        u'<p class="steps-note">%s</p>' % md_inline(note),
        u'<a class="band-more" href="%s">%s</a>'
        % (C.esc(doc_href('14', lang)), C.esc(C.x(lang, 'read_more'))),
        u'<a class="band-cta" href="%s">%s</a>'
        % (C.esc(C.CTA_URL % lang), C.esc(C.t(lang, 'nav.become_earthling'))),
        u'</div></section>',
    ])


def reserved(theme, n):
    u"""Полоса под содержимое, которого ещё нет.

    Ни одного слова: место обозначено рамкой и номером, а номер не требует
    перевода. Написать сюда «скоро» на девяти языках значило бы завести девять
    строк, которые потом придётся вычищать.
    """
    return (u'<section class="band band--%s band--reserved">'
            u'<div class="band-in"><div class="reserved-slot">%d</div></div>'
            u'</section>' % (theme, n))


def band(theme, title, lead, more=None, items=None, cta=None,
         slider=None, extra=None):
    o = ['<section class="band band--%s"><div class="band-in">' % theme]
    o.append('<h2 class="band-title">%s</h2>' % C.esc(title))
    o.append('<div class="band-lead">%s</div>'
             % ''.join('<p>%s</p>' % md_inline(p) for p in lead))
    if extra:
        o.append(extra)
    if items:
        o.append('<ul class="band-list">%s</ul>'
                 % ''.join('<li><a href="%s">%s</a></li>' % (C.esc(h), C.esc(t))
                           for t, h in items))
    if slider:
        # Слайдер выходит из контейнера во всю ширину: скошенные слайды должны
        # уезжать за оба края, иначе не видно, что их больше, чем помещается.
        o.append('</div>')
        o.append(slider)
        o.append('<div class="band-in">')
    if more:
        o.append('<a class="band-more" href="%s">%s</a>' % (C.esc(more[1]),
                                                            C.esc(more[0])))
    if cta:
        o.append('<a class="band-cta" href="%s">%s</a>' % (C.esc(cta[1]),
                                                           C.esc(cta[0])))
    o.append('</div></section>')
    return '\n'.join(o)


def build_index(lang):
    manifest = read_master(os.path.join(MANIFEST_DIR, '%s-manifest.md' % lang))
    more = C.x(lang, 'read_more')
    bands = []

    for i, (theme, what, nums, anchor) in enumerate(BANDS):
        if what == 'reserved':
            bands.append(reserved(theme, i + 1))
        elif what == 'awakened':
            bands.append(awakened(theme, lang))
        elif what == 'steps':
            assert has_doc('14', lang), u'документа 14 нет на языке %s' % lang
            bands.append(steps(theme, lang,
                               lead(load, '14', nums, anchor, lang)))
        elif what == 'platform':
            assert has_doc('12', lang), u'документа 12 нет на языке %s' % lang
            bands.append(platform(theme, lang, title_of(doc_master('12', lang)),
                                  lead(load, '12', nums, anchor, lang)))
        elif what == 'manifest':
            ps = lead(load, 'manifest', nums, anchor, lang)
            sents = re.split(r'(?<=[.!?])\s+', ps[0])
            assert len(sents) > POSTER_SENTENCES, (
                u'первый абзац Манифеста (%s) короче %d фраз - плакат собрать '
                u'не из чего' % (lang, POSTER_SENTENCES + 1))
            bands.append(poster(
                theme, title_of(manifest),
                u' '.join(sents[:POSTER_SENTENCES]),
                [u' '.join(sents[POSTER_SENTENCES:])] + ps[1:],
                (more, '/%s/manifest.html' % lang)))
        elif what == 'legal':
            items = [(title_of(doc_master(d, lang)), doc_href(d, lang))
                     for d in LEGAL_DOCS if has_doc(d, lang)]
            assert items, u'ни один правовой документ не доступен на %s' % lang
            bands.append(band(theme, C.t(lang, 'nav.legal_base'),
                              lead(load, LEGAL_LEAD_DOC, nums, anchor, lang),
                              items=items, extra=ladder(lang)))
        else:
            num = what.split(':')[1]
            assert has_doc(num, lang), u'документа %s нет на языке %s' % (num, lang)
            md = doc_master(num, lang)
            cta = ((C.t(lang, 'nav.become_earthling'), C.CTA_URL % lang)
                   if num == '14' else None)
            bands.append(band(theme, title_of(md),
                              lead(load, num, nums, anchor, lang),
                              more=(more, doc_href(num, lang)), cta=cta,
                              slider=langslider(lang) if num == '01' else None,
                              extra=timeline(lang) if num == '20' else None))

    title = C.t(lang, 'page.title')
    desc = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '',
                  md_inline(prose(manifest)[0])))[:300]
    inner = '<main id="main">%s</main>' % '\n'.join(bands)
    return wrap(lang, inner, '%s/%s/' % (ORIGIN, lang), title, desc,
                lambda c: '/%s/' % c,
                ['<link rel="stylesheet" href="/css/home.css">',
                 # Единственная его работа - подсветить текущую веху шкалы.
                 # Без него шкала читается целиком, просто без подсветки.
                 '<script defer src="/js/home.js"></script>'])


def build_manifest(lang):
    md = read_master(os.path.join(MANIFEST_DIR, '%s-manifest.md' % lang))
    doc = md2doc.parse(md)
    assert doc['title'], u'в Манифесте не найден заголовок H1'
    body = md2doc.render_body(doc)

    o = ['<main class="%s" id="main"><div class="sheet">' % ROOT,
         '<header class="doc-head"><h1 class="doc-title">%s</h1>'
         '<div class="rule-double"></div></header>' % C.esc(doc['title']),
         body]
    assert lang in SIGN, u'нет подписи под Манифестом для языка %s' % lang
    o.append('<p class="sign">%s</p>' % C.esc(SIGN[lang]))
    if lang in PDF:
        href, label = PDF[lang]
        assert os.path.isfile(os.path.join(SITE, href.lstrip('/'))), (
            u'нет файла %s - ссылка на PDF была бы битой' % href)
        o.append('<p><a class="pdf-link" href="%s">%s</a></p>'
                 % (href, C.esc(label)))
    o.append('</div></main>')

    desc = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '',
                  md_inline(prose(md)[0])))[:300]
    return wrap(lang, '\n'.join(o),
                '%s/%s/manifest.html' % (ORIGIN, lang),
                '%s | Earthlings' % doc['title'], desc,
                lambda c: '/%s/manifest.html' % c,
                ['<link rel="stylesheet" href="/css/home.css">'])


def main():
    dry = '--dry' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    langs = args or [l for l in ALL_LANGS if os.path.isfile(
        os.path.join(MANIFEST_DIR, '%s-manifest.md' % l))]
    assert langs, u'нет ни одного мастера Манифеста'

    for lang in langs:
        assert lang in SLUGS, (
            u'для языка %r не заданы слаги: ссылки с главной на документы '
            u'легли бы мимо' % lang)
        d = os.path.join(OUT, lang)
        if not os.path.isdir(d) and not dry:
            os.makedirs(d)
        for name, page in (('index.html', build_index(lang)),
                           ('manifest.html', build_manifest(lang))):
            if not dry:
                io.open(os.path.join(d, name), 'w', encoding='utf-8',
                        newline='\n').write(page)
            text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ',
                          page.split('<body', 1)[1])).strip()
            print('OK   _v2/%s/%-14s %3d КБ, текста без JS: %5d знаков'
                  % (lang, name, len(page.encode('utf-8')) // 1024, len(text)))


if __name__ == '__main__':
    main()
