# -*- coding: utf-8 -*-
u"""Собирает листы @font-face для письменностей в _v2/css/fonts-<язык>.css.

Зачем. Шрифтовая лесенка черновика (`_v2/css/tokens.css`, переменные `--sans`,
`--serif`, `--sans-nav`) перечисляет Noto для арабицы, деванагари, иероглифов и
мхедрули - а ни одного `@font-face`, который бы их объявил, в `_v2` нет. Имя в
лесенке само по себе ничего не даёт: оно означает «возьми шрифт с таким именем
у читателя». У кого он стоит - тот видит текст чужим шрифтом, у кого нет -
квадраты. Четыре языка из девяти держались на удаче.

Откуда берутся объявления. Из боевых `css/fonts-ar.css`, `-hi.css`, `-ka.css`,
`-zh.css`. Боевое дерево только ЧИТАЕТСЯ - замок этапа 0 запрещает писать в
него, а не смотреть. Сами файлы шрифтов не копируются: в дне подмены `/fonts/`
откатывается в общее дерево (блок `@shared` в vhost), и они остаются на месте.

Почему не копия файла целиком. В боевых листах живут ещё Amiri, Tiro Devanagari
Hindi и подмена имени `Inter` - шрифты прежней темы. В лесенке черновика их нет,
и объявлять их значило бы возить по сети то, что никогда не будет выбрано.
Отбор идёт по именам, вычитанным из `tokens.css`, а не по списку в этом файле:
список разошёлся бы с лесенкой молча, и разошёлся бы именно тогда, когда её
поправят.

Запуск:  python _tools/make_script_fonts.py
Выход:   <репозиторий сайта>/_v2/css/fonts-<язык>.css
"""

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_site_docs import SITE                               # noqa: E402

V2 = os.path.join(SITE, '_v2')
assert os.path.isdir(V2), u'нет черновика %s' % V2

# Семейства, объявленные в самом tokens.css: они уже есть в черновике своими
# файлами, и переобъявлять их из боевого листа нельзя - получили бы два разных
# набора начертаний под одним именем.
OWN = ('Montserrat', 'Cormorant')

# Язык -> боевой лист. Один лист может обслуживать один язык: письменность у
# каждого своя. Языка нет в таблице - у него латиница или кириллица, и Noto ему
# не нужен.
SRC_BY_LANG = {'ar': 'fonts-ar.css', 'hi': 'fonts-hi.css',
               'ka': 'fonts-ka.css', 'zh': 'fonts-zh.css'}


def wanted_families():
    u"""Имена семейств из лесенки черновика, кроме своих."""
    p = os.path.join(V2, 'css', 'tokens.css')
    css = io.open(p, encoding='utf-8').read()
    assert css.strip(), u'пустой tokens.css'
    names = set()
    for var in ('--sans', '--serif', '--sans-nav'):
        m = re.search(re.escape(var) + r'\s*:(.*?);', css, re.S)
        assert m, u'в tokens.css не нашлась переменная %s' % var
        names |= set(re.findall(r"'([^']+)'", m.group(1)))
    names -= set(OWN)
    assert names, u'в лесенке не осталось ни одного семейства - отбор пуст'
    return names


def blocks_of(path):
    u"""@font-face из листа, по одному на элемент, вместе с именем семейства."""
    css = io.open(path, encoding='utf-8').read()
    assert css.strip(), u'пустой лист %s' % path
    out = []
    for b in re.findall(r'@font-face\s*\{[^}]*\}', css):
        m = re.search(r"font-family:\s*'([^']+)'", b)
        assert m, u'в %s есть @font-face без имени семейства' % path
        out.append((m.group(1), b))
    assert out, u'в %s ни одного @font-face' % path
    return out


def main():
    want = wanted_families()
    written = 0
    for lang, name in sorted(SRC_BY_LANG.items()):
        src = os.path.join(SITE, 'css', name)
        assert os.path.isfile(src), (
            u'нет боевого листа %s - без него письменность языка %s осталась '
            u'бы без шрифта' % (src, lang))

        keep, seen, dropped = [], set(), set()
        for fam, block in blocks_of(src):
            if fam in want:
                keep.append(block)
                seen.add(fam)
            else:
                dropped.add(fam)

        assert keep, (
            u'из %s не отобрано ни одного объявления. Имена в лесенке '
            u'tokens.css и в боевом листе разошлись: в лесенке %s, в листе %s'
            % (name, sorted(want), sorted(dropped)))

        # Каждый файл шрифта обязан существовать. Ссылка на отсутствующий
        # woff2 не роняет страницу - она молча отдаёт 404 и подставляет
        # системный шрифт, то есть ровно ту беду, ради которой всё это.
        missing = []
        for block in keep:
            for url in re.findall(r'url\(([^)]+)\)', block):
                url = url.strip('\'"')
                if not url.startswith('/fonts/'):
                    missing.append(url + u' (не из /fonts/)')
                elif not os.path.isfile(os.path.join(SITE, url.lstrip('/'))):
                    missing.append(url)
        assert not missing, (
            u'нет файлов шрифтов для %s: %s' % (lang, ', '.join(missing[:5])))

        head = (u'/* Письменность языка %s. Собран make_script_fonts.py из\n'
                u'   боевого css/%s: оставлены только семейства, названные в\n'
                u'   лесенке _v2/css/tokens.css - %s.\n'
                u'   Руками не править: правка переживёт до следующей сборки.\n'
                u'   Отброшено как шрифты прежней темы: %s. */\n'
                % (lang, name, ', '.join(sorted(seen)),
                   ', '.join(sorted(dropped)) or u'ничего'))

        out = os.path.join(V2, 'css', 'fonts-%s.css' % lang)
        io.open(out, 'w', encoding='utf-8', newline='\n').write(
            head + u''.join(keep) + u'\n')
        written += 1
        sys.stdout.write(
            'fonts-%s.css  объявлений %d, семейств %d (%s), %d КБ\n'
            % (lang, len(keep), len(seen), ', '.join(sorted(seen)),
               os.path.getsize(out) // 1024))

    assert written == len(SRC_BY_LANG)
    sys.stdout.write('листов написано: %d\n' % written)


if __name__ == '__main__':
    main()
