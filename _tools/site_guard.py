# -*- coding: utf-8 -*-
u"""Замок на запись в боевое дерево сайта.

Решение Артура 2026-08-25: боевой сайт заменяется новым и больше не правится
ничем - ни руками, ни пересборкой. Пересборка это тоже правка.

Замок на это уже стоял, но на входе ОДНОГО скрипта: `build_site_docs.py`
отказывается запускаться с `--theme legacy`. Разбор 2026-09-01 показал, чего
такой замок не ловит.

  1. `build_site_docs.py --fix-hreflang` выполняется РАНЬШЕ отказа и пишет в
     `<site>/documents/<язык>/`. Сухой прогон: 308 живых страниц. Ни флага,
     ни предупреждения.
  2. `build_mainpage.py` пишет `<site>/mainpage/<язык>/index.html` и про
     замок не знает вовсе.
  3. `md2doc.py` берёт путь назначения из командной строки и пишет куда
     скажут.
  4. Страница `ka02-civic-voice.html` легла в боевое дерево 25 августа в
     08:09 - за час до того, как замок появился.

Отсюда правило этого файла: **замок стоит на записи, а не на входе.** Скрипту
не надо помнить про флаг; он физически не может записать в боевое дерево, не
сказав об этом вслух.

Что разрешено:
  - что угодно вне дерева сайта (свой репозиторий, отчёты, временные файлы);
  - что угодно внутри `<site>/_v2/` - это и есть новый сайт;
  - боевое дерево ТОЛЬКО при ALLOW_LEGACY_BUILD=1. Единственный законный
    случай - день подмены.

Переменная названа так же, как у прежнего замка, намеренно: два замка на одно
решение должны отпираться одним ключом, иначе в день подмены выяснится, что
ключей два и второй забыли.
"""
import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
V2 = os.path.join(SITE, '_v2')

ALLOW = 'ALLOW_LEGACY_BUILD'


class LegacyWriteRefused(Exception):
    u"""Попытка записи в боевое дерево без явного разрешения."""


def _norm(path):
    return os.path.normcase(os.path.abspath(path))


def is_inside(path, root):
    u"""path лежит внутри root.

    Через `os.path.relpath`, а не сравнением строк: `<site>/_v2suffix` начинается
    с `<site>/_v2`, но внутри него не лежит, и проверка на префикс пустила бы
    его как свой.
    """
    p, r = _norm(path), _norm(root)
    if p == r:
        return True
    rel = os.path.relpath(p, r)
    return not rel.startswith(os.pardir + os.sep) and rel != os.pardir


def allowed():
    return os.environ.get(ALLOW) == '1'


def verdict(path):
    u"""Куда ведёт путь: 'вне сайта', 'v2' или 'боевое'."""
    if not is_inside(path, SITE):
        return 'outside'
    if is_inside(path, V2):
        return 'v2'
    return 'legacy'


def check(path, what=u'запись'):
    u"""Разрешена ли запись. Отказ - исключение, а не тихий пропуск.

    Возвращает путь, чтобы вызов можно было ставить в выражение.
    """
    if verdict(path) != 'legacy' or allowed():
        return path
    raise LegacyWriteRefused(
        u'ОТКАЗ: %s в боевое дерево сайта.\n\n'
        u'  Путь:  %s\n\n'
        u'  Боевой сайт заменяется новым и больше не правится - ни руками,\n'
        u'  ни пересборкой. Пишите в _v2 (для сборщика корпуса это\n'
        u'  --theme v2).\n\n'
        u'  Если это день подмены: %s=1 перед командой.\n'
        % (what, os.path.abspath(path), ALLOW))


def write(path, text, dry=False, newline='\n'):
    u"""Единственный разрешённый способ записать файл дерева сайта."""
    check(path)
    if dry:
        return False
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        check(d, u'создание каталога')
        os.makedirs(d)
    io.open(path, 'w', encoding='utf-8', newline=newline).write(text)
    return True


def write_bytes(path, data, dry=False):
    check(path)
    if dry:
        return False
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        check(d, u'создание каталога')
        os.makedirs(d)
    io.open(path, 'wb').write(data)
    return True


def makedirs(path):
    check(path, u'создание каталога')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def die(exc):
    u"""Напечатать отказ и вернуть код возврата для main()."""
    sys.stderr.write(u'%s\n' % exc)
    return 2


def selftest():
    u"""Замок обязан отпираться и запираться. Гоняется из приёмки.

    Проверка на пустом входе не «проходит»: если бы SITE указывал в никуда,
    все пути стали бы 'outside' и замок молча разрешил бы всё.
    """
    problems = []
    if not os.path.isdir(SITE):
        return [u'дерева сайта нет: %s - замку нечего охранять' % SITE]

    prod = os.path.join(SITE, 'documents', 'ru', 'ru01-deklaraciya.html')
    draft = os.path.join(V2, 'documents', 'ru', 'ru01-deklaraciya.html')
    outside = os.path.join(REPO, '_tools', 'report.txt')

    if verdict(prod) != 'legacy':
        problems.append(u'боевой путь не опознан как боевой: %s' % prod)
    if verdict(draft) != 'v2':
        problems.append(u'путь черновика не опознан как черновик: %s' % draft)
    if verdict(outside) != 'outside':
        problems.append(u'путь вне сайта опознан неверно: %s' % outside)

    # Ловушка на сравнение строк вместо разбора пути.
    if verdict(V2 + 'x') != 'legacy':
        problems.append(u'путь-двойник %s принят за черновик' % (V2 + 'x'))

    was = os.environ.get(ALLOW)
    try:
        os.environ.pop(ALLOW, None)
        try:
            check(prod)
            problems.append(u'замок НЕ ЗАПЕРТ: боевая запись прошла без %s' % ALLOW)
        except LegacyWriteRefused:
            pass
        check(draft)                       # черновик обязан проходить всегда
        os.environ[ALLOW] = '1'
        check(prod)                        # ключ обязан отпирать
    except LegacyWriteRefused:
        problems.append(u'замок НЕ ОТПИРАЕТСЯ: %s=1 не пустил боевую запись'
                        % ALLOW)
    finally:
        os.environ.pop(ALLOW, None)
        if was is not None:
            os.environ[ALLOW] = was
    return problems


if __name__ == '__main__':
    bad = selftest()
    for b in bad:
        print(b)
    print(u'замок: %s' % (u'провалов %d' % len(bad) if bad else u'исправен'))
    sys.exit(len(bad))
