# -*- coding: utf-8 -*-
"""Сборка главной страницы RU из мастера Манифеста тем же шаблоном, что и корпус.

Главная набирается ровно как документ: та же гарнитура, те же отбивки, та же
мера строки. Своего оформления у неё нет - отдельная вёрстка на главной
разъезжается с корпусом при первой же правке темы.

Своего оформления и своего подвала у страницы нет: она грузится внутрь
оболочки сайта, где подвал уже стоит.

Использование:
  python build_mainpage.py            собрать mainpage/ru/index.html
  python build_mainpage.py --dry      показать, ничего не записывая
"""
import io, os, re, sys, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md2doc
from build_site_docs import SITE, MD_DIR, ROOT

MASTER = os.path.join(MD_DIR, 'МАНИФЕСТ ПРИНАДЛЕЖНОСТИ.md')
PAGE = os.path.join(SITE, 'mainpage', 'ru', 'index.html')
assert os.path.isfile(MASTER), MASTER
assert os.path.isfile(PAGE), PAGE

# Последняя строка Манифеста ведёт на документ об учредительном периоде: это
# самый прямой ответ на «что дальше» именно сейчас. Ссылка, не кнопка -
# оформление остаётся документным. Прежним якорем было слово «Вперёд.»; оно
# снято, потому что так заканчивается манифест шифропанков.
ONWARD_DOC = '20'
# Адрес берём из той же таблицы, что и сборщик корпуса: держать его здесь
# отдельной строкой значит забыть про него на следующем переименовании.
from build_site_docs import doc_href  # noqa: E402
ONWARD_HREF = doc_href(ONWARD_DOC)
ONWARD_TEXT = 'Мы выбираем друг друга.'

STYLE = u"""<style>
/* Оформление приезжает из docs-statute.css. Здесь только отступ: шапка сайта
   - fixed, и без него текст уходил бы под неё. Высота шапки плюс два
   сантиметра воздуха - столько же, сколько у страниц документов. */
.statute{padding-top:calc(var(--header-height,64px) + 76px)}
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
    """Последнюю строку Манифеста делаем ссылкой на учредительный период."""
    old = '<p><strong>%s</strong></p>' % ONWARD_TEXT
    if body.count(old) != 1:
        return body, False
    new = ('<p class="onward"><a href="%s" data-action="open-document" data-doc="%s">'
           '<strong>%s</strong></a></p>' % (ONWARD_HREF, ONWARD_DOC, ONWARD_TEXT))
    return body.replace(old, new, 1), True


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
    assert linked, 'последний абзац мастера изменился - ссылка «Вперёд.» не поставлена'

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

    if not dry:
        io.open(PAGE, 'w', encoding='utf-8', newline='\n').write(page)
    print("главная собрана из мастера: %d абзацев, %d КБ"
          % (len(re.findall(r"<p[ >]", body)), len(page.encode("utf-8")) // 1024))


if __name__ == '__main__':
    main()
