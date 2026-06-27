#!/usr/bin/env python3
import configparser
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
def font_paths() -> list[Path]:
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    fonts = config["fonts"]
    return sorted((ROOT / fonts.get("output_root", "out/fonts")).glob("*/*.ttf"))


def advance(font, codepoint):
    cmap = font.getBestCmap()
    glyph = cmap[codepoint]
    return font["hmtx"][glyph][0]


def main() -> None:
    paths = font_paths()
    assert paths, "no fonts found"
    for font_file in paths:
        font = TTFont(font_file)
        half = advance(font, ord("0"))
        full = advance(font, ord("가"))
        assert full == half * 2, (font_file, half, full)
        for char in "A0a":
            assert advance(font, ord(char)) == half, (font_file, char)
        for char in "가힣ㄱＡ　":
            assert advance(font, ord(char)) == full, (font_file, char)
        names = font["name"]
        family_names = {
            record.toUnicode()
            for record in names.names
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
    print(f"ok: {len(paths)} fonts")


if __name__ == "__main__":
    main()
