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
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    # OpenType timestamps count seconds since 1904, not the Unix epoch.
    timestamp = config["fonts"].getint("source_date_epoch") + 2082844800
    for font_file in font_paths():
        font = TTFont(font_file, recalcTimestamp=False)
        half_width = advance(font, ord("0"))

        font["OS/2"].xAvgCharWidth = half_width
        font["post"].isFixedPitch = 1
        font["hhea"].advanceWidthMax = max(width for width, _ in font["hmtx"].metrics.values())
        font["head"].created = font["head"].modified = timestamp
        if "FFTM" in font:
            del font["FFTM"]  # FontForge's build timestamps are not needed by renderers.

        font.save(font_file)
        print(f"fixed {font_file.name}: xAvgCharWidth={half_width}, isFixedPitch=1")


if __name__ == "__main__":
    main()
