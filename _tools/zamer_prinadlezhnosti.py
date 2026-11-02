# -*- coding: utf-8 -*-
u"""Замер слова "членство" на тематических страницах сайта.

Зачем этот файл лежит в репозитории, а не в черновиках сессии. Прибор замера
живёт там же, где то, что он мерит: скрипт, оставленный в папке сессии,
исчезает вместе с сессией, и следующий заход мерит заново другим прибором и
получает другое число. Ровно так число "80" прожило два месяца, пока живой
замер 2026-11-02 не дал 236.

Что считается. Вся семья слов по каждому языку, а не одно отвлечённое
существительное: "член" о человеке ловится так же, как "членство" о
принадлежности. Длинный корень съедает короткий - после находки на её место
подставляется пробел, иначе "членств" посчитается дважды.

Регистр считается в Python с re.IGNORECASE | re.UNICODE: `grep -i` в Git Bash
на этой машине НЕ складывает регистры кириллицы, и три прежних замера дали 14
вместо 20.

Запуск:
    python _tools/zamer_prinadlezhnosti.py            замер, код возврата 0
    python _tools/zamer_prinadlezhnosti.py --check    проверка, найдено - код 1
    python _tools/zamer_prinadlezhnosti.py --files    ещё и разбивка по файлам

Проверка (--check) падает на любой находке вне списка законных из
LEGITIMATE. Умолчание - запрет: новое законное вхождение заводится в список
руками, с причиной.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
# Репозиторий сайта - соседняя папка рядом с этим репозиторием, как у
# build_site_docs.py. Переопределяется EARTHLINGS_SITE, если они лежат врозь.
# Захардкоженный путь одной машины в публичном репозитории делает скрипт
# неработающим у всех, кроме одного человека.
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')

# Рабочая директория Bash сохраняется между вызовами, и после cd
# относительные пути ломаются. Поэтому дом проверяется сразу.
assert os.path.isdir(SITE), (
    u'не найден репозиторий сайта: %s\n'
    u'Ожидается earth-lings-site рядом с этим репозиторием. Если он лежит в '
    u'другом месте - EARTHLINGS_SITE=/путь/к/earth-lings-site' % SITE)

TREES = [
    ('topics', os.path.join(SITE, 'topics')),
    ('_v2/topics', os.path.join(SITE, '_v2', 'topics')),
]
for _name, _path in TREES:
    assert os.path.isdir(_path), u'нет дерева %s: %s' % (_name, _path)

LANGS = ['ru', 'en', 'es', 'de', 'fr', 'zh', 'ar', 'hi', 'ka']

# Семья слов по языкам. Длинная форма стоит перед короткой: порядок
# значащий, по нему работает правило "длинный корень съедает короткий".
FAMILY = {
    'en': [u'membership', u'member'],
    'ru': [u'членств', u'член'],
    'de': [u'Mitgliedschaft', u'Mitglied'],
    'es': [u'membresía', u'afiliación', u'miembro'],
    'fr': [u'adhésion', u'adhérent', u'membre'],
    'hi': [u'सदस्यता', u'सदस्य'],
    'ka': [u'წევრობ', u'წევრ'],
    # 🚨 Арабское ЛОМАНОЕ множественное أعضاء подстроки عضو НЕ содержит, и
    # семья его не ловила вовсе: проверено 2026-11-02, re.findall даёт ноль.
    # Три таких места на страницах нашлись глазами, а не прибором, и ровно
    # их не хватало арабскому до дельты остальных языков - то есть разрыв в
    # счёте был слепотой прибора, а не особенностью перевода. Урок общий:
    # приставки, инфиксы и ломаные формы ломают счёт по основе МОЛЧА.
    'ar': [u'عضوية', u'أعضاء', u'عضو'],
    'zh': [u'会员', u'成员'],
}

assert FAMILY, u'пустой словарь семьи слов'
assert sorted(FAMILY) == sorted(LANGS), u'словарь семьи слов не по девяти языкам'
for _l, _w in FAMILY.items():
    assert _w, u'пустая семья слов: %s' % _l

# Законные вхождения: государства-члены, членство в международных
# организациях, члены Совета и Core Nodes, цитаты и заголовки, где слово
# несёт само различение. Ключ - "дерево|язык|файл", значение - сколько
# законных вхождений в нём ожидается и почему.
#
# Разбор 2026-11-02: признака законности из первого списка (государства-члены,
# международные организации, UNDRIP, Core Nodes) на тематических страницах не
# нашлось ни одного. Законными признаны четыре места: два заголовка, где слово
# стоит в ОТРИЦАЕМОЙ половине и несёт само различение (убрать его - значит
# убрать мысль), и два, где семья слов перехватывает чужое значение -
# французское «присоединение» и грузинское о ЧУЖИХ народах.
# Нашлось новое - заводить сюда руками, с причиной.
LEGITIMATE = {
    # "A people is a subject, not a member"
    '_v2/topics|en|a-people-without-territory': 1,
    # "Народ - субъект, а не член"
    '_v2/topics|ru|a-people-without-territory': 1,
    # Французское adhésion здесь переводит не «членство», а «присоединение»:
    # русский мастер говорит «учреждённый осознанным присоединением», en -
    # conscious accession, de - Beitritt, es - adhesión. Канон слово о самом
    # ДЕЙСТВИИ разрешает прямо: «взнос при вступлении». Семья слов
    # перехватывает adhésion потому, что французское слово несёт оба смысла.
    '_v2/topics|fr|new-subject-of-international-law': 1,
    # Грузинское წევრები здесь о ЧУЖИХ народах - апатридах и непризнанных,
    # «члены тех народов, которых не признаёт ни одна карта», - а замок
    # 2026-08-20 о принадлежности к народу Earthlings. Подстановка მონაწილე
    # дала бы «участники тех народов» и сменила бы смысл.
    '_v2/topics|ka|self-determination-without-territory': 1,
}

# Замороженное дерево: копия для отката после подмены 2026-09-06. Править и
# коммитить в него нельзя, pre-commit откажет. Поэтому его вхождения МЕРЯЮТСЯ,
# но проверку не роняют: иначе --check не может пройти никогда, и проверка,
# которая обязана падать, перестаёт что-либо значить.
FROZEN_TREE = 'topics'


def words_of(lang):
    return FAMILY.get(lang, [])


def count_text(text, lang):
    u"""Сколько слов семьи в тексте. Длинный корень съедает короткий."""
    out = {}
    s = text
    for w in words_of(lang):
        rx = re.compile(re.escape(w), re.IGNORECASE | re.UNICODE)
        hits = list(rx.finditer(s))
        if hits:
            out[w] = len(hits)
            # На место совпадения - пробелы той же длины: так короткий
            # корень не найдёт себя внутри уже посчитанного длинного.
            s = rx.sub(lambda m: u' ' * len(m.group(0)), s)
    return out


def lang_of(path):
    u"""Язык страницы по имени файла.

    🚨 Английский хаб зовётся index.html, а не en.html. Прибор, который
    смотрит только на <язык>.html, английский хаб НЕ ВИДИТ - и замер
    2026-11-02, давший по хабам "1 вхождение, только ru", пропустил два
    английских. Проверено: /c/local_git_vps/earth-lings-site/_v2/topics/
    index.html держит и member, и membership.
    """
    base = os.path.basename(path)
    code = os.path.splitext(base)[0]
    if code == 'index':
        return 'en'
    return code if code in LANGS else None


def pages_of(root):
    u"""Страницы дерева: темы <тема>/<язык>.html и хабы <язык>.html."""
    out = []
    for name in sorted(os.listdir(root)):
        full = os.path.join(root, name)
        if os.path.isdir(full):
            for f in sorted(os.listdir(full)):
                p = os.path.join(full, f)
                if os.path.isfile(p) and lang_of(p):
                    out.append((name, p))
        elif os.path.isfile(full) and lang_of(full):
            out.append((None, full))
    return out


def scan():
    u"""Замер обоих деревьев. Возвращает список находок по файлам."""
    rows = []
    for tree, root in TREES:
        pages = pages_of(root)
        assert pages, u'пустой ввод: в дереве %s нет страниц' % tree
        for topic, path in pages:
            lang = lang_of(path)
            text = io.open(path, encoding='utf-8').read()
            assert text.strip(), u'пустой ввод: %s' % path
            found = count_text(text, lang)
            total = sum(found.values())
            if total:
                rows.append({'tree': tree, 'topic': topic, 'lang': lang,
                             'path': path, 'words': found, 'total': total})
    return rows


def selftest():
    u"""Отрицательный контроль. Прибор обязан поймать подсунутое слово в
    обоих регистрах и НЕ поймать слово-замену."""
    chlen = u'член'                      # член
    chlenstvo = u'членство'
    prinadl = u'принадлежность'

    got = count_text(u'%s %s' % (chlen, chlen.upper()), 'ru')
    assert got.get(chlen[:4]) == 2, u'регистр кириллицы не сложился: %r' % got

    got = count_text(chlenstvo, 'ru')
    assert got == {chlenstvo[:7]: 1}, u'длинный корень не съел короткий: %r' % got

    got = count_text(prinadl, 'ru')
    assert got == {}, u'замена поймана как дефект: %r' % got

    got = count_text(u'Member MEMBERSHIP', 'en')
    assert got == {u'membership': 1, u'member': 1}, u'английский: %r' % got

    got = count_text(u'belonging earthling participant', 'en')
    assert got == {}, u'английская замена поймана как дефект: %r' % got

    # Прибор не считает языка, которого не знает.
    assert count_text(chlen, 'zz') == {}


def main(argv):
    selftest()
    check = '--check' in argv
    by_files = '--files' in argv

    rows = scan()
    by_tree_lang = {}
    for r in rows:
        by_tree_lang.setdefault((r['tree'], r['lang']), 0)
        by_tree_lang[(r['tree'], r['lang'])] += r['total']

    out = sys.stdout
    for tree, _root in TREES:
        total = sum(v for (t, _l), v in by_tree_lang.items() if t == tree)
        files = len([r for r in rows if r['tree'] == tree])
        out.write(u'%s: %d вхождений в %d файлах\n' % (tree, total, files))
        for lang in LANGS:
            n = by_tree_lang.get((tree, lang), 0)
            if n:
                out.write(u'    %s %d\n' % (lang, n))
        out.write(u'\n')

    if by_files:
        for r in rows:
            out.write(u'%s  %s/%s  %d  %s\n' % (
                r['tree'], r['topic'] or u'(хаб)', r['lang'], r['total'],
                u', '.join(u'%s=%d' % (k, v) for k, v in sorted(r['words'].items()))))
        out.write(u'\n')

    grand = sum(by_tree_lang.values())
    out.write(u'ВСЕГО по двум деревьям: %d\n' % grand)

    if not check:
        return 0

    # Проверка: найдено вне списка законных - падаем. Умолчание - запрет.
    bad = []
    frozen = 0
    for r in rows:
        if r['tree'] == FROZEN_TREE:
            frozen += r['total']
            continue
        key = u'%s|%s|%s' % (r['tree'], r['lang'], r['topic'] or u'hub')
        allowed = LEGITIMATE.get(key, 0)
        if r['total'] > allowed:
            bad.append((key, r['total'], allowed, r['path']))
    if frozen:
        out.write(u'\nЗамороженное дерево %s: %d вхождений, проверку не роняют '
                  u'(править его нельзя).\n' % (FROZEN_TREE, frozen))
    if bad:
        out.write(u'\nПРОВЕРКА НЕ ПРОШЛА: %d файлов со словом о принадлежности\n'
                  % len(bad))
        for key, got, allowed, path in bad:
            out.write(u'    %s: найдено %d, законных %d - %s\n'
                      % (key, got, allowed, path))
        return 1
    out.write(u'\nПРОВЕРКА ПРОШЛА: вне списка законных вхождений нет\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
