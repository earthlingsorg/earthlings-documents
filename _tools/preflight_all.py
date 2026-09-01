# -*- coding: utf-8 -*-
u"""Одна команда приёмки: прогоняет все проверки корпуса и сайта.

Зачем. Проверок семь, живут они в двух репозиториях, вызываются руками и
поодиночке. Из-за этого одна из них - `verify_md_html.py` - молча не работала
десять дней: она падала на импорте, а вызывать её было неоткуда, и заметить
поломку нечем. Проверка, которую надо вспомнить, чтобы запустить, рано или
поздно не запускается.

Здесь они собраны в одну таблицу «проверка - результат». Запуск:

    python _tools/preflight_all.py            все проверки
    python _tools/preflight_all.py --fast     без аудита девяти языков

Код возврата 0, если провалов нет. Ненулевой - число проваленных проверок.

Правило одно и оно жёсткое: **проверка, которая не смогла запуститься,
считается ПРОВАЛЕННОЙ, а не пропущенной.** Ровно на этом различении и был
потерян десяток дней.
"""
import io
import os
import re
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')

LANGS = ['ar', 'de', 'en', 'es', 'fr', 'hi', 'ka', 'ru', 'zh']


class Row(object):
    def __init__(self, name, ok, note):
        self.name, self.ok, self.note = name, ok, note


def run(args, cwd=None):
    u"""Запускает проверку и возвращает (код, вывод). Не упавший процесс с
    ненулевым кодом - это провал проверки; не запустившийся - тоже."""
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    try:
        p = subprocess.run([sys.executable] + args, cwd=cwd or REPO,
                           capture_output=True, env=env, timeout=1800)
    except Exception as e:                       # noqa: BLE001
        return 99, u'не запустилась: %s' % e
    out = (p.stdout or b'').decode('utf-8', 'replace')
    err = (p.stderr or b'').decode('utf-8', 'replace')
    return p.returncode, (out + err)


def tail(text, n=1):
    lines = [x for x in text.split('\n') if x.strip()]
    return ' | '.join(lines[-n:])[:110] if lines else u'(пусто)'


def check_verify():
    code, out = run([os.path.join('_tools', 'verify_md_html.py'), 'all', 'all'])
    m = re.search(r'итого: (\d+) из (\d+)', out)
    if code == 99 or not m:
        return Row(u'мастер против страницы', False, tail(out))
    bad, total = int(m.group(1)), int(m.group(2))
    return Row(u'мастер против страницы', code == 0 and bad == 0,
               u'проверено %d, расхождений %d' % (total, bad))


def check_nav():
    code, out = run([os.path.join('_tools', 'check_nav_sync.py')])
    return Row(u'меню: constants.js против chrome.py', code == 0, tail(out))


def check_audit(fast):
    if fast:
        return Row(u'машинная вычитка девяти языков', True, u'пропущено по --fast')
    code, out = run([os.path.join('_tools', 'audit_lang.py'), '--all'])
    if code == 99:
        return Row(u'машинная вычитка девяти языков', False, tail(out))
    # Отчёты пишутся в файлы; смотрим на жёсткие замки в каждом.
    hard = []
    for lang in LANGS:
        p = os.path.join(TOOLS, 'audit-report-%s.txt' % lang)
        if not os.path.isfile(p):
            hard.append(u'%s: отчёта нет' % lang)
            continue
        s = io.open(p, encoding='utf-8').read()
        n = len(re.findall(r'^  ДЕФЕКТ ', s, re.M))
        if n:
            hard.append(u'%s: %d' % (lang, n))
    return Row(u'машинная вычитка девяти языков', not hard,
               u'жёстких замков сработало: %s'
               % (', '.join(hard) if hard else u'ни одного'))


def check_layout():
    u"""Одинаковое число строк у девяти языков в каждом документе.

    Сверка мастер-против-страницы этого не видит: она сравнивает слова. А
    расхождение разметки означает, что где-то у одного языка появился или
    пропал блок, - и найдено оно бывает только так.
    """
    import glob
    ru = {}
    for p in sorted(glob.glob(os.path.join(REPO, 'ru', '[0-9][0-9]-*.md'))):
        ru[os.path.basename(p)[:2]] = len(
            io.open(p, encoding='utf-8').read().split('\n'))
    if not ru:
        return Row(u'разметка совпадает у девяти языков', False,
                   u'русских мастеров не найдено')
    bad = []
    for lang in LANGS:
        if lang == 'ru':
            continue
        for p in sorted(glob.glob(os.path.join(REPO, lang, '[0-9][0-9]-*.md'))):
            num = os.path.basename(p)[:2]
            if num not in ru:
                continue
            n = len(io.open(p, encoding='utf-8').read().split('\n'))
            if n != ru[num]:
                bad.append(u'%s%s %d/%d' % (lang, num, ru[num], n))
    return Row(u'разметка совпадает у девяти языков', not bad,
               u'документов у ru %d, расхождений %d%s'
               % (len(ru), len(bad),
                  (': ' + ', '.join(bad[:4])) if bad else ''))


def check_sitemap():
    p = os.path.join(SITE, '_v2', 'sitemap.xml')
    if not os.path.isfile(p):
        return Row(u'сайтмап черновика', False, u'файла нет - сборка не запускалась')
    s = io.open(p, encoding='utf-8').read()
    numeric = re.findall(
        r'<loc>[^<]*/documents/[a-z]{2}/[a-z]{2}[0-9]{2}\.html</loc>', s)
    total = s.count('<loc>')
    return Row(u'сайтмап черновика', not numeric and total > 200,
               u'адресов %d, числовых адресов документов %d'
               % (total, len(numeric)))


def check_site(script, name):
    p = os.path.join(SITE, '_v2', 'tools', script)
    if not os.path.isfile(p):
        return Row(name, False, u'скрипта нет: %s' % p)
    code, out = run([p], cwd=SITE)
    return Row(name, code == 0, tail(out))


def check_prod_untouched():
    u"""Боевое дерево не тронуто: в рабочей копии сайта нет изменённых файлов
    вне _v2/ и разрешённого списка. Замок этапа 0 ловит это на коммите, здесь -
    до него."""
    try:
        p = subprocess.run(['git', 'status', '--porcelain'], cwd=SITE,
                           capture_output=True, timeout=120)
    except Exception as e:                       # noqa: BLE001
        return Row(u'боевое дерево не тронуто', False, u'git не запустился: %s' % e)
    allowed = re.compile(
        r'^(_v2/|\.githooks/|\.gitignore$|package(-lock)?\.json$|'
        r'README\.md$|CLAUDE\.md$|build\.sh$|sw\.js$)')
    bad = []
    stray = []
    for line in (p.stdout or b'').decode('utf-8', 'replace').split('\n'):
        if not line.strip():
            continue
        path = line[3:].strip().strip('"')
        if line[:2] == '??':
            # Раньше здесь стоял `continue` с доводом «неотслеживаемое не
            # коммитится». Довод неверен: `git add -A` делает его
            # отслеживаемым одним движением, и ровно так в боевое дерево
            # попала ka02-civic-voice.html - выход сборки, запущенной без
            # --theme v2. Файл пролежал там неделю, невидимый для этой
            # проверки, которая всё это время говорила «не тронуто».
            if not allowed.match(path):
                stray.append(path)
            continue
        if not allowed.match(path):
            bad.append(path)
    note = u'изменённых файлов вне _v2: %d' % len(bad)
    if bad:
        note += u' (' + u', '.join(bad[:3]) + u')'
    if stray:
        note += u'; НЕОТСЛЕЖИВАЕМЫХ: %d (%s)' % (len(stray),
                                                 u', '.join(stray[:3]))
    return Row(u'боевое дерево не тронуто', not bad and not stray, note)


def check_guard():
    u"""Замок на запись в боевое дерево исправен.

    Сам замок стоит в site_guard.py и вызывается из каждого места записи.
    Здесь проверяется, что он и запирается, и отпирается: ослабленный замок
    выглядит точно как исправный, пока в него не постучат.
    """
    if TOOLS not in sys.path:
        sys.path.insert(0, TOOLS)
    try:
        import site_guard
        bad = site_guard.selftest()
    except Exception as e:                       # noqa: BLE001
        return Row(u'замок на боевое дерево', False,
                   u'не запустился: %s: %s' % (type(e).__name__, e))
    return Row(u'замок на боевое дерево', not bad,
               u'исправен' if not bad else u'; '.join(bad)[:110])


def check_launch():
    u"""Готовность к подмене - девятнадцать проверок из `preflight_launch.py`.

    Отдельным файлом, потому что вопросы разные: здесь корпус, там - что
    перестанет отдаваться в момент смены корня nginx. Вызывается отсюда,
    чтобы ответ давала одна команда: проверка, которую надо вспомнить, чтобы
    запустить, рано или поздно не запускается.
    """
    if TOOLS not in sys.path:
        sys.path.insert(0, TOOLS)
    try:
        import preflight_launch
        return preflight_launch.run_checks()
    except Exception as e:                       # noqa: BLE001
        return [Row(u'готовность к подмене', False,
                    u'не запустилась: %s: %s' % (type(e).__name__, e))]


def main():
    fast = '--fast' in sys.argv
    corpus = [check_verify(), check_layout(), check_nav(), check_audit(fast),
              check_sitemap(),
              check_site('contrast_check.py', u'контраст меню'),
              check_site('menu_fits.py', u'меню помещается в шапку'),
              check_prod_untouched(), check_guard()]
    launch = [] if '--corpus' in sys.argv else check_launch()
    rows = corpus + launch

    width = max(len(r.name) for r in rows)
    line = '=' * (width + 60)
    print('')
    print(u'ПРЕДПОЛЁТ: %d проверок' % len(rows))
    print(line)
    print(u'  -- корпус ' + '-' * (width + 48))
    for r in corpus:
        print(u'  %-6s %-*s  %s' % (u'ok' if r.ok else u'ПРОВАЛ', width,
                                    r.name, r.note))
    if launch:
        print(u'  -- готовность к подмене ' + '-' * (width + 34))
        for r in launch:
            print(u'  %-6s %-*s  %s' % (u'ok' if r.ok else u'ПРОВАЛ', width,
                                        r.name, r.note))
    print(line)
    bad = [r for r in rows if not r.ok]
    print(u'провалено: %d из %d' % (len(bad), len(rows)))
    if any(not r.ok for r in launch):
        print(u'подробности по подмене: python _tools/preflight_launch.py -v')
    return len(bad)


if __name__ == '__main__':
    sys.exit(main())
