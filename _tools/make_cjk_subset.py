"""Печёт субсет Noto Serif SC для китайского PDF Обращения.

Зачем субсет, а не шрифт целиком. Noto Serif SC несёт около 65 тысяч глифов и
весит 25 МБ в переменном начертании; статические Regular и Bold дали бы
десятки мегабайт в публичном репозитории. В китайском Манифесте при этом
меньше пятисот уникальных иероглифов. Субсет из них весит примерно столько же,
сколько PT Serif, лежащий рядом.

Откуда берутся знаки. Из той же страницы _v2/zh/manifest.html, из которой
собирается сам PDF, - разбор вызывается функцией самого сборщика, чтобы набор
не разошёлся с текстом. Сверх текста добавлены ASCII целиком (адрес сайта,
номера страниц, слово Earthlings) и китайская пунктуация целиком: она стоит
копейки по весу, а её нехватка означала бы пустой квадрат посреди фразы.

Скрипт разовый: перезапускать нужно, только если в китайском Обращении
появился знак, которого в субсете нет. Сборщик PDF это заметит сам - он
сверяет каждый символ текста с таблицей шрифта и падает с перечнем недостающих.
Так и случилось при переименовании 2026-08-26: заголовок стал «致所有人», и знак
致 в субсете, испечённом по прежнему тексту, отсутствовал. Исходный шрифт для
этого нужно скачать заново - в репозитории его нет и не должно быть.

Запуск:  python _tools/make_cjk_subset.py <путь к NotoSerifSC[wght].ttf>
Выход:   _tools/fonts/NotoSerifSC-Regular.ttf и -Bold.ttf
"""

import importlib.util
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "fonts"

# Начертания. Курсива у иероглифов нет как явления - ровно как у грузинского
# мхедрули, - поэтому курсивные лица сборщик отобразит на прямые, а печь их
# отдельно незачем.
WEIGHTS = {"NotoSerifSC-Regular.ttf": 400, "NotoSerifSC-Bold.ttf": 700}


def manifesto_chars():
    """Символы китайского Манифеста - разбором самого сборщика, не копией."""
    spec = importlib.util.spec_from_file_location(
        "_mpdf", HERE / "build_manifesto_pdf.py")
    mod = importlib.util.module_from_spec(spec)
    saved = sys.argv
    sys.argv = ["build_manifesto_pdf.py", "zh"]
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = saved
    title, body, sign, cta = mod.parse_source()
    text = "".join([title, sign, cta] + body)
    assert len(text) > 500, "разбор страницы дал подозрительно мало текста"
    return set(text)


def wanted_codepoints():
    cps = {ord(c) for c in manifesto_chars()}
    # ASCII целиком: адрес earth-lings.org, номера страниц, слово Earthlings.
    cps |= set(range(0x20, 0x7F))
    # Пунктуация китайского письма целиком: CJK-знаки (U+3000-U+303F) и
    # полноширинные формы (U+FF00-U+FF65). Вместе это меньше двухсот глифов.
    cps |= set(range(0x3000, 0x3040))
    # С 0xFF01, а не с 0xFF00: сама позиция 0xFF00 в Unicode не занята.
    cps |= set(range(0xFF01, 0xFF66))
    # Тире 破折号 и двойные кавычки упрощённого письма - единственные знаки вне
    # ASCII, которые разрешены китайскому в check_translation.py.
    cps |= {0x2014, 0x201C, 0x201D}
    return cps


def bake(src, cps):
    OUT_DIR.mkdir(exist_ok=True)
    for name, wght in WEIGHTS.items():
        font = TTFont(src)
        # Переменный шрифт reportlab не понимает и берёт из него одно
        # начертание, отчего жирный стал бы неотличим от обычного. Печём
        # статические экземпляры, как это уже сделано для грузинского.
        static = instancer.instantiateVariableFont(
            font, {"wght": wght}, inplace=False, updateFontNames=True)
        opts = subset.Options()
        opts.name_IDs = ["*"]
        opts.name_legacy = True
        opts.notdef_outline = True
        sub = subset.Subsetter(options=opts)
        sub.populate(unicodes=cps)
        sub.subset(static)
        out = OUT_DIR / name
        static.save(out)
        have = set()
        for table in TTFont(out)["cmap"].tables:
            have |= set(table.cmap)
        missing = cps - have
        assert not missing, (
            "в субсете %s не хватает %d кодпойнтов: %s"
            % (name, len(missing), sorted(missing)[:20]))
        print("%s  %d КБ, глифов %d"
              % (name, out.stat().st_size // 1024, len(have)))


def main():
    assert len(sys.argv) == 2, __doc__.strip().splitlines()[-2].strip()
    src = Path(sys.argv[1])
    assert src.is_file(), "нет исходного шрифта: %s" % src
    cps = wanted_codepoints()
    print("нужно кодпойнтов: %d" % len(cps))
    bake(src, cps)


if __name__ == "__main__":
    sys.exit(main())
