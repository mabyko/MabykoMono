#!/usr/bin/env python3
import configparser
import hashlib
import shutil
import tarfile
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"


def fetch(url: str, dest: Path, sha256: str) -> None:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"download {url}")
        with urllib.request.urlopen(url) as response, dest.open("wb") as file:
            shutil.copyfileobj(response, file)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    if digest != sha256:
        dest.unlink()
        raise ValueError(f"{dest.name}: sha256 mismatch: {digest} != {sha256}")


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

    jb_zip = SOURCES / f"JetBrainsMono-{fonts['jetbrains_mono_version']}.zip"
    fetch(fonts["jetbrains_mono_url"], jb_zip, fonts["jetbrains_mono_sha256"])
    unpack_zip(jb_zip, jb_zip.with_suffix(""))

    d2_zip = SOURCES / f"D2Coding-Ver{fonts['d2coding_version']}-{fonts['d2coding_date']}.zip"
    fetch(fonts["d2coding_url"], d2_zip, fonts["d2coding_sha256"])
    unpack_zip(d2_zip, d2_zip.with_suffix(""))

    nf_tar = SOURCES / f"NerdFontsSymbolsOnly-{fonts['nerd_fonts_version']}.tar.xz"
    fetch(fonts["nerd_fonts_url"], nf_tar, fonts["nerd_fonts_sha256"])
    unpack_tar_xz(nf_tar, SOURCES / nf_tar.name.removesuffix(".tar.xz"))


if __name__ == "__main__":
    main()
