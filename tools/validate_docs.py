#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    ("README.md", "README.pt-BR.md"),
    ("CHANGELOG.md", "CHANGELOG.pt-BR.md"),
    ("CONTRIBUTING.md", "CONTRIBUTING.pt-BR.md"),
    ("SECURITY.md", "SECURITY.pt-BR.md"),
]

DOCS = ["README.md", "installation.md", "compatibility.md", "migration.md", "validation.md", "troubleshooting.md"]

def main() -> int:
    missing = []
    for left, right in PAIRS:
        if not (ROOT / left).is_file():
            missing.append(left)
        if not (ROOT / right).is_file():
            missing.append(right)
    for name in DOCS:
        if not (ROOT / "docs" / "en" / name).is_file():
            missing.append(f"docs/en/{name}")
        if not (ROOT / "docs" / "pt-BR" / name).is_file():
            missing.append(f"docs/pt-BR/{name}")
    if missing:
        print("Missing bilingual documentation: " + ", ".join(sorted(missing)), file=sys.stderr)
        return 1
    print("OK: bilingual documentation structure")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
