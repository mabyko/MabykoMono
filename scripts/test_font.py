#!/usr/bin/env python3
import re
import configparser
import subprocess
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
def font_paths() -> list[Path]:
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    fonts = config["fonts"]
    return sorted((ROOT / fonts.get("output_root", "out/fonts")).glob("*/*.ttf"))


FONTS = font_paths()


def advance(font, codepoint):
    cmap = font.getBestCmap()
    glyph = cmap[codepoint]
    return font["hmtx"][glyph][0]


def assert_range(font, start, end, width):
    cmap = font.getBestCmap()
    missing = [cp for cp in range(start, end + 1) if cp not in cmap]
    assert not missing, f"missing glyphs: U+{missing[0]:04X}.. ({len(missing)})"
    wrong = [cp for cp in range(start, end + 1) if advance(font, cp) != width]
    assert not wrong, f"wrong width: U+{wrong[0]:04X}={advance(font, wrong[0])}"


def hb_advances(font_file, text):
    output = subprocess.check_output(
        ["hb-shape", str(font_file), text],
        text=True,
    )
    return [int(value) for value in re.findall(r"\+(-?\d+)", output)]


def hb_shape(font_file, text):
    return subprocess.check_output(
        ["hb-shape", str(font_file), text],
        text=True,
    )


def main() -> None:
    assert FONTS, "no fonts found"
    for font_file in FONTS:
        font = TTFont(font_file)
        half = advance(font, ord("0"))
        full = advance(font, ord("가"))

        assert half > 0
        assert full == half * 2

        assert_range(font, 0x3131, 0x318E, full)
        assert_range(font, 0xAC00, 0xD7A3, full)
        assert_range(font, 0xFF01, 0xFF60, full)
        assert_range(font, 0xFFE0, 0xFFE6, full)
        assert advance(font, 0x3000) == full
        has_nerd = font_file.parent.name.endswith("-nf")
        if has_nerd:
            assert advance(font, 0xE0B0) == half
            powerline = font["glyf"][font.getBestCmap()[0xE0B0]]
            assert (powerline.xMin, powerline.xMax) == (0, half), (
                "powerline must fill the cell",
                powerline.xMin,
                powerline.xMax,
            )
        if 0x2665 in font.getBestCmap():
            assert not font.getBestCmap()[0x2665].endswith("-nf")

        family_names = {
            record.toUnicode()
            for record in font["name"].names
            if record.nameID in {1, 16}
        }
        assert any(name.startswith("Mabyko Mono") for name in family_names), (
            font_file,
            family_names,
        )

        assert font["post"].isFixedPitch == 1
        assert font["OS/2"].xAvgCharWidth == half
        assert font["hhea"].advanceWidthMax == max(
            width for width, _ in font["hmtx"].metrics.values()
        )

        assert hb_advances(font_file, "aaaaaaaaaa") == [half] * 10
        assert hb_advances(font_file, "가가가가가") == [full] * 5
        if has_nerd:
            assert hb_advances(font_file, "a가Ａ\ue0b0") == [half, full, full, half]
        else:
            assert hb_advances(font_file, "a가Ａ") == [half, full, full]
        shaped_equals = hb_shape(font_file, "===")
        if font_file.parent.name.endswith("-nl"):
            assert ".liga" not in shaped_equals, (font_file, shaped_equals)
        else:
            assert ".liga" in shaped_equals, (font_file, shaped_equals)

        fc_scan = subprocess.check_output(
            ["fc-scan", "--format", "%{family}\\n%{style}\\n", str(font_file)],
            text=True,
        )
        assert "Mabyko Mono" in fc_scan

    print(f"ok: {len(FONTS)} fonts coverage, metrics, HarfBuzz shaping, fontconfig")


if __name__ == "__main__":
    main()
