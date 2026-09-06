# -*- coding: utf-8 -*-
u"""Посимвольная сверка цитат Декларации в документах корпуса.

Зачем. Документы 02 и 04 цитируют Декларацию дословно, в кавычках, и рядом
пересказывают её же своими словами. Пересказ править можно и нужно - слова
корпуса меняются вместе с Декларацией; цитату править нельзя ни на знак.
Разница между двумя правками на глаз не видна: обе выглядят как «поменяли
слово в абзаце». Здесь она видна.

Как считается. Из документов вынимаются все закавыченные куски, и каждый
ищется в Декларации ТОГО ЖЕ языка ПОДСТРОКОЙ, без нормализации: любая разница
в знаке, пробеле или окончании означает «не найдено».

Найденный кусок - доказанная цитата нашей Декларации. Ненайденный ничего
плохого не означает: документ 04 цитирует ещё Устав ООН, Всеобщую декларацию,
резолюции 1514 и 2625, декларацию о правах коренных народов, заключение Суда
по Косово и немецкий BGB, а документ 02 закавычивает и собственные обороты.
Отделить их по тексту блока нельзя: блок про чужую декларацию тоже называет
слово «декларация».

Поэтому проверка устроена не как «сколько расхождений», а как **снимок и
сверка с ним**: множество совпавших цитат не должно УМЕНЬШАТЬСЯ. Пропала
цитата из снимка - значит правка задела дословный текст, и это провал.

Кавычки у каждого языка свои, и это не мелочь: детектор, знающий только
ёлочки, не увидит немецких и китайских цитат вовсе и покажет ноль
расхождений на нуле данных. Поэтому пары заданы ЧИСЛОВЫМИ кодпойнтами, а
скрипт падает, если из документов языка не вынулось ни одной цитаты.

ЭТАЛОН лежит в репозитории: `_tools/quotes-baseline.json`. Без аргументов
скрипт сверяется именно с ним, поэтому проверка работает и в приёмке, и
руками, одной и той же командой.

**Когда цитата меняется законно** - вместе с самой Декларацией, - эталон
пересоздаётся `--save` В ТОМ ЖЕ КОММИТЕ, что и правка текста. Это условие, а
не пожелание: обновление эталона отдельным коммитом означает, что кто-то
сначала увидел красную приёмку, а потом сделал её зелёной, ничего не объяснив.
В одном коммите обновление видно в диффе и требует слов в сообщении.

Запуск:
    python _tools/check_quotes.py                    сверить с эталоном
    python _tools/check_quotes.py --list             показать сами цитаты
    python _tools/check_quotes.py --save FILE        пересоздать эталон
    python _tools/check_quotes.py --against FILE     сверить с другим снимком
"""
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
assert os.path.isdir(os.path.join(REPO, 'ru')), (
    u'не найден каталог мастеров: %s' % os.path.join(REPO, 'ru'))

LANGS = ['ru', 'en', 'de', 'es', 'fr', 'ka', 'zh', 'ar', 'hi']
DOCS = ['02', '04']

BASELINE = os.path.join(HERE, 'quotes-baseline.json')

# Пары кавычек по языкам. Заданы кодпойнтами, а не литералами: литерал в
# heredoc или в чужой кодировке портится молча, и проверка начинает мерить
# пустоту. Языки с одинаковыми кавычками перечислены поштучно намеренно -
# таблица должна читаться как утверждение о каждом языке, а не как умолчание.
QUOTES = {
    'ru': [(0x00AB, 0x00BB)],
    'es': [(0x00AB, 0x00BB)],
    'fr': [(0x00AB, 0x00BB)],
    'ka': [(0x00AB, 0x00BB)],
    'ar': [(0x00AB, 0x00BB)],
    'hi': [(0x00AB, 0x00BB)],
    # Немецкая нижняя открывающая и верхняя закрывающая.
    'de': [(0x201E, 0x201C)],
    # Китайские полноширинные; угловые скобки - на случай, если появятся.
    'zh': [(0x201C, 0x201D), (0x300C, 0x300D)],
    # Английский набран прямыми: открывающая и закрывающая - один знак,
    # поэтому куски берутся парами по порядку.
    'en': [(0x0022, 0x0022)],
}


def master(lang, doc):
    f = glob.glob(os.path.join(REPO, lang, '%s-*.md' % doc))
    assert len(f) == 1, u'мастер %s/%s: найдено файлов %d' % (lang, doc, len(f))
    s = io.open(f[0], encoding='utf-8').read()
    assert s.strip(), u'пустой мастер %s' % f[0]
    return s


def quoted(lang, text):
    u"""Закавыченные куски без самих кавычек."""
    out = []
    for op, cl in QUOTES[lang]:
        o, c = chr(op), chr(cl)
        if o == c:
            parts = text.split(o)
            # Куски с нечётным номером лежат между парой кавычек.
            out += [parts[i] for i in range(1, len(parts), 2)]
        else:
            out += re.findall(re.escape(o) + r'(.+?)' + re.escape(c), text, re.S)
    # Пустых и однобуквенных «цитат» не бывает: это разметка, а не речь.
    return [q.strip() for q in out if len(q.strip()) > 1]


def matched(lang):
    u"""Куски документов 02 и 04, найденные в Декларации этого языка."""
    decl = master(lang, '01')
    hit, seen_any = [], 0
    for doc in DOCS:
        qs = quoted(lang, master(lang, doc))
        seen_any += len(qs)
        for q in qs:
            if q in decl:
                hit.append('%s\t%s' % (doc, q))
    assert seen_any, (
        u'в документах %s языка %s не вынулось ни одной цитаты. Скорее всего '
        u'кавычки этого языка не те, что записаны в QUOTES, и проверка '
        u'показала бы ноль расхождений на нуле данных.'
        % ('/'.join(DOCS), lang))
    assert hit, (
        u'в документах %s языка %s не нашлось НИ ОДНОЙ цитаты Декларации, '
        u'хотя закавыченных мест %d. Так не бывает: сверять было бы нечего.'
        % ('/'.join(DOCS), lang, seen_any))
    return hit


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show = '--list' in sys.argv
    save = against = None
    for i, a in enumerate(sys.argv):
        if a == '--save' and i + 1 < len(sys.argv):
            save = sys.argv[i + 1]
        if a == '--against' and i + 1 < len(sys.argv):
            against = sys.argv[i + 1]
    langs = [a for a in args if a not in (save, against)] or LANGS
    for l in langs:
        assert l in LANGS, u'неизвестный язык %r' % l
    # Без аргументов сверяемся с эталоном репозитория. Просто посчитать -
    # это не проверка: число само по себе ничего не утверждает.
    if not save and not against:
        against = BASELINE
        if not os.path.isfile(against):
            print(u'ОТКАЗ: эталон не найден: %s' % against)
            print(u'Пересоздать: python _tools/check_quotes.py --save %s'
                  % against)
            print(u'Зелёная строка на отсутствующем эталоне была бы ложью.')
            return 2

    now = {}
    for l in langs:
        now[l] = matched(l)
        print(u'%-3s цитат Декларации, совпавших посимвольно: %d'
              % (l, len(now[l])))
        if show:
            for q in now[l]:
                doc, text = q.split('\t', 1)
                print(u'    %s  %s' % (doc, text[:100]))
    print(u'итого: %d' % sum(len(v) for v in now.values()))

    if save:
        # newline задан явно: без него Windows пишет CRLF, git нормализует в
        # LF, и файл в рабочей копии остаётся «изменённым» после каждой съёмки.
        io.open(save, 'w', encoding='utf-8', newline='\n').write(
            json.dumps(now, ensure_ascii=False, indent=1) + '\n')
        print(u'снимок записан: %s' % save)
        return 0

    if against:
        assert os.path.isfile(against), u'нет снимка %s' % against
        was = json.loads(io.open(against, encoding='utf-8').read())
        assert was, u'снимок пуст - сверять не с чем'
        lost = 0
        for l in sorted(was):
            gone = [q for q in was[l] if q not in now.get(l, [])]
            add = [q for q in now.get(l, []) if q not in was[l]]
            for q in gone:
                doc, text = q.split('\t', 1)
                print(u'ПРОПАЛА  %s %s  %s' % (l, doc, text[:100]))
            for q in add:
                doc, text = q.split('\t', 1)
                print(u'новая    %s %s  %s' % (l, doc, text[:100]))
            lost += len(gone)
        print(u'сверка со снимком: пропало цитат %d' % lost)
        return 1 if lost else 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
