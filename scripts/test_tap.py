#!/usr/bin/env python3
"""Check the Linux release workflow without network access or a tap checkout."""
import configparser
import hashlib
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = (
    ("font-mabyko-mono", "MabykoMono", "MabykoMono-v{version}.zip"),
    ("font-mabyko-mono-nf", "MabykoMonoNF", "MabykoMono_NF_v{version}.zip"),
    ("font-mabyko-mono-nl", "MabykoMonoNL", "MabykoMono_NL_v{version}.zip"),
    ("font-mabyko-mono-narrow", "MabykoMonoNarrow", "MabykoMono_Narrow_v{version}.zip"),
    ("font-mabyko-mono-narrow-nf", "MabykoMonoNarrowNF", "MabykoMono_Narrow_NF_v{version}.zip"),
    ("font-mabyko-mono-narrow-nl", "MabykoMonoNarrowNL", "MabykoMono_Narrow_NL_v{version}.zip"),
)


def main():
    config = configparser.ConfigParser()
    config.read(ROOT / "config.ini")
    version = config["fonts"]["version"]
    workflow = (ROOT / ".github/workflows/bump-tap.yml").read_text()
    step = workflow.split("      - name: Update casks\n", 1)[1]
    script = textwrap.dedent(step.split("        run: |\n", 1)[1].split("\n      - name:", 1)[0])
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "Casks").mkdir()
        (root / "bin").mkdir()
        (root / "assets").mkdir()
        for token, _, template in PACKAGES:
            name = template.format(version=version)
            (root / "assets" / name).write_bytes(name.encode())
            if "narrow" not in token:
                (root / "Casks" / f"{token}.rb").write_text('  version "0.4.0"\n  sha256 "old"\n')
        curl = root / "bin/curl"
        curl.write_text(f"#!{sys.executable}\n" + textwrap.dedent("""
            import os, sys
            from pathlib import Path
            name = sys.argv[-1].rsplit('/', 1)[-1]
            sys.stdout.buffer.write((Path(os.environ['TAP_TEST_ASSETS']) / name).read_bytes())
        """))
        curl.chmod(0o755)
        git = root / "bin/git"
        git.write_text("#!/bin/sh\nexit 0\n")
        git.chmod(0o755)
        runner = root / "update.sh"
        runner.write_text(script)
        env = {**os.environ, "TAG": f"v{version}", "PATH": f"{root / 'bin'}:{os.environ['PATH']}", "TAP_TEST_ASSETS": str(root / "assets")}
        subprocess.run(["bash", "-n", str(runner)], check=True)
        subprocess.run(["bash", str(runner)], cwd=root, env=env, check=True)
        for token, prefix, template in PACKAGES:
            name = template.format(version=version)
            cask = (root / "Casks" / f"{token}.rb").read_text()
            assert f'version "{version}"' in cask
            assert f'sha256 "{hashlib.sha256(name.encode()).hexdigest()}"' in cask
            if "narrow" in token:
                assert cask.startswith(f'cask "{token}" do\n')
                assert template.replace("{version}", "#{version}") in cask
                for style in ("Thin", "Light", "Regular", "Medium", "SemiBold", "Bold"):
                    assert f'font "{prefix}-{style}.ttf"' in cask
                assert cask.count('  font "') == 6
        marker = root / "Casks/font-mabyko-mono-narrow.rb"
        marker.write_text(marker.read_text() + "# existing recipe customization\n")
        before = {p: p.read_bytes() for p in (root / "Casks").glob("*.rb")}
        subprocess.run(["bash", str(runner)], cwd=root, env=env, check=True)
        assert all(p.read_bytes() == data for p, data in before.items()), "second run changed existing casks"
    print("ok: tap casks, archive URLs/hashes, six weights, repeat-run preservation")


if __name__ == "__main__":
    main()
