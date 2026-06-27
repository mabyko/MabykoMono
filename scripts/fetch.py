#!/usr/bin/env python3
import configparser
import shutil
import tarfile
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"


def fetch(url: str, dest: Path) -> None:
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"download {url}")
    with urllib.request.urlopen(url) as response, dest.open("wb") as file:
        shutil.copyfileobj(response, file)


def unpack_zip(archive: Path, dest: Path) -> None:
    if dest.exists():
        return
    print(f"extract {archive.name}")
    with zipfile.ZipFile(archive) as zip_file:
        zip_file.extractall(dest)


def unpack_tar_xz(archive: Path, dest: Path) -> None:
    if dest.exists():
        return
    print(f"extract {archive.name}")
    dest.mkdir(parents=True)
    with tarfile.open(archive, "r:xz") as tar:
        tar.extractall(dest, filter="data")


def main() -> None:
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    fonts = config["fonts"]

    SOURCES.mkdir(exist_ok=True)

    jb_zip = SOURCES / "JetBrainsMono-2.304.zip"
    fetch(fonts["jetbrains_mono_url"], jb_zip)
    unpack_zip(jb_zip, SOURCES / "JetBrainsMono-2.304")

    d2_zip = SOURCES / "D2Coding-Ver1.3.2-20180524.zip"
    fetch(fonts["d2coding_url"], d2_zip)
    unpack_zip(d2_zip, SOURCES / "D2Coding-Ver1.3.2-20180524")

    nf_tar = SOURCES / "NerdFontsSymbolsOnly-3.4.0.tar.xz"
    fetch(fonts["nerd_fonts_url"], nf_tar)
    unpack_tar_xz(nf_tar, SOURCES / "NerdFontsSymbolsOnly-3.4.0")


if __name__ == "__main__":
    main()
