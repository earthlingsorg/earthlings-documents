# -*- coding: utf-8 -*-
"""Приёмка одного хинди-документа за один вызов.

Собирает в один отчёт то, что для хинди приходится проверять всегда:
структуру против русского мастера, построчную парность (её требует
preflight_all.check_layout), поштучную сверку чисел, счёт полужирного,
несущие разделители ` - `, и блок проверок, специфичных для деванагари.

Почему деванагари нужен свой блок:
  - прекомпонованные буквы с нуктой U+0958..U+095F исключены из композиции,
    NFC раскладывает их на базовую букву плюс U+093C; если в корпусе окажутся
    оба написания, поиск и сравнение строк начнут врать МОЛЧА;
  - цифры деванагари U+0966..U+096F ломают поштучную сверку чисел и делают
    адреса контрактов, даты и проценты некопируемыми;
  - ZWNJ U+200C управляет полуформами и запрещён общим словарём корпуса:
    решение сессии - не использовать, и проверка это стережёт.

Отчёт пишется в _tools/_doc-report-hi.txt в UTF-8 и НЕ печатается в консоль:
русская консоль Windows работает в cp1251, деванагари в неё не кодируется, и
процесс умирает посреди отчёта.

Использование: python _tools/check_hi_doc.py 05
               python _tools/check_hi_doc.py manifest
"""
import io, os, re, sys, collections, subprocess, unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert os.path.isdir(os.path.join(REPO, 'ru')), REPO

NUM = sys.argv[1] if len(sys.argv) > 1 else None
assert NUM and (re.match(r'^\d\d$', NUM) or NUM == 'manifest'), \
    'укажите номер документа двумя цифрами или слово manifest'

OUT = os.path.join(REPO, '_tools', '_doc-report-hi.txt')

# Словари строим из ЧИСЛОВЫХ кодпойнтов: литералы молча портятся при передаче
# через heredoc и буфер обмена, и проверка потом «проходит» на сломанном
# словаре, ничего не находя.
FORBIDDEN = {
    0x2014: 'em-dash', 0x2013: 'en-dash', 0x2212: 'minus', 0x2026: 'ellipsis',
    0x201C: 'ldquo', 0x201D: 'rdquo', 0x201E: 'bdquo', 0x201F: 'quote',
    0x2018: 'lsquo', 0x2019: 'rsquo', 0x201A: 'sbquo', 0x201B: 'quote',
    0x2039: 'lsaquo', 0x203A: 'rsaquo',
    0x00A0: 'nbsp', 0x202F: 'narrow-nbsp', 0x2009: 'thin-space',
    0x2007: 'figure-space', 0x2008: 'punct-space', 0x200A: 'hair-space',
    0x200B: 'zwsp', 0x200C: 'zwnj', 0x2060: 'word-joiner', 0xFEFF: 'bom',
}
NUKTA_PRECOMPOSED = tuple(range(0x0958, 0x0960))
DEVA_DIGITS = tuple(range(0x0966, 0x0970))
DANDA, DOUBLE_DANDA = 0x0964, 0x0965
# Классы письма для проверки смешанных слов. Строим из кодпойнтов, а не из
# литералов диапазона: именно порча литерала эта проверка и ловит.
DEVA = chr(0x0900) + '-' + chr(0x097F)
CYR = chr(0x0400) + '-' + chr(0x04FF)


def find(lang):
    if NUM == 'manifest':
        p = os.path.join(REPO, '_manifest', '%s-manifest.md' % lang)
        return p if os.path.isfile(p) else None
    d = os.path.join(REPO, lang)
    if not os.path.isdir(d):
        return None
    for f in sorted(os.listdir(d)):
        if f.startswith(NUM + '-') and f.endswith('.md'):
            return os.path.join(d, f)
    return None


def read(p):
    return io.open(p, encoding='utf-8').read() if p else ''


def numbers(s):
    u"""Числовые токены. Латинские идентификаторы (0x-адреса) берём целиком,
    иначе адрес контракта распадётся на десяток ложных расхождений."""
    s = re.sub(r'0x[0-9a-fA-F]+', ' ', s)
    return collections.Counter(re.findall(r'\d+', s))


def main():
    rp, hp = find('ru'), find('hi')
    assert rp, u'нет русского мастера %s' % NUM
    assert hp, u'нет хинди-перевода %s' % NUM
    ru, hi = read(rp), read(hp)
    assert ru.strip(), u'пустой русский мастер на входе'
    assert hi.strip(), u'пустой хинди-файл на входе'

    o = [u'=== ДОКУМЕНТ %s: %s ===' % (NUM, os.path.basename(hp)), u'']
    fails = 0

    # 1. Структура блоков - зовём существующий скрипт, чтобы не заводить
    #    второй источник истины о том, что такое блок.
    if NUM != 'manifest':
        r = subprocess.run([sys.executable,
                            os.path.join(REPO, '_tools', 'check_translation.py'),
                            NUM, 'hi'],
                           capture_output=True)
        txt = (r.stdout or b'').decode('utf-8', 'replace').strip()
        o += [u'--- 1. СТРУКТУРА БЛОКОВ ---', txt or u'(пусто)', u'']
        if r.returncode:
            fails += 1
    else:
        o += [u'--- 1. СТРУКТУРА БЛОКОВ ---',
              u'Обращение через check_translation не проходит (оно вне корпуса)',
              u'']

    # 2. Построчная парность. Её требует preflight_all.check_layout, и она
    #    ловит выпавший или лишний абзац там, где сверка слов молчит.
    rl, hl = ru.split('\n'), hi.split('\n')
    ok = len(rl) == len(hl)
    o += [u'--- 2. ПОСТРОЧНАЯ ПАРНОСТЬ ---',
          u'  ru %d строк, hi %d строк - %s' % (len(rl), len(hl),
                                                u'ok' if ok else u'РАСХОЖДЕНИЕ')]
    if not ok:
        fails += 1
        # покажем первую строку, где разъехалась пустота: это почти всегда
        # склеенный или разорванный абзац
        for i in range(min(len(rl), len(hl))):
            if (not rl[i].strip()) != (not hl[i].strip()):
                o.append(u'  первое расхождение пустых строк: строка %d' % (i + 1))
                o.append(u'    ru: %s' % rl[i][:70])
                o.append(u'    hi: %s' % hl[i][:70])
                break
    o.append(u'')

    # 3. Числа поштучно. Цифра в правовом тексте есть норма.
    rn, hn = numbers(ru), numbers(hi)
    diff = []
    for k in sorted(set(rn) | set(hn), key=lambda x: (len(x), x)):
        if rn[k] != hn[k]:
            diff.append(u'%s: ru %d, hi %d' % (k, rn[k], hn[k]))
    o += [u'--- 3. ЧИСЛА ПОШТУЧНО ---',
          u'  токенов у ru %d, у hi %d, расхождений %d'
          % (sum(rn.values()), sum(hn.values()), len(diff))]
    o += [u'    ' + d for d in diff]
    if diff:
        fails += 1
    o.append(u'')

    # 4. Полужирный. Расхождение обычно значит, что выделенное слово
    #    растворилось в перифразе (карта опасных мест, G6).
    rb, hb = ru.count('**'), hi.count('**')
    o += [u'--- 4. ПОЛУЖИРНЫЙ ---',
          u'  ** у ru %d, у hi %d - %s' % (rb, hb,
                                           u'ok' if rb == hb else u'РАСХОЖДЕНИЕ'),
          u'']
    if rb != hb:
        fails += 1

    # 5. Несущий разделитель ` - `. В документах 04, 14 и 20 он держит разбор
    #    главной, а не типографику: данда здесь запрещена независимо от того,
    #    как правильнее по языку.
    rd, hd = ru.count(' - '), hi.count(' - ')
    o += [u'--- 5. РАЗДЕЛИТЕЛЬ " - " ---',
          u'  у ru %d, у hi %d%s' % (rd, hd,
                                     u'' if rd == hd else u'  <-- сверить вручную'),
          u'']

    # 6. Деванагари: то, чего нет ни у одного другого языка корпуса.
    o.append(u'--- 6. ДЕВАНАГАРИ ---')

    bad = collections.Counter()
    for ch in hi:
        c = ord(ch)
        if c in FORBIDDEN:
            bad[c] += 1
    if bad:
        fails += 1
        for c, n in sorted(bad.items()):
            o.append(u'  ДЕФЕКТ запрещённый знак U+%04X %s: %d'
                     % (c, FORBIDDEN[c], n))
    else:
        o.append(u'  запрещённая типографика: чисто')

    nk = [ch for ch in hi if ord(ch) in NUKTA_PRECOMPOSED]
    if nk:
        fails += 1
        o.append(u'  ДЕФЕКТ прекомпонованные нукты U+0958..U+095F: %d (%s)'
                 % (len(nk), u''.join(sorted(set(nk)))))
    else:
        o.append(u'  прекомпонованные нукты: ноль')

    dd = [ch for ch in hi if ord(ch) in DEVA_DIGITS]
    if dd:
        fails += 1
        o.append(u'  ДЕФЕКТ цифры деванагари: %d - корпус считает числа поштучно,'
                 u' и адреса должны копироваться' % len(dd))
    else:
        o.append(u'  цифры деванагари: ноль (числа набраны ASCII)')

    if hi != unicodedata.normalize('NFC', hi):
        fails += 1
        o.append(u'  ДЕФЕКТ текст не в NFC - сравнение строк начнёт врать молча')
    else:
        o.append(u'  нормализация NFC: ok')

    # Кириллица ВНУТРИ слова деванагари. Заведено 2026-08-26, после того как
    # проверка нашла двенадцать таких слов в файлах самой сессии - в словаре
    # решений, в конфигурации аудита и во фрагменте схемы.
    #
    # Ловится только машинно. Глазами не видно вовсе: и деванагари, и
    # кириллица одинаково «не латиница», а रि и ри в мелком кегле неразличимы.
    # Цена молчаливая и высокая: слово с кириллической буквой внутри не
    # находится ни поиском, ни заменой, ни этим же аудитом, - то есть замок,
    # написанный с такой опечаткой, не срабатывает никогда и печатает «чисто».
    #
    # Опасность именно у хинди, а не у грузинского или арабского: переводит
    # сессия, которая одновременно пишет по-русски, и раскладка переключается
    # посреди слова.
    mixed = re.findall('(?:[' + DEVA + ']+[' + CYR + ']|[' + CYR + ']['
                       + DEVA + ']+)', hi)
    if mixed:
        fails += 1
        # печатаем слово целиком и кодпойнты: без них правку не составить
        words = re.findall('[' + DEVA + CYR + '-]*[' + CYR + '][' + DEVA
                           + CYR + '-]*', hi)
        words = [w for w in words if re.search('[' + DEVA + ']', w)]
        o.append(u'  ДЕФЕКТ кириллица внутри слова деванагари: %d'
                 % len(set(words)))
        for w in sorted(set(words))[:12]:
            o.append(u'    %-24s %s' % (w, u' '.join(
                u'U+%04X%s' % (ord(c), u'*' if 0x0400 <= ord(c) <= 0x04FF
                               else u'') for c in w)))
        o.append(u'    (звёздочкой помечены кириллические знаки)')
    else:
        o.append(u'  кириллица внутри слов деванагари: ноль')

    o.append(u'  данда U+0964: %d, двойная данда U+0965: %d'
             % (hi.count(chr(DANDA)), hi.count(chr(DOUBLE_DANDA))))

    deva = len(re.findall('[' + chr(0x0900) + '-' + chr(0x097F) + ']', hi))
    o.append(u'  знаков деванагари: %d' % deva)
    if deva < 200:
        fails += 1
        o.append(u'  ДЕФЕКТ деванагари почти нет - файл не переведён?')
    o.append(u'')

    # 7. Латинские вкрапления. Английские глоссы законны, но обязаны стоять
    #    при ПЕРВОМ употреблении и в одном написании по всему корпусу.
    lat = collections.Counter(
        w for w in re.findall(r'[A-Za-z][A-Za-z-]{2,}', hi))
    o += [u'--- 7. ЛАТИНСКИЕ ВКРАПЛЕНИЯ ---',
          u'  разных слов %d, всего вхождений %d'
          % (len(lat), sum(lat.values()))]
    for w, n in lat.most_common(40):
        o.append(u'    %-28s %d' % (w, n))
    o.append(u'')

    o.append(u'=== ПРОВАЛЕНО ПРОВЕРОК: %d ===' % fails)

    io.open(OUT, 'w', encoding='utf-8').write(u'\n'.join(o) + u'\n')
    sys.stdout.write('report -> %s  (fails=%d)\n' % (OUT, fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
