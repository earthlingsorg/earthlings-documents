# -*- coding: utf-8 -*-
u"""Собирает страницу подписей /verification/documents/ из настоящего дерева.

Зачем. Прежняя страница была написана при v1 и с тех пор не менялась: она
говорила «54 документа, 27 английских, 27 русских», когда подписей лежало
больше тысячи, а ссылки строила скриптом из шаблона, поэтому ни одна проверка
не видела, что они ведут в 403. Кнопки «Browse» с главной страницы проверки
пять подписей подряд вели человека именно туда.

Что делает. Обходит `_v2/verification/documents/` и пишет список подписей по
версиям (от новой к старой, якоря #v6 ... #v1), внутри версии - по языкам.
Чисел руками нет ни одного: версии, языки и файлы считаются обходом. Появится
v7 или десятый язык - страница расскажет о них сама.

Каждая строка - ссылка на файл подписи и, если документ с таким именем
опубликован сегодня, ссылка на него. Для версий с манифестом сборщик ещё и
сверяет сегодняшний файл с хешем из манифеста этой версии: совпал - подпись
прикладывается к живому файлу; не совпал - файл с тех пор менялся, и подпись
проверяется против состояния из истории Git. Без этой сверки ссылка «документ»
у v5 вела бы на файл, к которому подпись v5 уже не прикладывается.

Ссылки только статические и только на файлы: просмотр каталогов в nginx
выключен, ссылка на каталог без index.html - это 403.

Подписанный набор страница не трогает: манифесты подписывают страницы
документов и файлы .sig, навигационные страницы не подписываются.

Запуск:
    python _tools/build_verification_index.py           собрать
    python _tools/build_verification_index.py --check   сверить с диском, 1 - отстала
"""
import hashlib
import io
import os
import re
import sys
from html import escape

TOOLS = os.path.dirname(os.path.abspath(__file__))
assert os.path.isdir(TOOLS), TOOLS
sys.path.insert(0, TOOLS)

from build_site_docs import SITE    # noqa: E402
import site_guard as guard          # noqa: E402

V2 = os.path.join(SITE, '_v2')
VERIF = os.path.join(V2, 'verification')
SIGDIR = os.path.join(VERIF, 'documents')
DOCS = os.path.join(V2, 'documents')
OUT = os.path.join(SIGDIR, 'index.html')

LANG_NAMES = {'ar': 'Arabic', 'de': 'German', 'en': 'English', 'es': 'Spanish',
              'fr': 'French', 'hi': 'Hindi', 'ka': 'Georgian', 'ru': 'Russian',
              'zh': 'Chinese'}


def vnum(v):
    return int(v[1:])


def manifest_of(v):
    u"""Имя манифеста версии: у v1 без номера, у прочих MANIFEST-vN."""
    return 'MANIFEST.txt.asc' if v == 'v1' else 'MANIFEST-%s.txt.asc' % v


def chain_of(v):
    u"""Цепочка доверия: при v2 она называлась без номера, с v3 - с номером."""
    return {'v1': None, 'v2': 'CHAIN-OF-TRUST.txt.asc'}.get(v, 'CHAIN-OF-TRUST-%s.txt.asc' % v)


def manifest_hashes(v):
    p = os.path.join(VERIF, manifest_of(v))
    if not os.path.isfile(p):
        return None
    t = io.open(p, encoding='utf-8', errors='replace').read()
    h = dict((path, sha) for sha, path in
             re.findall(r'^([a-f0-9]{64})  (\S+\.html)$', t, re.M))
    return h or None


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def collect():
    u"""{версия: {язык: [(файл подписи, имя документа)]}} из обхода дерева.

    v1 - clearsigned `<язык>/<имя>.html.asc` прямо в каталоге языка; v2 и
    дальше - отдельные подписи `<язык>/vN/<имя>.html.sig`.
    """
    tree = {}
    for lang in sorted(os.listdir(SIGDIR)):
        ld = os.path.join(SIGDIR, lang)
        if not os.path.isdir(ld):
            continue
        for name in sorted(os.listdir(ld)):
            p = os.path.join(ld, name)
            if os.path.isfile(p) and name.endswith('.html.asc'):
                tree.setdefault('v1', {}).setdefault(lang, []).append(
                    ('%s/%s' % (lang, name), name[:-len('.asc')]))
            elif os.path.isdir(p) and re.match(r'^v\d+$', name):
                for s in sorted(os.listdir(p)):
                    if s.endswith('.html.sig') and os.path.isfile(os.path.join(p, s)):
                        tree.setdefault(name, {}).setdefault(lang, []).append(
                            ('%s/%s/%s' % (lang, name, s), s[:-len('.sig')]))
    assert tree, u'в %s не нашлось ни одной подписи' % SIGDIR
    return tree


def status_of(v, langs):
    u"""Для каждой подписи: есть ли документ сегодня и совпадает ли он с
    хешем манифеста версии. Возвращает строки и счётчики."""
    hashes = manifest_hashes(v) if v != 'v1' else None
    rows, n, exists, match = {}, 0, 0, 0
    for lang, items in langs.items():
        out = []
        for sig, doc in items:
            n += 1
            live = os.path.join(DOCS, lang, doc)
            ok_live = os.path.isfile(live)
            same = None
            if ok_live:
                exists += 1
                if hashes is not None:
                    want = hashes.get('%s/%s' % (lang, doc))
                    same = want is not None and sha256(live) == want
                    match += 1 if same else 0
            out.append((sig, doc, ok_live, same))
        rows[lang] = out
    return rows, n, exists, match, hashes is not None


def version_note(v, n, exists, match, has_hashes):
    u"""Пояснение к версии - по счётчикам, а не написанное заранее."""
    if v == 'v1':
        tail = (u'Each file is a clearsigned copy: it carries the document text and its signature '
                u'together, and verifies on its own with <code>gpg --verify</code> and the original '
                u'public key.')
    else:
        tail = (u'Each file is a detached signature: it verifies against the document file with '
                u'<code>gpg --verify &lt;file&gt;.sig &lt;file&gt;</code>.')
    if exists == 0 and v == 'v1':
        state = (u'No file signed by v1 exists today under its v1 name: the corpus was renumbered '
                 u'since, and the file names moved from short forms (<code>ru01.html</code>) to slug '
                 u'forms (<code>ru01-deklaraciya.html</code>).')
    elif exists == 0:
        state = (u'No file signed by %s exists today under its %s name: the corpus was renumbered '
                 u'since, and the file names moved from short forms (<code>ru01.html</code>) to slug '
                 u'forms (<code>ru01-deklaraciya.html</code>). A %s signature therefore cannot be '
                 u'checked against the present tree. The file state it attests is not published; it '
                 u'is kept in the author\'s archive and supplied on request. The manifest and the '
                 u'chain of trust of %s verify on their own with the public key.' % (v, v, v, v))
    elif has_hashes and match == n:
        state = (u'Every document of %s is published today exactly as signed: the signature '
                 u'verifies against the live file.' % v)
    elif has_hashes and match == 0:
        state = (u'The file names are still in use, but every file has changed since %s was signed, '
                 u'so a %s signature does not verify against today\'s file. The %s file state is not '
                 u'published; it is kept in the author\'s archive and supplied on request. The '
                 u'manifest and the chain of trust of %s verify on their own with the public key.'
                 % (v, v, v, v))
    elif has_hashes:
        state = (u'%d of %d documents are published today exactly as signed; the others have changed '
                 u'since, and the %s state they were signed in is not published - it is kept in the '
                 u'author\'s archive and supplied on request.' % (match, n, v))
    else:
        state = (u'%d of %d documents exist today under the same name.' % (exists, n))
    return state + u' ' + tail


def render(tree):
    versions = sorted(tree, key=vnum, reverse=True)
    total = sum(len(i) for v in tree.values() for i in v.values())
    all_langs = sorted({l for v in tree.values() for l in v})
    o = []
    w = o.append
    w(u'<!DOCTYPE html>')
    w(u'<html lang="en">')
    w(u'<head>')
    w(u'    <meta charset="UTF-8">')
    w(u'    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    w(u'    <title>Earthlings Project - Signed Documents</title>')
    w(u'    <meta name="robots" content="noindex">')
    w(u'    <style>')
    w(u'        body { font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; '
      u'margin: 0 auto; padding: 20px; background: #f8f9fa; color: #333; }')
    w(u'        .header { text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
      u'color: white; padding: 40px 20px; border-radius: 10px; margin-bottom: 30px; }')
    w(u'        .section { background: white; padding: 30px; margin-bottom: 20px; border-radius: 10px; '
      u'box-shadow: 0 2px 10px rgba(0,0,0,0.1); }')
    w(u'        h1 { color: white; margin-bottom: 10px; }')
    w(u'        h2 { color: #667eea; border-bottom: 2px solid #eee; padding-bottom: 10px; }')
    w(u'        h3 { color: #495057; }')
    w(u'        .back-link { display: inline-block; background: #6c757d; color: white; padding: 8px 16px; '
      u'text-decoration: none; border-radius: 5px; margin-bottom: 20px; }')
    w(u'        .back-link:hover { background: #5a6268; }')
    w(u'        .info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 15px; '
      u'border-radius: 5px; margin: 15px 0; }')
    w(u'        table { width: 100%; border-collapse: collapse; margin: 10px 0; }')
    w(u'        th, td { padding: 6px 10px; text-align: left; border-bottom: 1px solid #dee2e6; font-size: 14px; }')
    w(u'        th { background: #f8f9fa; font-weight: 600; }')
    w(u'        .mono { font-family: monospace; font-size: 12px; word-break: break-all; }')
    w(u'        .muted { color: #6c757d; }')
    w(u'        .toc a { display: inline-block; margin: 0 12px 8px 0; color: #667eea; font-weight: bold; }')
    w(u'        details { margin: 8px 0; }')
    w(u'        summary { cursor: pointer; color: #667eea; font-weight: bold; padding: 4px 0; }')
    w(u'        a { color: #283593; }')
    w(u'    </style>')
    w(u'</head>')
    w(u'<body>')
    w(u'    <a href="../index.html" class="back-link">Back to Verification</a>')
    w(u'')
    w(u'    <div class="header">')
    w(u'        <h1>Signed Documents</h1>')
    w(u'        <p style="margin-top: 15px; font-size: 18px;">%d signature files in %d versions, %d languages</p>'
      % (total, len(versions), len(all_langs)))
    w(u'    </div>')
    w(u'')
    w(u'    <div class="section">')
    w(u'        <h2>Versions</h2>')
    w(u'        <table>')
    w(u'            <tr><th>Version</th><th>Signature files</th><th>Languages</th><th>Manifest</th></tr>')
    for v in versions:
        langs = tree[v]
        n = sum(len(i) for i in langs.values())
        man = manifest_of(v)
        man_cell = (u'<a href="../%s" download>%s</a>' % (man, man)
                    if os.path.isfile(os.path.join(VERIF, man)) else u'<span class="muted">-</span>')
        w(u'            <tr><td><a href="#%s">%s</a></td><td>%d</td><td>%d (%s)</td><td>%s</td></tr>'
          % (v, v, n, len(langs), u', '.join(sorted(langs)), man_cell))
    w(u'        </table>')
    w(u'        <div class="info">This page is built from the signature files on the server: every number and '
      u'every link below comes from the directory itself. The current version is %s. How to check a '
      u'signature is shown on the <a href="../index.html">verification page</a>.</div>' % versions[0])
    w(u'    </div>')

    for v in versions:
        rows, n, exists, match, has_hashes = status_of(v, tree[v])
        chain = chain_of(v)
        w(u'')
        w(u'    <div class="section" id="%s">' % v)
        w(u'        <h2>%s - %d signature files</h2>' % (v, n))
        w(u'        <p>%s</p>' % version_note(v, n, exists, match, has_hashes))
        links = []
        man = manifest_of(v)
        if os.path.isfile(os.path.join(VERIF, man)):
            links.append(u'<a href="../%s" download>%s</a>' % (man, man))
        if chain and os.path.isfile(os.path.join(VERIF, chain)):
            links.append(u'<a href="../%s" download>%s</a>' % (chain, chain))
        if links:
            w(u'        <p>Signed records of this version: %s</p>' % u' | '.join(links))
        for lang in sorted(rows):
            items = rows[lang]
            w(u'        <details id="%s-%s">' % (v, lang))
            w(u'            <summary>%s (%s) - %d files</summary>'
              % (LANG_NAMES.get(lang, lang), lang, len(items)))
            w(u'            <table>')
            w(u'                <tr><th>Signature</th><th>Document today</th></tr>')
            for sig, doc, ok_live, same in items:
                sig_cell = u'<a class="mono" href="%s" download>%s</a>' % (escape(sig), escape(sig.split('/')[-1]))
                if not ok_live:
                    doc_cell = u'<span class="muted">no file under this name today</span>'
                else:
                    link = u'<a class="mono" href="../../documents/%s/%s">%s</a>' % (lang, escape(doc), escape(doc))
                    if same is True:
                        doc_cell = link + u' <span class="muted">(matches)</span>'
                    elif same is False:
                        doc_cell = link + u' <span class="muted">(changed since %s)</span>' % v
                    else:
                        doc_cell = link
                w(u'                <tr><td>%s</td><td>%s</td></tr>' % (sig_cell, doc_cell))
            w(u'            </table>')
            w(u'        </details>')
        w(u'    </div>')

    w(u'')
    w(u'    <footer style="text-align: center; margin-top: 40px; color: #666;">')
    w(u'        <p>Earthlings project | Artur Arakelian | <a href="mailto:info@earth-lings.org">info@earth-lings.org</a></p>')
    w(u'        <p style="font-size: 12px; margin-top: 10px;"><a href="../index.html">Back to Verification</a> | '
      u'<a href="../arakelian-public-key.asc" download>Download Public Key</a></p>')
    w(u'    </footer>')
    w(u'</body>')
    w(u'</html>')
    return u'\n'.join(o) + u'\n'


def main():
    page = render(collect())
    if '--check' in sys.argv:
        cur = io.open(OUT, encoding='utf-8', newline='').read() if os.path.isfile(OUT) else u''
        if cur == page:
            print(u'страница подписей совпадает с деревом: отставания нет')
            return 0
        print(u'страница подписей ОТСТАЛА от дерева: пересоберите '
              u'python _tools/build_verification_index.py')
        return 1
    guard.write(OUT, page)
    print(u'записано: %s (%d байт)' % (OUT, len(page.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
