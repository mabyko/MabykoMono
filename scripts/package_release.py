#!/usr/bin/env python3
import configparser
import os
import time
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
    timestamp = time.gmtime(fonts.getint("source_date_epoch"))[:6]
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
            for path in [*font_paths, ROOT / "LICENSE", *sorted((ROOT / "licenses").glob("*.txt"))]:
                name = f"licenses/{path.name}" if path.parent.name == "licenses" else path.name
                entry = zipfile.ZipInfo(name, date_time=timestamp)
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)

        tmp_path.replace(zip_path)
        print(f"wrote {zip_path} ({len(font_paths)} fonts)")


if __name__ == "__main__":
    main()
