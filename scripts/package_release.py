#!/usr/bin/env python3
import configparser
import os
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKAGES = (
    ("standard", "MabykoMono-v{version}.zip"),
    ("standard-nl", "MabykoMono_NL_v{version}.zip"),
    ("standard-nf", "MabykoMono_NF_v{version}.zip"),
)


def main() -> None:
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    fonts = config["fonts"]
    version = fonts["version"]
    output_root = ROOT / fonts.get("output_root", "out/fonts")
    release_dir = ROOT / "out" / "release"
    release_dir.mkdir(parents=True, exist_ok=True)

    for dirname, filename_template in PACKAGES:
        source_dir = output_root / dirname
        font_paths = sorted(source_dir.glob("*.ttf"))
        assert font_paths, f"no fonts found in {source_dir}"

        zip_path = release_dir / filename_template.format(version=version)
        tmp_path = zip_path.with_name(f".{zip_path.name}.{os.getpid()}.tmp")
        if tmp_path.exists():
            tmp_path.unlink()

        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for font_path in font_paths:
                archive.write(font_path, arcname=font_path.name)

        tmp_path.replace(zip_path)
        print(f"wrote {zip_path} ({len(font_paths)} fonts)")


if __name__ == "__main__":
    main()
