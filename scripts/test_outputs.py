#!/usr/bin/env python3
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


def main() -> None:
    missing = [
        ROOT / "out" / "fonts" / dirname / f"{prefix}-{style}.ttf"
        for dirname, prefix in VARIANTS
        for style in STYLES
        if not (ROOT / "out" / "fonts" / dirname / f"{prefix}-{style}.ttf").exists()
    ]
    assert not missing, "missing outputs: " + ", ".join(str(path) for path in missing)
    print(f"ok: {len(STYLES) * len(VARIANTS)} outputs")


if __name__ == "__main__":
    main()
