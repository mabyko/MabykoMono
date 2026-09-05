#!/usr/bin/env python3
import configparser
import tomllib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STYLES = (
    "Thin",
    "Light",
    "Regular",
    "Medium",
    "SemiBold",
    "Bold",
)

VARIANTS = (
    ("standard-nf", "MabykoMonoNF"),
    ("standard", "MabykoMono"),
    ("standard-nl", "MabykoMonoNL"),
)

PACKAGES = (
    ("standard", "MabykoMono", "MabykoMono-v{version}.zip"),
    ("standard-nl", "MabykoMonoNL", "MabykoMono_NL_v{version}.zip"),
    ("standard-nf", "MabykoMonoNF", "MabykoMono_NF_v{version}.zip"),
)


def main() -> None:
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    version = config["fonts"]["version"]
    output_root = ROOT / config["fonts"].get("output_root", "out/fonts")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert version == project["project"]["version"], "project/font versions differ"

    missing = [
        output_root / dirname / f"{prefix}-{style}.ttf"
        for dirname, prefix in VARIANTS
        for style in STYLES
        if not (output_root / dirname / f"{prefix}-{style}.ttf").exists()
    ]
    assert not missing, "missing outputs: " + ", ".join(str(path) for path in missing)

    release_dir = ROOT / "out" / "release"
    for dirname, prefix, zip_template in PACKAGES:
        zip_path = release_dir / zip_template.format(version=version)
        assert zip_path.exists(), f"missing package: {zip_path}"
        font_names = [f"{prefix}-{style}.ttf" for style in STYLES]
        notices = ["LICENSE", "licenses/JetBrainsMono-OFL.txt", "licenses/D2Coding-OFL.txt", "licenses/NerdFonts-LICENSE.txt"]
        expected = sorted(font_names + notices)
        with zipfile.ZipFile(zip_path) as archive:
            names = sorted(archive.namelist())
            for name in font_names:
                assert archive.read(name) == (output_root / dirname / name).read_bytes()
            for name in notices:
                assert archive.read(name) == (ROOT / name).read_bytes()
        assert names == expected, f"{zip_path}: {names} != {expected}"

    print(f"ok: {len(STYLES) * len(VARIANTS)} outputs and {len(PACKAGES)} packages")


if __name__ == "__main__":
    main()
