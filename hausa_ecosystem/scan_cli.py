import sys
from pathlib import Path

from hausa_ecosystem.code_checker import check_hausa_python, check_hausa_rust

SUPPORTED_SUFFIXES = (".hausa", ".hrust")


def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print("Kuskure: Yi amfani da: hausa-scan  ko  hausa-scan folder")
        return 1

    root = Path(args[0]) if args else Path.cwd()
    return scan_project(root)


def scan_project(root):
    if not root.exists():
        print(f"FAIL: Ba a sami folder ko fayil ba: {root}")
        return 1

    files = find_hausa_files(root)
    if not files:
        print(f"WARN: Ba a sami .hausa ko .hrust file a: {root}")
        return 0

    passed = 0
    failed = 0

    print(f"Ana binciken Hausa files a: {root}")
    for file_path in files:
        result = check_file(file_path)
        if result == 0:
            passed += 1
        else:
            failed += 1

    print("-----------------------")
    print(f"Sakamako: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


def find_hausa_files(root):
    if root.is_file():
        return [root] if root.suffix in SUPPORTED_SUFFIXES else []

    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix in SUPPORTED_SUFFIXES
        and not any(part.startswith(".") for part in path.parts)
    )


def check_file(file_path):
    if file_path.suffix == ".hausa":
        return check_hausa_python(file_path)
    if file_path.suffix == ".hrust":
        return check_hausa_rust(file_path)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
