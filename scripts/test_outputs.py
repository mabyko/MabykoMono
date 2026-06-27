#!/usr/bin/env python3
import configparser
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

    missing = [
        ROOT / "out" / "fonts" / dirname / f"{prefix}-{style}.ttf"
        for dirname, prefix in VARIANTS
        for style in STYLES
        if not (ROOT / "out" / "fonts" / dirname / f"{prefix}-{style}.ttf").exists()
    ]
    assert not missing, "missing outputs: " + ", ".join(str(path) for path in missing)

    release_dir = ROOT / "out" / "release"
    for dirname, prefix, zip_template in PACKAGES:
        zip_path = release_dir / zip_template.format(version=version)
        assert zip_path.exists(), f"missing package: {zip_path}"
        expected = sorted(f"{prefix}-{style}.ttf" for style in STYLES)
        with zipfile.ZipFile(zip_path) as archive:
            names = sorted(archive.namelist())
        assert names == expected, f"{zip_path}: {names} != {expected}"

    print(f"ok: {len(STYLES) * len(VARIANTS)} outputs and {len(PACKAGES)} packages")


if __name__ == "__main__":
    main()
