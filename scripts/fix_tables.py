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
    return font["hmtx"][cmap[codepoint]][0]


def main() -> None:
    for font_file in font_paths():
        font = TTFont(font_file)
        half_width = advance(font, ord("0"))

        font["OS/2"].xAvgCharWidth = half_width
        font["post"].isFixedPitch = 1
        font["hhea"].advanceWidthMax = max(width for width, _ in font["hmtx"].metrics.values())

        font.save(font_file)
        print(f"fixed {font_file.name}: xAvgCharWidth={half_width}, isFixedPitch=1")


if __name__ == "__main__":
    main()
