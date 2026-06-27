#!/usr/bin/env fontforge -script
import configparser
from pathlib import Path

import fontforge
import psMat


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"

HANGUL_RANGES = (
    (0x3131, 0x318E),
    (0xAC00, 0xD7A3),
)
FULLWIDTH_RANGES = (
    (0x3000, 0x3000),
    (0xFF01, 0xFF60),
    (0xFFE0, 0xFFE6),
)
NERD_RANGES = (
    (0xE000, 0xF8FF),
    (0xF0000, 0xFFFFD),
    (0x100000, 0x10FFFD),
)
STYLES = (
    ("Thin", 100),
    ("Light", 300),
    ("Regular", 400),
    ("Medium", 500),
    ("SemiBold", 600),
    ("Bold", 700),
)
VARIANTS = (
    {
        "dirname": "standard-nf",
        "family": "Mabyko Mono NF",
        "prefix": "MabykoMonoNF",
        "pattern_key": "jetbrains_mono_pattern",
        "nerd": True,
    },
    {
        "dirname": "standard",
        "family": "Mabyko Mono",
        "prefix": "MabykoMono",
        "pattern_key": "jetbrains_mono_pattern",
        "nerd": False,
    },
    {
        "dirname": "standard-nl",
        "family": "Mabyko Mono NL",
        "prefix": "MabykoMonoNL",
        "pattern_key": "jetbrains_mono_nl_pattern",
        "nerd": False,
    },
)


def in_ranges(codepoint, ranges):
    return any(start <= codepoint <= end for start, end in ranges)


def center_width(glyph, width):
    old_width = glyph.width
    if old_width > 0 and old_width != width:
        glyph.transform(psMat.translate((width - old_width) / 2, 0))
    glyph.width = width


def scale_to_width(glyph, width):
    old_width = glyph.width
    if old_width > 0 and old_width != width:
        glyph.transform(psMat.scale(width / old_width, 1))
    glyph.width = width


def unlink(font):
    font.selection.all()
    font.unlinkReferences()
    font.selection.none()


def keep_only(font, ranges):
    for glyph in list(font.glyphs()):
        codepoint = glyph.unicode
        if codepoint < 0 or not in_ranges(codepoint, ranges):
            glyph.clear()


def clear_ranges(font, ranges):
    font.selection.none()
    for start, end in ranges:
        font.selection.select(("more", "ranges"), start, end)
    for glyph in font.selection.byGlyphs:
        glyph.clear()
    font.selection.none()


def ensure_blank_fullwidth(font, ranges, width):
    for start, end in ranges:
        for codepoint in range(start, end + 1):
            glyph = font.createChar(codepoint)
            if not glyph.isWorthOutputting():
                glyph.width = width


def suffix_glyph_names(font, suffix):
    seen = set()
    for glyph in font.glyphs():
        name = f"{glyph.glyphname}{suffix}"
        if name in seen:
            name = f"{name}-{glyph.encoding}"
        glyph.glyphname = name
        seen.add(name)


def merge_subset(base, source, ranges, width, path):
    unlink(source)
    keep_only(source, ranges)
    for glyph in source.glyphs():
        if glyph.isWorthOutputting() and glyph.unicode >= 0:
            center_width(glyph, width)
    source.generate(str(path))
    clear_ranges(base, ranges)
    base.mergeFonts(str(path))


def set_names(font, family, style, weight, version, half_width, full_width):
    font.familyname = family
    font.fontname = family.replace(" ", "") + f"-{style}"
    font.fullname = family + f" {style}"
    font.weight = style
    font.os2_weight = weight
    font.os2_width = 5
    font.os2_vendor = "MBYK"
    font.os2_typolinegap = 0
    font.hhea_linegap = 0
    font.os2_panose = (2, 11, 5, 9, 2, 2, 3, 2, 2, 7)
    font.comment = f"{family}: half width {half_width}, full width {full_width}"
    font.copyright = (
        "Mabyko Mono is derived from JetBrains Mono, D2Coding, and Nerd Fonts. "
        "All font software is licensed under the SIL Open Font License 1.1."
    )
    font.sfnt_names = (
        ("English (US)", "Family", family),
        ("English (US)", "SubFamily", style),
        ("English (US)", "Fullname", family + f" {style}"),
        ("English (US)", "Preferred Family", family),
        ("English (US)", "Preferred Styles", style),
        ("English (US)", "Compatible Full", family + f" {style}"),
        ("English (US)", "UniqueID", f"{family} {style} {version}"),
        ("English (US)", "Version", f"Version {version}"),
        ("English (US)", "License", "SIL Open Font License, Version 1.1"),
        ("English (US)", "License URL", "https://openfontlicense.org"),
    )


def build_style(fonts, variant, style, weight, half_width, full_width, output_dir):
    jb_path = ROOT / fonts.get(variant["pattern_key"]).format(style=style)
    d2_key = "d2coding_bold" if weight >= 600 else "d2coding_regular"
    jb = fontforge.open(str(jb_path))
    d2 = fontforge.open(str(ROOT / fonts[d2_key]))

    jb.em = d2.em

    source_half = int(jb[0x0030].width)

    unlink(jb)
    for glyph in jb.glyphs():
        if glyph.isWorthOutputting() and glyph.width > 0:
            cells = max(1, round(glyph.width / source_half))
            scale_to_width(glyph, half_width * cells)

    merge_subset(
        jb,
        d2,
        HANGUL_RANGES + FULLWIDTH_RANGES,
        full_width,
        BUILD / f"d2-subset-{style}.ttf",
    )
    ensure_blank_fullwidth(jb, HANGUL_RANGES + FULLWIDTH_RANGES, full_width)

    if variant["nerd"]:
        nf = fontforge.open(str(ROOT / fonts["nerd_fonts_regular"]))
        nf.em = d2.em
        keep_only(nf, NERD_RANGES)
        suffix_glyph_names(nf, "-nf")
        for glyph in nf.glyphs():
            if glyph.isWorthOutputting() and glyph.unicode >= 0:
                center_width(glyph, half_width)
        nf_path = BUILD / f"nerd-subset-{variant['dirname']}-{style}.ttf"
        nf.generate(str(nf_path))
        clear_ranges(jb, NERD_RANGES)
        jb.mergeFonts(str(nf_path))
        nf.close()

    d2.close()
    set_names(jb, variant["family"], style, weight, fonts["version"], half_width, full_width)
    jb.generate(str(output_dir / f"{variant['prefix']}-{style}.ttf"))
    jb.close()


def main():
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    fonts = config["fonts"]
    output_root = ROOT / fonts.get("output_root", "out/fonts")

    BUILD.mkdir(exist_ok=True)

    d2 = fontforge.open(str(ROOT / fonts["d2coding_regular"]))

    source_full_width = int(d2[0xAC00].width or d2[0x3000].width)
    d2.close()
    full_width = int(fonts.get("full_width", source_full_width))
    half_width = int(fonts.get("half_width", full_width // 2))
    if full_width != half_width * 2:
        raise ValueError("full_width must be exactly twice half_width")

    for variant in VARIANTS:
        output_dir = output_root / variant["dirname"]
        output_dir.mkdir(parents=True, exist_ok=True)
        for style, weight in STYLES:
            build_style(fonts, variant, style, weight, half_width, full_width, output_dir)


if __name__ == "__main__":
    main()
