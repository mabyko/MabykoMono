#!/usr/bin/env python3
"""Small regression checks; no font tools or downloads required."""
import configparser
import io
import os
import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch

import fetch
import package_release
import test_outputs


ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for suffix in (".zip", ".tar.xz"):
            archive = root / f"source{suffix}"
            destination = root / f"extracted{suffix}"
            if suffix == ".zip":
                with zipfile.ZipFile(archive, "w") as output:
                    output.writestr("font.ttf", b"font")
                extractor = zipfile.ZipFile
            else:
                with tarfile.open(archive, "w:xz") as output:
                    entry = tarfile.TarInfo("font.ttf")
                    entry.size = 4
                    output.addfile(entry, io.BytesIO(b"font"))
                extractor = tarfile.TarFile

            def interrupted(self, path, *args, **kwargs):
                (Path(path) / "partial.ttf").write_bytes(b"incomplete")
                raise OSError("interrupted extraction")

            with patch.object(extractor, "extractall", interrupted):
                try:
                    fetch.unpack(archive, destination)
                except OSError:
                    pass
                else:
                    raise AssertionError("extraction failure was swallowed")
            assert not destination.exists()
            fetch.unpack(archive, destination)
            assert (destination / "font.ttf").read_bytes() == b"font"
            assert not (destination / "partial.ttf").exists()

        shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
        shutil.copyfile(ROOT / "pyproject.toml", root / "pyproject.toml")
        shutil.copytree(ROOT / "licenses", root / "licenses")
        config = configparser.ConfigParser()
        config.read(ROOT / "config.ini")
        config["fonts"]["output_root"] = "custom-fonts"
        with (root / "config.ini").open("w") as output:
            config.write(output)
        for dirname, prefix in test_outputs.VARIANTS:
            folder = root / "custom-fonts" / dirname
            folder.mkdir(parents=True)
            for style in test_outputs.STYLES:
                (folder / f"{prefix}-{style}.ttf").write_bytes(f"{prefix}-{style}".encode())
        with patch.object(package_release, "ROOT", root), patch.object(test_outputs, "ROOT", root):
            package_release.main()
            test_outputs.main()
            archives = {p: p.read_bytes() for p in (root / "out/release").glob("*.zip")}
            for font in (root / "custom-fonts").glob("*/*.ttf"):
                os.utime(font, (1800000000, 1800000000))
                font.chmod(0o600)
            package_release.main()
            assert all(p.read_bytes() == data for p, data in archives.items()), "ZIP depends on file metadata"
    print("ok: extraction recovery, custom output root, licenses, deterministic ZIPs")


if __name__ == "__main__":
    main()
