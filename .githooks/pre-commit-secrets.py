# -*- coding: utf-8 -*-
"""Блокирует коммит, если в него попал секрет.

Проверяется не диск, а именно то, что лежит в индексе: файл может быть чистым
на диске и грязным в индексе, и наоборот. Публичные адреса контрактов и
SHA-256 не являются секретами и не флагуются - вместо этого ищутся приватные
ключи, токены, пароли и мнемоники.

Ложное срабатывание снимается переменной окружения:
    ALLOW_SECRET_COMMIT=1 git commit ...
Пользоваться ею только тогда, когда вы посмотрели на находку глазами.
"""
import re
import os
import subprocess
import sys

PATTERNS = [
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'приватный ключ PEM'),
    (r'\bAKIA[0-9A-Z]{16}\b', 'ключ AWS'),
    (r'\bgh[pousr]_[A-Za-z0-9]{20,}', 'токен GitHub'),
    (r'\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}', 'ключ модели'),
    (r'\bxox[baprs]-[A-Za-z0-9-]{10,}', 'токен Slack'),
    (r'\bre_[A-Za-z0-9_]{20,}', 'ключ Resend'),
    (r'\bey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}', 'JWT'),
    (r'(?i)\b(?:password|passwd|пароль)\s*[:=]\s*["\'`]?[A-Za-z0-9_+/=-]{12,}', 'пароль'),
    (r'(?i)\b(?:api[_ ]?key|secret[_ ]?key|ipn[_ ]?secret|access[_ ]?token)\s*[:=]\s*'
     r'["\'`]?[A-Za-z0-9_+/=-]{12,}', 'ключ или токен'),
    # «seed phrase» и «сид-фраза» ловятся только со значением после
    # двоеточия или равенства, как и mnemonic рядом. Голая пара слов
    # секретом не является: en/20-the-founding-period.md говорит, что
    # кошелёк Web3Auth создаётся БЕЗ неё, и любой коммит, трогавший этот
    # файл, останавливался. Настоящая мнемоника - двенадцать или
    # двадцать четыре слова, и слов «seed phrase» в ней нет.
    (r'(?i)\b(?:mnemonic|seed phrase|сид-фраза)\s*[:=]', 'мнемоника кошелька'),
    (r'(?i)\bprivate[_ ]?key\s*[:=]\s*["\'`]?[0-9a-fA-F]{40,}', 'приватный ключ hex'),
]
COMPILED = [(re.compile(p), name) for p, name in PATTERNS]

RISKY_NAME = re.compile(r'(?i)(\.env$|\.env\.|\.pem$|\.key$|\.p12$|\.pfx$|id_rsa|id_ed25519|'
                        r'\.htpasswd|keystore)')

# Метка, которой заменяются вынесенные значения: сама по себе не секрет.
MARKER = 'вынесено:'


def staged_files():
    """Имена берём через -z: иначе git экранирует кириллицу, и путь не открыть."""
    out = subprocess.run(['git', 'diff', '--cached', '--name-only', '-z', '--diff-filter=ACMR'],
                         capture_output=True)
    raw = out.stdout.decode('utf-8', 'replace')
    return [p for p in raw.split('\0') if p.strip()]


def staged_text(path):
    """Содержимое берём из индекса, а не с диска: коммитится именно оно."""
    out = subprocess.run(['git', 'show', ':' + path], capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout.decode('utf-8', 'replace')


def main():
    if os.environ.get('ALLOW_SECRET_COMMIT') == '1':
        print('pre-commit: проверка на секреты пропущена по ALLOW_SECRET_COMMIT=1')
        return 0

    files = staged_files()
    problems, unread = [], []
    for path in files:
        if RISKY_NAME.search(path):
            problems.append((path, 'опасное имя файла', path))
            continue
        text = staged_text(path)
        if text is None:
            unread.append(path)
            continue
        if not text:
            continue
        for rx, name in COMPILED:
            for m in rx.finditer(text):
                frag = m.group(0)
                if MARKER in text[max(0, m.start() - 40):m.end() + 40]:
                    continue                      # это метка, а не значение
                problems.append((path, name, frag[:60]))
                break

    # Проверка, которая молча прочитала ноль файлов, ничего не гарантирует.
    if files and unread:
        print('')
        print('  КОММИТ ОСТАНОВЛЕН: не удалось прочитать из индекса %d файл(ов)'
              % len(unread))
        for p in unread[:10]:
            print('    ', p)
        print('  Проверка на секреты не выполнена, а не пройдена.')
        print('')
        return 1

    if not problems:
        print('pre-commit: проверено файлов на секреты: %d' % len(files))
        return 0

    print('')
    print('  КОММИТ ОСТАНОВЛЕН: в индексе похоже на секрет')
    print('')
    for path, name, frag in problems:
        print('    %-52s %-24s %s' % (path[:52], name, frag))
    print('')
    print('  Что делать: убрать значение из файла, оставить имя переменной и')
    print('  отсылку на C:\\memory\\SECRETS.local.md. Значения живут в серверном')
    print('  .env, а не в документации.')
    print('')
    print('  Если это ложное срабатывание и вы посмотрели на него глазами:')
    print('      ALLOW_SECRET_COMMIT=1 git commit ...')
    print('')
    return 1


if __name__ == '__main__':
    sys.exit(main())
