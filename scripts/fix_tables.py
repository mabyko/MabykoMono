#!/usr/bin/env python3
import configparser
import re
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
def font_paths() -> list[Path]:
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    fonts = config["fonts"]
    return sorted((ROOT / fonts.get("output_root", "out/fonts")).glob("*/*.ttf"))


def font_revision(version: str) -> float:
    """Encode MAJOR.MINOR.PATCH as MAJOR.MMpp in a signed 16.16 field."""
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        raise ValueError(f"expected a stable MAJOR.MINOR.PATCH version: {version}")
    major, minor, patch = map(int, version.split("."))
    if major > 32767 or minor > 99 or patch > 99:
        raise ValueError("font revision supports major <= 32767 and minor/patch <= 99")
    # Integer arithmetic avoids float-dependent rounding before serialization.
    decimal_units = major * 10000 + minor * 100 + patch
    fixed_units = (decimal_units * 65536 + 5000) // 10000
    return fixed_units / 65536


def advance(font, codepoint):
    cmap = font.getBestCmap()
    return font["hmtx"][cmap[codepoint]][0]


def main() -> None:
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    revision = font_revision(config["fonts"]["version"])
    # OpenType timestamps count seconds since 1904, not the Unix epoch.
    timestamp = config["fonts"].getint("source_date_epoch") + 2082844800
    for font_file in font_paths():
        font = TTFont(font_file, recalcTimestamp=False)
        half_width = advance(font, ord("0"))

        font["OS/2"].xAvgCharWidth = half_width
        font["post"].isFixedPitch = 1
        font["hhea"].advanceWidthMax = max(width for width, _ in font["hmtx"].metrics.values())
        font["head"].fontRevision = revision
        font["head"].created = font["head"].modified = timestamp
        if "FFTM" in font:
            del font["FFTM"]  # FontForge's build timestamps are not needed by renderers.

        font.save(font_file)
        print(f"fixed {font_file.name}: xAvgCharWidth={half_width}, isFixedPitch=1, fontRevision={revision}")


if __name__ == "__main__":
    main()
