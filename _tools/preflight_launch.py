# -*- coding: utf-8 -*-
u"""Готовность к подмене боевого сайта черновиком _v2.

Зачем отдельный файл. `preflight_all.py` проверяет КОРПУС: сошлись ли мастера
со страницами, одинакова ли разметка у девяти языков, не тронуто ли боевое
дерево. Ни одна из тех проверок не отвечает на вопрос, который решается в день
подмены: что перестанет отдаваться, когда корень nginx переедет на _v2.

Аудит 2026-09-01 нашёл 29 таких мест, и ни одно из них не ловилось ничем.
Пример цены: в боевом sitemap 72 адреса тем, которых в _v2 нет; 22 адреса
хинди отдают сегодня 200, а редиректа для них нет ни одного. Найдено это было
руками. Проверка, которую надо вспомнить, чтобы запустить, рано или поздно не
запускается - поэтому здесь она одна на всё и вызывается из общей приёмки.

Три правила, унаследованные от `preflight_all.py` и нарушать их нельзя:

  1. Проверка, которая НЕ СМОГЛА запуститься, считается ПРОВАЛЕННОЙ, а не
     пропущенной. Нет файла, нет карты редиректов, нет конфига - это провал.
  2. Проверка на пустом входе не «проходит». Везде, где считается доля или
     перебирается список, стоит assert на непустоту: проверка, молча
     прошедшая на нуле данных, хуже отсутствующей.
  3. Словари запрещённых знаков и цветов строятся из ЧИСЛОВЫХ кодпойнтов,
     а не из литералов: литералы портятся при переносе между оболочками
     молча, и проверка начинает мерить не то.

Что считается «отдастся после подмены». Три источника, и только они:
  - файл лежит в `_v2` по тому же адресу;
  - путь начинается с каталога, который остаётся общим с боевым деревом
    (список читается из ЖИВОГО `earthlings-nginx/new.conf`, а не хранится
    здесь копией: копия разошлась бы при первой правке конфига);
  - адрес есть в карте 301-редиректов `nginx/redirects-docs.map`.

Запуск:

    python _tools/preflight_launch.py            таблица проверок
    python _tools/preflight_launch.py -v         с перечнем того, что нашлось

Код возврата - число проваленных проверок, 0 если провалов нет.
"""
import glob
import gzip
import io
import os
import re
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
SITE = os.environ.get('EARTHLINGS_SITE') or os.path.join(
    os.path.dirname(REPO), 'earth-lings-site')
V2 = os.path.join(SITE, '_v2')
NGINX = os.environ.get('EARTHLINGS_NGINX') or os.path.join(
    os.path.dirname(REPO), 'earthlings-nginx')

LANGS = ['ar', 'de', 'en', 'es', 'fr', 'hi', 'ka', 'ru', 'zh']

# Бюджеты из README черновика, в БАЙТАХ ПОСЛЕ GZIP - как уходит по сети.
BUDGET_CSS = 30 * 1024
BUDGET_HTML = 60 * 1024

# Корневые файлы, без которых боевой домен теряет уже заработанное.
# Значение - зачем он нужен; попадает в отчёт, чтобы «добавить файл» не
# выглядело формальностью.
REQUIRED_ROOT = {
    'favicon.ico': u'значок вкладки',
    'manifest.json': u'установка на домашний экран',
    '404.html': u'страница ненайденного',
    'robots.txt': u'политика обхода',
    'sitemap.xml': u'карта сайта',
    'llms.txt': u'описание для ИИ-краулеров',
}

# Файлы подтверждения владения доменом. Именами не перечисляются: имя такого
# файла - выданный поисковиком код, а репозиторий корпуса публичный. Вместо
# списка они НАХОДЯТСЯ в корне боевого дерева по образцу - заодно проверка
# сама подхватит подтверждение, которое заведут завтра.
VERIFY_PATTERNS = [
    ('google*.html', u'подтверждение Search Console'),
    ('yandex_*.html', u'подтверждение Яндекс.Вебмастера'),
    ('.well-known', u'служебный каталог (в т.ч. продление сертификата)'),
]

# Каталоги, которым не место в корне боевого домена. Сегодня они закрыты
# правилом `location ~ ^/_`, но после подмены _v2 СТАНОВИТСЯ корнем, и это
# правило перестаёт их закрывать.
NOT_IN_WEBROOT = ['preview', 'i18n', 'tools']

# Разделы, перенесённые в новый сайт КАК ЕСТЬ (решение Артура). У них своя
# вёрстка, свои стили и своя обвязка; на новый дизайн они не переводятся.
#
# Требовать с них токены, hreflang, значок и бюджеты нового сайта - значит
# получить триста провалов, которые никто не собирается чинить, и через
# неделю выключить всю приёмку. Поэтому они проверяются только на то, что
# от них зависит снаружи: ведут ли ссылки в существующее и не попадает ли
# адрес под серверные редиректы.
#
# `preview` в этот список не входит: он не переносится вовсе, а удаляется.
CARRIED = ['awakened_code']


class Row(object):
    def __init__(self, name, ok, note, details=None):
        self.name = name
        self.ok = ok
        self.note = note
        self.details = details or []


def fail(name, why):
    u"""Проверка не смогла запуститься. Это провал, а не пропуск."""
    return Row(name, False, u'не смогла запуститься: %s' % why)


def read(path):
    return io.open(path, encoding='utf-8', errors='replace').read()


def rel(path, root):
    return os.path.relpath(path, root).replace(os.sep, '/')


# --------------------------------------------------------------------------
# Общий разбор дерева. Считается один раз и раздаётся проверкам: обход 267
# файлов на каждую из девятнадцати проверок стоил бы минуту на пустом месте.
# --------------------------------------------------------------------------

class Tree(object):
    def __init__(self):
        self.pages = {}          # страницы НОВОГО сайта: полный стандарт
        self.carried = {}        # перенесённые как есть: только связность
        self.css = {}            # css/имя.css -> текст
        self.classes = set()     # классы разметки нового сайта
        self.ids = set()

    def every(self):
        u"""Все страницы дерева. Для проверок связности: битая ссылка в
        перенесённом разделе отдаёт 404 ровно так же, как своя."""
        d = dict(self.pages)
        d.update(self.carried)
        return d

    @classmethod
    def load(cls):
        t = cls()
        if not os.path.isdir(V2):
            raise IOError(u'нет каталога черновика: %s' % V2)
        for dirpath, dirnames, filenames in os.walk(V2):
            parts = rel(dirpath, V2).split('/')
            if 'preview' in parts:
                continue
            carried = parts[0] in CARRIED
            for fn in filenames:
                if not fn.endswith('.html'):
                    continue
                p = os.path.join(dirpath, fn)
                (t.carried if carried else t.pages)[rel(p, V2)] = read(p)
        for p in sorted(glob.glob(os.path.join(V2, 'css', '*.css'))):
            t.css[rel(p, V2)] = read(p)
        if not t.pages:
            raise IOError(u'в черновике не найдено ни одной своей страницы')
        if not t.css:
            raise IOError(u'в черновике не найдено ни одного файла стилей')
        # Классы и id собираются ТОЛЬКО со своих страниц: у перенесённых
        # разделов свои стили, и их классы «оживили» бы мёртвые правила в
        # наших, а свои - утонули бы в их именах.
        for s in t.pages.values():
            for m in re.finditer(r'\bclass="([^"]*)"', s):
                t.classes.update(m.group(1).split())
            for m in re.finditer(r'\sid="([^"]+)"', s):
                t.ids.add(m.group(1))
        return t

    def url_of(self, relpath):
        u"""Файл -> адрес, каким его увидит читатель."""
        u = '/' + relpath
        return u[:-len('index.html')] if u.endswith('/index.html') else u


def strip_css_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def main_of(html):
    u"""Тело документа без шапки и подвала. Перекрёстные ссылки корпуса живут
    только здесь; ссылки обвязки на другие языки законны и в счёт не идут."""
    m = re.search(r'<main\b[^>]*>(.*)</main>', html, re.S)
    return m.group(1) if m else ''


# --------------------------------------------------------------------------
# Источники правды, которые лежат ВНЕ этого файла и читаются живьём.
# --------------------------------------------------------------------------

def load_shared_dirs():
    u"""Каталоги, остающиеся общими с боевым деревом.

    Читаются из живого `new.conf`, а не хранятся здесь списком. Причина
    ровно та же, по которой menu_fits.py читает величины из tokens.css:
    копия разошлась бы с оригиналом при первой правке, и проверка начала бы
    мерить состояние, которого нет.
    """
    p = os.path.join(NGINX, 'new.conf')
    if not os.path.isfile(p):
        raise IOError(u'нет снимка nginx: %s' % p)
    m = re.search(r'location\s+~\s+\^/\(([a-z_|]+)\)/', read(p))
    if not m:
        raise IOError(u'в new.conf не найдена группа общих каталогов')
    dirs = [d for d in m.group(1).split('|') if d]
    if not dirs:
        raise IOError(u'группа общих каталогов пуста')
    return dirs


def load_redirects():
    p = os.path.join(SITE, 'nginx', 'redirects-docs.map')
    if not os.path.isfile(p):
        raise IOError(u'нет карты редиректов: %s' % p)
    red = {}
    for line in read(p).split('\n'):
        m = re.match(r'\s*(/\S+)\s+(/\S+);', line)
        if m:
            red[m.group(1)] = m.group(2)
    if not red:
        raise IOError(u'карта редиректов пуста')
    return red


def make_resolver(shared, redirects):
    u"""Отдастся ли адрес после подмены и откуда."""
    def resolve(url):
        path = url.split('#')[0].split('?')[0]
        if not path.startswith('/'):
            return None
        f = path + 'index.html' if path.endswith('/') else path
        if os.path.isfile(os.path.join(V2, f.lstrip('/'))):
            return 'v2'
        top = path.strip('/').split('/')[0]
        if top in shared and os.path.exists(os.path.join(SITE, f.lstrip('/'))):
            return 'shared'
        if path in redirects:
            return 'redirect'
        return None
    return resolve


# ==========================================================================
# ПРОВЕРКИ
# ==========================================================================

def check_continuity(tree, resolve):
    u"""Каждый адрес боевого sitemap обязан отдаваться и после подмены."""
    name = u'континуитет: адреса боевого sitemap'
    p = os.path.join(SITE, 'sitemap.xml')
    if not os.path.isfile(p):
        return fail(name, u'нет боевого sitemap: %s' % p)
    locs = re.findall(r'<loc>https://earth-lings[.]org([^<]*)</loc>', read(p))
    if not locs:
        return fail(name, u'в боевом sitemap ни одного адреса')
    gone = [u for u in locs if resolve(u) is None]
    return Row(name, not gone,
               u'адресов %d, потеряется %d' % (len(locs), len(gone)),
               gone)


def check_live_documents(tree, resolve):
    u"""Страницы корпуса, которые сегодня отдают 200 и не имеют редиректа.

    Отдельно от sitemap: адрес может быть живым и проиндексированным, не
    попав в карту сайта. Так и вышло с хинди - 22 страницы на прежних
    слагах, ни одной записи в карте редиректов.
    """
    name = u'континуитет: живые страницы корпуса'
    docs = os.path.join(SITE, 'documents')
    if not os.path.isdir(docs):
        return fail(name, u'нет боевого каталога documents')
    live = []
    for lang in LANGS:
        d = os.path.join(docs, lang)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.html'):
                live.append('/documents/%s/%s' % (lang, fn))
    if not live:
        return fail(name, u'в боевом дереве не найдено ни одной страницы корпуса')
    gone = [u for u in live if resolve(u) is None]
    return Row(name, not gone,
               u'страниц %d, потеряется %d' % (len(live), len(gone)), gone)


def check_internal_links(tree, resolve):
    u"""Внутренние ссылки черновика ведут туда, где после подмены что-то есть."""
    name = u'внутренние ссылки черновика'
    bad = {}
    for relpath, s in tree.every().items():
        base = os.path.dirname(relpath)
        for href in re.findall(r'href="([^"]+)"', s):
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:',
                                '#', 'data:', 'javascript:')):
                continue
            path = href.split('#')[0].split('?')[0]
            if not path:
                continue
            if not path.startswith('/'):
                path = '/' + os.path.normpath(
                    os.path.join(base, path)).replace(os.sep, '/')
            if resolve(path) is None:
                bad.setdefault(path, []).append(relpath)
    total = sum(len(v) for v in bad.values())
    return Row(name, not bad,
               u'битых целей %d, вхождений %d' % (len(bad), total),
               [u'%s (%d стр., напр. %s)' % (k, len(v), v[0])
                for k, v in sorted(bad.items())])


def check_root_files(tree, resolve):
    u"""Корневые файлы, теряющиеся вместе со сменой корня."""
    name = u'корневые файлы на месте'
    need = [(f, why) for f, why in sorted(REQUIRED_ROOT.items())]
    for pattern, why in VERIFY_PATTERNS:
        found = [os.path.basename(p)
                 for p in sorted(glob.glob(os.path.join(SITE, pattern)))]
        if not found:
            continue                 # такого подтверждения нет и в боевом
        need.extend((f, why) for f in found)
    if not need:
        return fail(name, u'список обязательных файлов пуст')
    missing = [u'%s - %s' % (f, why) for f, why in need
               if resolve('/' + f) is None]
    return Row(name, not missing,
               u'обязательных %d, нет %d' % (len(need), len(missing)),
               missing)


def check_head_icons(tree, resolve):
    u"""Значок и манифест объявлены в разметке, а не только лежат в корне."""
    name = u'значок и манифест в разметке'
    no_icon = [p for p, s in tree.pages.items()
               if not re.search(r'<link[^>]+rel="[^"]*\bicon\b[^"]*"', s)]
    no_manifest = [p for p, s in tree.pages.items()
                   if 'rel="manifest"' not in s]
    bad = []
    if no_icon:
        bad.append(u'без значка: %d' % len(no_icon))
    if no_manifest:
        bad.append(u'без манифеста: %d' % len(no_manifest))
    return Row(name, not bad,
               u'страниц %d; %s' % (len(tree.pages),
                                    ', '.join(bad) if bad else u'все объявлены'),
               (no_icon or no_manifest)[:20])


def check_robots(tree, resolve):
    u"""robots.txt боевой, а не черновиковый."""
    name = u'robots.txt боевой'
    p = os.path.join(V2, 'robots.txt')
    if not os.path.isfile(p):
        return fail(name, u'нет robots.txt в черновике')
    s = read(p)
    bad = []
    if re.search(r'(?mi)^\s*Disallow:\s*/\s*$', s):
        bad.append(u'стоит Disallow: / - весь сайт закрыт от индексации')
    if not re.search(r'(?mi)^\s*Sitemap:\s*http', s):
        bad.append(u'нет строки Sitemap:')
    return Row(name, not bad,
               u'проверок 2, провалов %d' % len(bad), bad)


def check_webroot_clean(tree, resolve):
    u"""Служебных каталогов в корне будущего боевого домена нет."""
    name = u'служебного в корне нет'
    present = [d for d in NOT_IN_WEBROOT if os.path.isdir(os.path.join(V2, d))]
    return Row(name, not present,
               u'служебных каталогов в корне: %d' % len(present),
               [u'/%s/ - после подмены отдаётся наружу' % d for d in present])


def check_cross_language(tree, resolve):
    u"""Ссылка в теле документа ведёт на страницу СВОЕГО языка."""
    name = u'перекрёстные ссылки внутри языка'
    bad = []
    seen = 0
    for relpath, s in sorted(tree.pages.items()):
        m = re.match(r'documents/([a-z]{2})/', relpath)
        if not m:
            continue
        lang = m.group(1)
        seen += 1
        for other in re.findall(r'href="[^"]*?/documents/([a-z]{2})/[^"]*"',
                                main_of(s)):
            if other != lang:
                bad.append(u'%s -> /documents/%s/' % (relpath, other))
    if not seen:
        return fail(name, u'в черновике не найдено ни одной страницы корпуса')
    return Row(name, not bad,
               u'страниц корпуса %d, чужих ссылок %d' % (seen, len(bad)), bad)


def check_descriptions(tree, resolve):
    u"""У каждой страницы непустое описание."""
    name = u'описание на каждой странице'
    bad = [p for p, s in sorted(tree.pages.items())
           if not re.search(r'<meta name="description" content="[^"]+"', s)]
    return Row(name, not bad,
               u'страниц %d, без описания %d' % (len(tree.pages), len(bad)), bad)


def check_hreflang(tree, resolve):
    u"""Кластер hreflang самоссылочен и взаимен."""
    name = u'hreflang самоссылочный и взаимный'
    ann = {}
    for relpath, s in tree.pages.items():
        head = s.split('</head>')[0]
        ann[tree.url_of(relpath)] = dict(re.findall(
            r'<link rel="alternate" hreflang="([^"]+)" '
            r'href="https://earth-lings[.]org([^"]+)"', head))
    if not any(ann.values()):
        return fail(name, u'ни на одной странице нет hreflang')
    bad = []
    for url, hl in sorted(ann.items()):
        if not hl:
            continue
        if url not in hl.values():
            bad.append(u'%s не перечисляет себя' % url)
            continue
        for lang, target in hl.items():
            if lang == 'x-default':
                continue
            other = ann.get(target)
            if other is not None and url not in other.values():
                bad.append(u'%s -> %s, обратной ссылки нет' % (url, target))
    return Row(name, not bad,
               u'кластеров %d, невзаимных мест %d' % (len(ann), len(bad)), bad)


def check_social_meta(tree, resolve):
    u"""Обвязка соцсетей полна и картинка действительно существует."""
    name = u'обвязка соцсетей полна'
    no_locale = [p for p, s in tree.pages.items() if 'og:locale' not in s]
    no_tw = [p for p, s in tree.pages.items()
             if 'og:image' in s and 'twitter:description' not in s]
    missing_img = set()
    for s in tree.pages.values():
        for m in re.finditer(
                r'content="https://earth-lings[.]org(/[^"]+\.(?:jpg|png|webp))"', s):
            if resolve(m.group(1)) is None:
                missing_img.add(m.group(1))
    bad = []
    if no_locale:
        bad.append(u'без og:locale: %d' % len(no_locale))
    if no_tw:
        bad.append(u'без twitter:description: %d' % len(no_tw))
    if missing_img:
        bad.append(u'нет картинки: %s' % ', '.join(sorted(missing_img)))
    return Row(name, not bad,
               u'страниц %d; %s' % (len(tree.pages),
                                    ', '.join(bad) if bad else u'полна'),
               sorted(missing_img) + no_locale[:10] + no_tw[:10])


def check_tokens_defined(tree, resolve):
    u"""Каждый var(--...) объявлен. Необъявленный молча теряет свойство."""
    name = u'токены объявлены'
    tok = tree.css.get('css/tokens.css')
    if tok is None:
        return fail(name, u'нет css/tokens.css')
    defined = set(re.findall(r'(?m)^\s*(--[a-z0-9-]+)\s*:', tok))
    if not defined:
        return fail(name, u'в tokens.css не объявлено ни одного токена')
    used = {}
    for relpath, css in tree.css.items():
        for m in re.finditer(r'var\(\s*(--[a-z0-9-]+)\s*([,)])', css):
            # var(--x, запасное) объявления не требует: запасное и есть ответ.
            if m.group(2) == ',':
                continue
            used.setdefault(m.group(1), set()).add(relpath)
    undefined = sorted(k for k in used if k not in defined)
    return Row(name, not undefined,
               u'объявлено %d, используется без объявления %d'
               % (len(defined), len(undefined)),
               [u'%s (в %s)' % (k, ', '.join(sorted(used[k])))
                for k in undefined])


def check_dead_css(tree, resolve):
    u"""Правил под классы, которых нет ни на одной странице, быть не должно.

    Классы, которые ставит скрипт, живут в JS и находятся там же - иначе
    проверка ругалась бы на них вечно и была бы выключена через неделю.
    """
    name = u'мёртвых правил в стилях нет'
    js = ''
    for p in sorted(glob.glob(os.path.join(V2, 'js', '*.js'))):
        js += read(p)
    if not js:
        return fail(name, u'не найдено ни одного файла скриптов')
    known = set(tree.classes)
    known.update(re.findall(r'classList\.(?:add|remove|toggle)\(\s*[\'"]([\w-]+)',
                            js))
    dead = {}
    for relpath, css in tree.css.items():
        body = strip_css_comments(css)
        for sel in re.findall(r'(?m)^([^{}@/][^{}]*?)\{', body):
            for part in sel.split(','):
                for cls in re.findall(r'\.([A-Za-z][\w-]*)', part):
                    if cls not in known:
                        dead.setdefault(cls, set()).add(relpath)
    return Row(name, not dead,
               u'файлов стилей %d, мёртвых классов %d'
               % (len(tree.css), len(dead)),
               [u'.%s (%s)' % (k, ', '.join(sorted(v)))
                for k, v in sorted(dead.items())])


def check_unstyled_classes(tree, resolve):
    u"""Класс в разметке, у которого нет ни одного правила.

    Зеркало проверки мёртвых правил, и находит она другое. Мёртвое правило -
    это лишние байты. Класс без правила - это ЗАМЫСЕЛ, который не виден
    читателю: сборщик ставит `nav-item--here` на текущий пункт меню, а
    подсветки нет; ставит `tbl-wrap` вокруг таблицы, а прокрутки нет.
    Сборщик и стили расходятся молча, и заметить это можно только так.

    Ловится по разметке, потому что классы ставит генератор обвязки: если
    он перестанет их ставить, проверка промолчит - но тогда и замысла нет.
    """
    name = u'классы разметки описаны в стилях'
    styled = set()
    for css in tree.css.values():
        styled.update(re.findall(r'\.([A-Za-z][\w-]*)',
                                 strip_css_comments(css)))
    if not styled:
        return fail(name, u'в стилях не найдено ни одного класса')
    used = {}
    for relpath, s in tree.pages.items():
        for m in re.finditer(r'\bclass="([^"]*)"', s):
            for c in m.group(1).split():
                used.setdefault(c, set()).add(relpath)
    if not used:
        return fail(name, u'в разметке не найдено ни одного класса')
    orphan = sorted(c for c in used if c not in styled)
    return Row(name, not orphan,
               u'классов в разметке %d, без единого правила %d'
               % (len(used), len(orphan)),
               [u'.%s - %d стр., напр. %s'
                % (c, len(used[c]), sorted(used[c])[0]) for c in orphan])


def check_budgets(tree, resolve):
    u"""Вес страницы по сети: HTML и блокирующий отрисовку CSS, оба в gzip."""
    name = u'бюджеты веса страницы'
    sizes = {}
    for relpath, css in tree.css.items():
        sizes[relpath] = css.encode('utf-8')
    bad = []
    worst_html = ('', 0)
    for relpath, s in sorted(tree.pages.items()):
        raw = s.encode('utf-8')
        n = len(gzip.compress(raw, 9))
        if n > worst_html[1]:
            worst_html = (relpath, n)
        if n > BUDGET_HTML:
            bad.append(u'%s: HTML %d КБ при потолке %d'
                       % (relpath, n // 1024, BUDGET_HTML // 1024))
        head = s.split('</head>')[0]
        blob = b''
        for href in re.findall(r'<link rel="stylesheet" href="([^"]+)"', head):
            key = 'css/' + href.rsplit('/', 1)[-1]
            if key in sizes:
                blob += sizes[key]
        if not blob:
            bad.append(u'%s: не подключено ни одного файла стилей' % relpath)
            continue
        c = len(gzip.compress(blob, 9))
        if c > BUDGET_CSS:
            bad.append(u'%s: CSS %d КБ при потолке %d'
                       % (relpath, c // 1024, BUDGET_CSS // 1024))
    return Row(name, not bad,
               u'страниц %d, вне бюджета %d (самый тяжёлый HTML %d КБ)'
               % (len(tree.pages), len(bad), worst_html[1] // 1024),
               bad)


def check_colors(tree, resolve):
    u"""Цвет задаётся только токеном.

    Ищется hex и функциональная запись В ПОЗИЦИИ ЗНАЧЕНИЯ свойства: на
    витрине палитры коды написаны текстом как подписи образцов, и проверка
    «любой hex» срабатывала бы на них вечно.
    """
    name = u'цвет только из токенов'
    pat = re.compile(
        r'(?:color|background|border|outline|fill|stroke|shadow)[a-z-]*\s*:'
        r'[^;"\']*(?:#[0-9a-fA-F]{3,8}|rgba?\(|hsla?\()')
    bad = []
    for relpath, css in tree.css.items():
        if relpath == 'css/tokens.css':
            continue
        for i, line in enumerate(css.split('\n'), 1):
            if pat.search(strip_css_comments(line)):
                bad.append(u'%s:%d %s' % (relpath, i, line.strip()[:70]))
    for relpath, s in tree.pages.items():
        if pat.search(s):
            bad.append(u'%s (в разметке)' % relpath)
    return Row(name, not bad,
               u'файлов %d, цветов мимо токенов %d'
               % (len(tree.css) + len(tree.pages), len(bad)), bad)


def check_analytics(tree, resolve):
    u"""Счётчик на каждой странице: иначе половина сайта не измеряется."""
    name = u'счётчик на каждой странице'
    bad = [p for p, s in sorted(tree.pages.items())
           if 'stats.earth-lings.org' not in s]
    return Row(name, not bad,
               u'страниц %d, без счётчика %d' % (len(tree.pages), len(bad)), bad)


def check_css_assets(tree, resolve):
    u"""Каждый url() из стилей действительно отдаётся."""
    name = u'файлы, на которые ссылаются стили'
    missing = set()
    seen = 0
    for relpath, css in tree.css.items():
        for m in re.finditer(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', css):
            u = m.group(1)
            if u.startswith(('data:', 'http://', 'https://')):
                continue
            seen += 1
            if u.startswith('/'):
                path = u
            else:
                path = '/' + os.path.normpath(
                    os.path.join('css', u)).replace(os.sep, '/')
            if resolve(path) is None:
                missing.add(path)
    if not seen:
        return fail(name, u'в стилях не найдено ни одной ссылки на файл')
    return Row(name, not missing,
               u'ссылок %d, недостающих файлов %d' % (seen, len(missing)),
               sorted(missing))


def check_rtl(tree, resolve):
    u"""У физического свойства есть зеркальная пара для арабского.

    Логические свойства (padding-inline-start) пары не требуют - они
    зеркалятся сами, и это предпочтительный способ.
    """
    name = u'зеркальные пары для RTL'
    phys = re.compile(r'(?:margin|padding|border)-(?:left|right)\s*:'
                      r'|text-align:\s*(?:left|right)\b')
    bad = []
    for relpath, css in tree.css.items():
        if relpath.startswith('css/fonts-'):
            continue
        body = strip_css_comments(css)
        rules = re.findall(r'(?m)^([^{}@/][^{}]*?)\{([^}]*)\}', body)

        def parts(sel):
            u"""Селектор -> множество его частей. Сравнивать строкой целиком
            нельзя: `[dir=rtl] .a, [dir=rtl] .b` и `.b, .a` - одна и та же
            пара, записанная в другом порядке."""
            return set(p.strip() for p in sel.split(',') if p.strip())

        mirrored = set()
        for sel, _ in rules:
            if '[dir="rtl"]' in sel:
                mirrored |= parts(re.sub(r'\[dir="rtl"\]\s*', '', sel))
        for sel, decl in rules:
            if '[dir="rtl"]' in sel:
                continue
            if phys.search(decl) and not (parts(sel) & mirrored):
                bad.append(u'%s: %s' % (relpath, sel.strip()[:60]))
    return Row(name, not bad,
               u'правил без зеркальной пары %d' % len(bad), bad)


def check_own_lang_query(tree, resolve):
    u"""Свои адреса не должны нести ?lang= - боевой vhost их перехватывает.

    В `earth-lings.conf` на уровне server стоит правило, а не location:

        if ($arg_lang ~ "^(ru|en|de|es|fr|ar|hi|zh|ka)$") {
            return 301 https://earth-lings.org/$arg_lang/;
        }

    Оно заведено против дублей от прежнего SPA и срабатывает на ЛЮБОМ пути.
    На черновиковом поддомене такого правила нет, поэтому проверить это
    браузером на new.earth-lings.org невозможно - расхождение вылезет ровно
    в день подмены.

    Цена конкретная: рамка «Пробуждённого кода» на девяти главных загружена
    как /awakened_code/?embed=1&lang=xx. После подмены она отдаст 301 на
    /xx/, и главная покажет саму себя внутри собственной рамки.

    Чужие домены правило не трогает: ссылки на app.earth-lings.org с ?lang=
    законны и здесь не считаются.
    """
    name = u'свои адреса без ?lang='
    conf = os.path.join(NGINX, 'earth-lings.conf')
    if not os.path.isfile(conf):
        return fail(name, u'нет боевого vhost: %s' % conf)
    if 'arg_lang' not in read(conf):
        # Правила больше нет - проверка потеряла смысл и молчать об этом нельзя.
        return fail(name, u'в earth-lings.conf нет правила $arg_lang; '
                          u'проверку надо пересмотреть или снять')
    # `&amp;` в разметке обязателен по HTML, поэтому перед `lang=` стоит не
    # амперсанд, а точка с запятой. Первая версия этого правила искала
    # `[?&]lang=` и не находила НИ ОДНОГО из девяти вхождений: проверка
    # молча проходила на том самом дефекте, ради которого написана.
    bad = []
    for relpath, s in sorted(tree.every().items()):
        for m in re.finditer(
                r'(?:src|href)="(/[^"]*?[?&](?:amp;)?lang=[a-z]{2}[^"]*)"', s):
            bad.append(u'%s -> %s' % (relpath, m.group(1).replace('&amp;', '&')))
    return Row(name, not bad,
               u'своих адресов с ?lang= %d' % len(bad), bad)


def tags_only(html):
    u"""Разметка без содержимого, в котором могут стоять угловые скобки.

    Иначе разбор тегов считает разметкой то, что ею не является. Так и вышло:
    в awakened_code/index.html значок вкладки задан как
    href="data:image/svg+xml,<svg ...><text ...>%3E_</text></svg>", и проверка
    объявила страницу рваной - «лишний </svg>», - хотя она цела.

    Убираются комментарии, тела script и style и значения атрибутов в
    кавычках. Сами теги остаются нетронутыми.
    """
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    html = re.sub(r'(?is)<script\b[^>]*>.*?</script>', '<script></script>', html)
    html = re.sub(r'(?is)<style\b[^>]*>.*?</style>', '<style></style>', html)
    html = re.sub(r'=\s*"[^"]*"', '=""', html)
    html = re.sub(r"=\s*'[^']*'", "=''", html)
    return html


def check_markup(tree, resolve):
    u"""Разметка цела: без дублей id, висящих якорей и рваных тегов."""
    name = u'разметка цела'
    void = set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                'link', 'meta', 'source', 'track', 'wbr'])
    bad = []
    for relpath, s in sorted(tree.every().items()):
        ids = re.findall(r'\sid="([^"]+)"', s)
        dup = sorted(set(x for x in ids if ids.count(x) > 1))
        if dup:
            bad.append(u'%s: дубли id %s' % (relpath, ', '.join(dup[:4])))
        idset = set(ids)
        for fr in sorted(set(re.findall(r'href="#([^"]+)"', s))):
            if fr not in idset:
                bad.append(u'%s: висящий якорь #%s' % (relpath, fr))
        stack = []
        for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>',
                             tags_only(s)):
            close, tag, self_ = m.group(1), m.group(2).lower(), m.group(3)
            if tag in void or self_:
                continue
            if not close:
                stack.append(tag)
            elif stack and stack[-1] == tag:
                stack.pop()
            else:
                bad.append(u'%s: лишний </%s>' % (relpath, tag))
                break
        if stack:
            bad.append(u'%s: не закрыто %s' % (relpath, ', '.join(stack[:4])))
    return Row(name, not bad,
               u'страниц %d, мест с рваной разметкой %d'
               % (len(tree.pages), len(bad)), bad)


CHECKS = [
    check_continuity,
    check_live_documents,
    check_internal_links,
    check_root_files,
    check_head_icons,
    check_robots,
    check_webroot_clean,
    check_cross_language,
    check_descriptions,
    check_hreflang,
    check_social_meta,
    check_tokens_defined,
    check_dead_css,
    check_unstyled_classes,
    check_budgets,
    check_colors,
    check_analytics,
    check_css_assets,
    check_rtl,
    check_own_lang_query,
    check_markup,
]


def run_checks():
    u"""Возвращает список Row. Ни одно исключение наружу не выпускается:
    упавшая проверка - это провал с объяснением, а не обвал приёмки.

    Если не прочитались общие входы - дерево черновика, снимок nginx, карта
    редиректов, - возвращается ОДНА строка провала, а не девятнадцать
    одинаковых. Девятнадцать раз повторить «нет файла» значит спрятать
    причину в шуме; провалом это остаётся в обоих случаях.
    """
    try:
        tree = Tree.load()
        shared = load_shared_dirs()
        redirects = load_redirects()
    except Exception as e:                       # noqa: BLE001
        return [fail(u'готовность к подмене (%d проверок)' % len(CHECKS),
                     u'%s' % e)]
    resolve = make_resolver(shared, redirects)

    rows = []
    for f in CHECKS:
        try:
            rows.append(f(tree, resolve))
        except Exception as e:                   # noqa: BLE001
            rows.append(fail(f.__name__, u'%s: %s' % (type(e).__name__, e)))
    return rows


def main():
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    rows = run_checks()
    width = max(len(r.name) for r in rows)
    print('')
    print(u'ГОТОВНОСТЬ К ПОДМЕНЕ: %d проверок' % len(rows))
    print('=' * (width + 62))
    for r in rows:
        print(u'  %-6s %-*s  %s'
              % (u'ok' if r.ok else u'ПРОВАЛ', width, r.name, r.note))
        if verbose and not r.ok and r.details:
            for d in r.details[:40]:
                print(u'           %s' % d)
            if len(r.details) > 40:
                print(u'           ... ещё %d' % (len(r.details) - 40))
    print('=' * (width + 62))
    bad = [r for r in rows if not r.ok]
    print(u'провалено: %d из %d' % (len(bad), len(rows)))
    if bad and not verbose:
        print(u'подробности: python _tools/preflight_launch.py -v')
    return len(bad)


if __name__ == '__main__':
    sys.exit(main())
