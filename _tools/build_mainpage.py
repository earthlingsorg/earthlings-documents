# -*- coding: utf-8 -*-
"""ОТКЛЮЧЁН. Сборка главной страницы БОЕВОГО сайта из мастера Обращения.

Скрипт пишет в `mainpage/<язык>/index.html` боевого дерева, а боевой сайт
заменяется новым и больше не правится - ни руками, ни пересборкой. Главные
нового сайта собирает `build_home_v2.py`.

Отключён 2026-08-31, и не из осторожности: собрать он больше не может.
Скрипт брал последнюю строку мастера Обращения и превращал её в ссылку на
документ об учредительном периоде. Строки, на которую он опирался («Мы
выбираем друг друга»), в мастере нет с 31 августа - текст Обращения заменён
целиком. Таблица `ONWARD_TEXT_BY_LANG` снята вместе с этой опорой: держать в
публичном репозитории список фраз из текста, которого больше нет, значит
однажды поверить ему.

Что ниже - оставлено как есть, до дня подмены. Тогда решается судьба всего
боевого дерева разом, и этот файл уходит вместе с ним.

Ниже - прежнее описание.

Сборка главной страницы RU из мастера Обращения тем же шаблоном, что и корпус.

Главная набирается ровно как документ: та же гарнитура, те же отбивки, та же
мера строки. Своего оформления у неё нет - отдельная вёрстка на главной
разъезжается с корпусом при первой же правке темы.

Своего оформления и своего подвала у страницы нет: она грузится внутрь
оболочки сайта, где подвал уже стоит.

Использование:
  python build_mainpage.py            собрать mainpage/ru/index.html
  python build_mainpage.py en         собрать mainpage/en/index.html
  python build_mainpage.py --dry      показать, ничего не записывая
"""
import io, os, re, sys, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md2doc

if os.environ.get('ALLOW_LEGACY_BUILD') != '1':
    print('')
    print('  ОТКАЗ: сборка главной боевого сайта отключена.')
    print('')
    print('  Боевой сайт заменяется новым и больше не правится.')
    print('  Главные нового сайта собирает build_home_v2.py.')
    print('')
    print('  Опора скрипта - последняя строка мастера Обращения - снята:')
    print('  текст Обращения заменён целиком 31 августа 2026.')
    print('')
    sys.exit(2)
from build_site_docs import SITE, REPO, ROOT, LANGS_BY_DOC
import site_guard as guard

# Обращение лежит вне корпуса: он ничего не устанавливает, предложения к нему
# не принимаются и на голосование он не выносится (Учредительный период, 02).
ADDRESS_DIR = os.path.join(REPO, '_address')

LANG = 'ru'
for a in sys.argv[1:]:
    if not a.startswith('--'):
        LANG = a

MASTER = os.path.join(ADDRESS_DIR, '%s-address.md' % LANG)
PAGE = os.path.join(SITE, 'mainpage', LANG, 'index.html')
assert os.path.isfile(MASTER), (
    'нет мастера Обращения для языка "%s": %s. Языки, для которых он есть: %s' % (
        LANG, MASTER,
        ', '.join(sorted(f[:2] for f in os.listdir(ADDRESS_DIR) if f.endswith('-address.md')))))
assert os.path.isfile(PAGE), PAGE

# Последняя строка Обращения ведёт на документ об учредительном периоде: это
# самый прямой ответ на «что дальше» именно сейчас. Ссылка, не кнопка -
# оформление остаётся документным. Прежним якорем было слово «Вперёд.»; оно
# снято, потому что так заканчивается манифест шифропанков.
ONWARD_DOC = '20'
# Адрес берём из той же таблицы, что и сборщик корпуса: держать его здесь
# отдельной строкой значит забыть про него на следующем переименовании.
from build_site_docs import doc_href  # noqa: E402
ONWARD_HREF = doc_href(ONWARD_DOC, LANG)
# Последняя строка Обращения на каждом языке своя. Языка нет в таблице - сборка
# остановится на проверке ниже, а не поставит ссылку молча мимо.
ONWARD_TEXT_BY_LANG = {}   # снято: фразы из прежнего текста Обращения
# Прежде здесь стояла последняя строка Обращения на семи языках. Текст
# заменён 2026-08-31, строки больше нет ни на одном языке, и держать её
# копию в публичном репозитории не для чего.

# Подпись под Обращением. Обращение подписывают его авторы, а не народ
# (Учредительный период, раздел 02), поэтому здесь команда, а не «Earthlings».
SIGN_BY_LANG = {
    'ru': 'Команда Earthlings',
    'en': 'The Earthlings team',
    'de': 'Das Team der Earthlings',
    'fr': "L'équipe Earthlings",
    'es': 'El equipo Earthlings',
    'ka': 'Earthlings-ის გუნდი',
    'zh': 'Earthlings 团队',
}

# Ссылка на PDF. Файла для языка нет - блок не выводится, битой ссылки не будет.
PDF_BY_LANG = {
    'ru': ('/downloads/manifest-prinadlezhnosti-ru.pdf', 'Скачать манифест в PDF'),
    'en': ('/downloads/manifesto-of-belonging-en.pdf', 'Download the manifesto as PDF'),
    'de': ('/downloads/manifest-der-zugehoerigkeit-de.pdf', 'Manifest als PDF herunterladen'),
    'fr': ('/downloads/manifeste-d-appartenance-fr.pdf', 'Télécharger le Manifeste en PDF'),
    'es': ('/downloads/manifiesto-de-la-pertenencia-es.pdf', 'Descargar el Manifiesto en PDF'),
    'ka': ('/downloads/manifesto-of-belonging-ka.pdf', 'ჩამოტვირთეთ მანიფესტი PDF-ად'),
    'zh': ('/downloads/manifesto-of-belonging-zh.pdf', '下载宣言 PDF'),
}

PDF_SVG = ('<svg viewBox="0 0 16 19" fill="none" stroke="currentColor" stroke-width="1.3" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M9.4 1H2.6C2 1 1.5 1.5 1.5 2.1v14.8c0 .6.5 1.1 1.1 1.1h10.8c.6 0 '
           '1.1-.5 1.1-1.1V6.1z"/><path d="M9.4 1v5.1h5.1"/><path d="M5 13.4h6"/></svg>')
assert LANG in ONWARD_TEXT_BY_LANG, (
    'не задана последняя строка Обращения для языка "%s": без неё ссылка на '
    'учредительный период не встанет. Языки: %s'
    % (LANG, ', '.join(sorted(ONWARD_TEXT_BY_LANG))))
ONWARD_TEXT = ONWARD_TEXT_BY_LANG[LANG]

STYLE = u"""<style>
/* Оформление приезжает из docs-statute.css. Здесь только отступ: шапка сайта
   - fixed, и без него текст уходил бы под неё. Высота шапки плюс два
   сантиметра воздуха - столько же, сколько у страниц документов. */
.statute{padding-top:calc(var(--header-height,64px) + 76px)}
/* Подпись идёт после кнопки и закрывает текст. Стоять перед ней она не может:
   там она работает меткой голоса, и всё, что ниже, читается речью команды -
   «мы» манифеста сужается до неё одной. Ниже подписи остаётся только ссылка
   на PDF: она принадлежит странице, а не документу, поэтому и стоит вне
   подписанного текста. */
.statute .sign{
  margin: 2.8rem auto 0; text-align: center;
  font-style: italic; font-size: .92rem; color: var(--ink-soft);
}
.statute .sign::before{
  content: ""; display: block; width: 56px; height: 0;
  margin: 0 auto 1.2rem; border-top: 1px solid var(--rule-soft);
}
/* Последняя строка манифеста - одновременно дверь в учредительный период.
   Тонкий синий контур цветом --navy: это единственный синий в палитре
   листа, произвольный оттенок выбивался бы из корпуса. */
.statute .onward{ margin: 3.4rem 0 0; text-align: center; }
.statute .onward a{
  display: inline-block; padding: .95rem 2.4rem;
  border: 1px solid var(--navy); color: var(--navy);
  text-decoration: none; letter-spacing: .02em;
  background: transparent;
  transition: box-shadow .25s ease;
}
/* Цвет надписи наследуется от ссылки: иначе .statute strong перебивает его
   своим navy и на наведении текст сливается с рамкой. */
.statute .onward a strong{ color: inherit; }
/* На наведении контур становится вдвое толще, а заливки нет. Толщина набрана
   внутренней тенью, а не border-width: рамка в 2px сдвинула бы кнопку. */
.statute .onward a:hover,
.statute .onward a:focus-visible{
  box-shadow: inset 0 0 0 1px var(--navy);
}
.statute .onward a:focus-visible{ outline: 2px solid var(--gold); outline-offset: 3px; }
@media (max-width: 480px){
  .statute .onward a{ padding: .85rem 1.5rem; }
}
/* Скачивание - действие второго плана. Красный здесь опознавательный знак
   формата, а не сигнал тревоги: приглушённый кирпичный, без рамки и без
   заливки в покое, мельче основной кнопки. Внимание он забирает ровно
   настолько, чтобы его заметили рядом с навигационной кнопкой. */
.statute .get-pdf{ --pdf: #9a3324; margin: 1.6rem 0 0; text-align: center; }
.statute .get-pdf a{
  display: inline-flex; align-items: center; gap: .5rem;
  padding: .45rem .8rem; border-radius: 3px;
  font-size: .88rem; color: var(--pdf); text-decoration: none;
  background: transparent;
  transition: background-color .25s ease;
}
.statute .get-pdf a span{ border-bottom: 1px solid rgba(154,51,36,.35); padding-bottom: 1px; }
.statute .get-pdf svg{ width: 15px; height: 18px; flex: 0 0 auto; }
.statute .get-pdf a:hover,
.statute .get-pdf a:focus-visible{ background: rgba(154,51,36,.07); }
.statute .get-pdf a:hover span,
.statute .get-pdf a:focus-visible span{ border-bottom-color: var(--pdf); }
.statute .get-pdf a:focus-visible{ outline: 2px solid var(--pdf); outline-offset: 2px; }
</style>"""

UMAMI = ('<!--umami-start--><script defer src="https://stats.earth-lings.org/script.js" '
         'data-website-id="badb2091-1880-4933-bf4e-8d7be1f7ce44"></script>'
         '<script defer src="/js/umami-tracker.js?v=1"></script><!--umami-end-->')


def head_html():
    """Шапку прежней страницы сохраняем целиком: там описания, og и hreflang."""
    s = io.open(PAGE, encoding='utf-8').read()
    head = s.split('</head>', 1)[0]
    assert '<title>' in head and 'hreflang' in head, 'шапка неполная'
    # стиль корпуса нужен и при прямом открытии страницы, не только внутри оболочки
    link = '<link rel="stylesheet" href="/css/docs-statute.css?v=1">'
    if link not in head:
        head = head.replace('<link rel="stylesheet" href="/css/fonts-deco.css?v=2">',
                            '<link rel="stylesheet" href="/css/fonts-deco.css?v=2">' + link, 1)
    return head + '</head>'


def link_onward(body):
    """Последнюю строку Обращения делаем ссылкой на учредительный период."""
    old = '<p><strong>%s</strong></p>' % ONWARD_TEXT
    if body.count(old) != 1:
        return body, False
    new = ('<p class="onward"><a href="%s" data-action="open-document" data-doc="%s">'
           '<strong>%s</strong></a></p>' % (ONWARD_HREF, ONWARD_DOC, ONWARD_TEXT))
    return body.replace(old, new, 1), True


def sign_and_pdf():
    """Подпись авторов и ссылка на PDF - они принадлежат странице, не тексту.

    В мастере их нет намеренно: подпись не часть Обращения, а указание, чей
    это голос, и в переводе она не должна прогоняться через текст.
    """
    out = ['<p class="sign">%s</p>' % html.escape(SIGN_BY_LANG[LANG])]
    href, label = PDF_BY_LANG.get(LANG, (None, None))
    if href and os.path.isfile(os.path.join(SITE, href.lstrip('/'))):
        out.append('<p class="get-pdf"><a href="%s" download>%s<span>%s</span></a></p>'
                   % (href, PDF_SVG, html.escape(label)))
    else:
        sys.stderr.write(
            'ВНИМАНИЕ %s: нет файла %s - блок скачивания не выводится. '
            'Собрать PDF новой редакции и пересобрать страницу.\n' % (LANG, href))
    return '\n'.join(out)


def main():
    dry = '--dry' in sys.argv
    md = io.open(MASTER, encoding='utf-8').read()
    assert md.strip(), 'пустой мастер'
    doc = md2doc.parse(md)
    assert doc['title'], 'не найден заголовок H1'

    title_html = html.escape(doc['title'])
    head = ('<header class="doc-head col"><h1 class="doc-title">%s</h1>'
            '<div class="rule-double"></div></header>' % title_html)
    body = md2doc.render_body(doc)
    body, linked = link_onward(body)
    assert linked, (
        'последняя строка мастера не совпадает с ONWARD_TEXT для языка "%s" '
        '(%r) - ссылка на учредительный период не поставлена. Правьте таблицу, '
        'а не мастер.' % (LANG, ONWARD_TEXT))
    body += '\n' + sign_and_pdf()

    page = '\n'.join([
        head_html(),
        '<body class="%s">' % ROOT,
        '<main>',
        '<div class="%s">' % ROOT,
        STYLE,
        '<div class="sheet">',
        head,
        body,
        '</div>',
        '</div>',
        '</main>',
        UMAMI,
        '</body>',
        '</html>',
        '',
    ])

    guard.write(PAGE, page, dry=dry)
    print("главная собрана из мастера: %d абзацев, %d КБ"
          % (len(re.findall(r"<p[ >]", body)), len(page.encode("utf-8")) // 1024))


if __name__ == '__main__':
    # Отказ замка печатается человеку, а не трассировкой: произошло
    # ровно то, ради чего он поставлен, и это не поломка скрипта.
    try:
        main()
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
