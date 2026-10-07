#!/usr/bin/env python3
"""Check release revision encoding, including patch and minor rollovers."""
from fix_tables import font_revision


def main() -> None:
    assert font_revision("0.5.1") == 3283 / 65536
    versions = [f"0.{minor}.{patch}" for minor in range(100) for patch in range(100)]
    revisions = [font_revision(version) for version in versions]
    assert all(a < b for a, b in zip(revisions, revisions[1:])), "release revisions collide or go backwards"
    assert revisions[-1] < font_revision("1.0.0")
    assert font_revision("0.5.9") < font_revision("0.5.10") < font_revision("0.6.0")
    assert font_revision("32767.99.99") * 65536 <= 2147483647
    for version in ("0.5", "0.5.1-rc.1", "0.5.1+build", "00.5.1", "-1.0.0", "0.100.0", "0.5.100", "32768.0.0"):
        try:
            font_revision(version)
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsupported version was accepted: {version}")
    print("ok: font revisions preserve release order and patch versions within 16.16 limits")


if __name__ == "__main__":
    main()
