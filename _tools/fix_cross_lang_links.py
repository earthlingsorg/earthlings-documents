# -*- coding: utf-8 -*-
u"""Перекрёстные ссылки внутри мастера ведут на страницы СВОЕГО языка.

Зачем. Читатель на хинди жмёт «Устав» и попадает на русский текст. Найдено
2026-09-01: 45 таких ссылок в трёх мастерах хинди - последнего закрытого
языка, где локализация адресов не доехала. Ни в одном из остальных восьми
языков такого нет.

Почему скриптом, а не руками. Соответствие «номер документа - слаг» уже
задано в `SLUGS` сборщика. Переписать его сюда значит завести вторую копию,
которая разойдётся при первом переименовании. Здесь она читается из живого
источника, а руками правится только проза - механику делает скрипт.

Замена узкая: меняется РОВНО адрес внутри ссылки, к тексту не прикасаемся.
Номер документа берётся из старого адреса, новый собирается из слага того
языка, чей это мастер.

Запуск:

    python _tools/fix_cross_lang_links.py            показать, что нашлось
    python _tools/fix_cross_lang_links.py --apply    записать

Код возврата - число оставшихся чужих ссылок (0, если чисто).
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from build_site_docs import SLUGS, ORIGIN            # noqa: E402

LANGS = sorted(SLUGS)

# Адрес страницы корпуса: и абсолютный, и корневой. Ссылки в мастерах сейчас
# абсолютные, но корневые появятся, если однажды решим их сократить, - и тогда
# проверка не должна замолчать.
LINK = re.compile(
    r'(?P<pre>(?:' + re.escape(ORIGIN) + r')?)/documents/'
    r'(?P<lang>[a-z]{2})/(?P=lang)(?P<num>[0-9]{2})'
    r'(?P<slug>-[a-z0-9-]+)?\.html')


def target(lang, num):
    u"""Адрес документа `num` на языке `lang`, или None, если его там нет."""
    slug = SLUGS.get(lang, {}).get(num)
    if not slug:
        return None
    return '/documents/%s/%s%s-%s.html' % (lang, lang, num, slug)


def scan(apply=False):
    found = []
    unmapped = []
    changed_files = 0
    for lang in LANGS:
        d = os.path.join(REPO, lang)
        if not os.path.isdir(d):
            continue
        for path in sorted(glob.glob(os.path.join(d, '[0-9][0-9]-*.md'))):
            s = io.open(path, encoding='utf-8').read()
            assert s.strip(), path
            out = s
            hits = 0
            for m in list(LINK.finditer(s)):
                if m.group('lang') == lang:
                    continue
                num = m.group('num')
                want = target(lang, num)
                if not want:
                    unmapped.append(u'%s/%s -> документа %s нет в SLUGS[%s]'
                                    % (lang, os.path.basename(path), num, lang))
                    continue
                found.append(u'%s/%s: %s%s -> %s'
                             % (lang, os.path.basename(path),
                                m.group('lang'), num, want))
                out = out.replace(m.group(0), m.group('pre') + want)
                hits += 1
            if hits and apply:
                io.open(path, 'w', encoding='utf-8',
                        newline='\n').write(out)
                changed_files += 1
    return found, unmapped, changed_files


def main():
    apply = '--apply' in sys.argv
    found, unmapped, changed = scan(apply)

    if not LANGS:
        print(u'ОТКАЗ: SLUGS пуст - проверять нечего, и это не «чисто».')
        return 1

    for f in found:
        print(u'  ' + f)
    for u in unmapped:
        print(u'  НЕ СОПОСТАВЛЕНО: ' + u)

    print(u'')
    print(u'чужих ссылок: %d, файлов затронуто: %s'
          % (len(found), changed if apply else u'(сухой прогон)'))
    if unmapped:
        print(u'не сопоставлено: %d - эти НЕ тронуты' % len(unmapped))
    if found and not apply:
        print(u'записать: python _tools/fix_cross_lang_links.py --apply')
    return len(unmapped) if apply else len(found)


if __name__ == '__main__':
    sys.exit(main())
