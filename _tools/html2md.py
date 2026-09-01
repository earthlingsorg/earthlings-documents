# -*- coding: utf-8 -*-
"""Восстановление .md-мастера из живой страницы сайта.

Нужен для документов, у которых мастера не осталось: текст берётся с сайта и
переводится обратно в markdown, чтобы дальше корпус собирался из одного
источника. Разбор идёт по дереву, а не регулярками: разметка живых страниц
вложенная, и регулярки на ней молча теряют куски.

Использование:
  python html2md.py <вход.html> <выход.md>
Затем обязательно сверить: verify_md_html.py покажет, всё ли слово в слово.
"""
import io, os, re, sys, html
from html.parser import HTMLParser
import site_guard as guard

INLINE = {'a', 'strong', 'b', 'em', 'i', 'span', 'code', 'sup', 'sub', 'br', 'abbr'}
SKIP = {'script', 'style', 'svg', 'nav', 'head'}
HEADING = {'h1': '# ', 'h2': '## ', 'h3': '### ', 'h4': '#### ', 'h5': '#### ', 'h6': '#### '}
QUOTE_CLASSES = ('important-box', 'highlight-box', 'note', 'callout', 'warning-box')
END_QUOTE = '\x00/quote'   # служебная отметка конца врезки, в текст не попадает


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []          # готовые блоки markdown
        self.buf = []          # текст текущего блока
        self.block = None      # тег текущего блока
        self.skip = 0
        self.list_stack = []   # 'ul' / ['ol', счётчик]
        self.quote = 0
        self.href = []
        self.row = None        # текущая строка таблицы
        self.table = None      # накопленные строки таблицы
        self.subtitle = False

    # ---------------------------------------------------------- служебное
    def emit(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            self.out.append(text)

    def flush(self):
        if not self.buf:
            self.block = None
            return
        text = re.sub(r'\s+', ' ', ''.join(self.buf)).strip()
        self.buf = []
        b, self.block = self.block, None
        if not text:
            return
        if b in HEADING:
            self.emit(HEADING[b] + text)
        elif b == 'li':
            if self.list_stack and self.list_stack[-1][0] == 'ol':
                self.list_stack[-1][1] += 1
                self.emit('%d. %s' % (self.list_stack[-1][1], text))
            else:
                self.emit('- ' + text)
        elif b in ('td', 'th'):
            self.row.append(text)
        elif self.subtitle:
            self.emit('**%s**' % text)
            self.subtitle = False
        elif self.quote:
            self.emit('> ' + text)
        else:
            self.emit(text)

    # ---------------------------------------------------------- разбор
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get('class', '')
        if tag in SKIP:
            self.skip += 1
            return
        if self.skip:
            return

        if tag in INLINE:
            if tag in ('strong', 'b'):
                self.buf.append('**')
            elif tag in ('em', 'i'):
                self.buf.append('*')
            elif tag == 'a':
                self.buf.append('[')
                self.href.append(a.get('href', ''))
            elif tag == 'br':
                self.buf.append(' ')
            return

        self.flush()

        if tag == 'table':
            self.table = []
        elif tag == 'tr':
            self.row = []
        elif tag in ('td', 'th', 'li') or tag in HEADING or tag == 'p':
            self.block = tag
            if tag == 'p' and 'document-subtitle' in cls:
                self.subtitle = True
        elif tag == 'ul':
            self.list_stack.append(['ul', 0])
        elif tag == 'ol':
            self.list_stack.append(['ol', 0])
        elif tag in ('div', 'section', 'blockquote'):
            if tag == 'blockquote' or any(c in cls for c in QUOTE_CLASSES):
                self.quote += 1
                self._quote_tag = tag

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return

        if tag in INLINE:
            if tag in ('strong', 'b'):
                self.buf.append('**')
            elif tag in ('em', 'i'):
                self.buf.append('*')
            elif tag == 'a':
                href = self.href.pop() if self.href else ''
                self.buf.append('](%s)' % href if href else ']')
            return

        self.flush()

        if tag == 'tr' and self.row is not None:
            if self.table is not None and self.row:
                self.table.append(self.row)
            self.row = None
        elif tag == 'table' and self.table is not None:
            self.emit_table()
        elif tag in ('ul', 'ol') and self.list_stack:
            self.list_stack.pop()
        elif tag in ('div', 'section', 'blockquote') and self.quote:
            self.quote -= 1
            if not self.quote:
                self.out.append(END_QUOTE)   # граница врезки

    def handle_data(self, data):
        if self.skip:
            return
        if self.block or self.buf:
            self.buf.append(data)
        elif data.strip():
            # текст вне блока - не терять
            self.buf.append(data)
            self.block = 'p'

    def emit_table(self):
        rows, self.table = self.table, None
        if not rows:
            return
        width = max(len(r) for r in rows)
        rows = [r + [''] * (width - len(r)) for r in rows]
        self.out.append('| ' + ' | '.join(rows[0]) + ' |')
        self.out.append('|' + '---|' * width)
        for r in rows[1:]:
            self.out.append('| ' + ' | '.join(r) + ' |')

    def result(self):
        self.flush()
        return self.out


def convert(src):
    s = io.open(src, encoding='utf-8').read()
    s = re.sub(r'<!--seo-prev-next-start-->.*?<!--seo-prev-next-end-->', '', s, flags=re.S)
    s = re.sub(r'<!--umami-start-->.*?<!--umami-end-->', '', s, flags=re.S)
    s = re.sub(r'<head>.*?</head>', '', s, flags=re.S | re.I)
    r = Reader()
    r.feed(s)
    blocks = r.result()
    assert blocks, 'ничего не разобрано'
    assert blocks[0].startswith('# '), 'первым блоком должен быть заголовок H1, получено: %s' % blocks[0][:60]

    # Пустая строка разделяет блоки, но пункты одного списка и строки одной
    # таблицы должны идти подряд: пустая строка внутри них разорвёт их на
    # части при обратной сборке.
    def kind(b):
        if b.startswith('- ') or re.match(r'^\d+\.\s', b):
            return 'list'
        if b.startswith('|'):
            return 'table'
        if b.startswith('> '):
            return 'quote'
        return 'block'

    out = []
    for i, b in enumerate(blocks):
        if b == END_QUOTE:
            continue
        out.append(b)
        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
        if kind(b) == 'quote':
            # абзацы одной врезки разделяет строка '>', разные врезки - пустая
            if nxt is not None and nxt != END_QUOTE and kind(nxt) == 'quote':
                out.append('>')
                continue
            out.append('')
            continue
        if nxt is not None and kind(b) != 'block' and kind(b) == kind(nxt):
            continue
        out.append('')
    return '\n'.join(out).rstrip() + '\n'


def main():
    assert len(sys.argv) == 3, __doc__
    src, dst = sys.argv[1], sys.argv[2]
    assert os.path.isfile(src), src
    md = convert(src)
    # Путь назначения приходит из командной строки, то есть может указать
    # куда угодно, включая боевое дерево сайта. Через замок - как и все
    # остальные записи.
    guard.write(dst, md)
    print('OK  %s -> %s, %d строк, %d слов'
          % (os.path.basename(src), os.path.basename(dst),
             len(md.split('\n')), len(re.findall(r'[0-9A-Za-zЀ-ӿ]+', md))))


if __name__ == '__main__':
    try:
        main()
    except guard.LegacyWriteRefused as e:
        sys.exit(guard.die(e))
