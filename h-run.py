#!/usr/bin/env python3
# h-run.py
import os
import sys
from pathlib import Path

from core.python_engine import english_to_hausa, hausa_to_english, run_hausa_code
from core.rust_engine import english_to_hrust, hrust_to_english, run_rust_code


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--translate":
        return run_command("to-en", sys.argv[2])

    if len(sys.argv) == 3 and sys.argv[2] == "--translate":
        return run_command("to-en", sys.argv[1])

    if len(sys.argv) == 4 and sys.argv[2] in ("--translate", "-o"):
        return run_legacy_option_command(sys.argv[1], sys.argv[2], sys.argv[3])

    if len(sys.argv) >= 3:
        return run_command(sys.argv[1], sys.argv[2])

    if len(sys.argv) == 2:
        return run_legacy_file_command(sys.argv[1])

    print_usage()
    return 1


def run_command(command, target_file):
    _, extension = os.path.splitext(target_file)

    if command == "run":
        if extension == ".hausa":
            return run_hausa_code(target_file)
        if extension == ".hrust":
            return run_rust_code(target_file)
        print("Kuskure: Wannan nau'in fayil din bai dace ba. Yi amfani da .hausa ko .hrust")
        return 1

    if command == "to-en":
        content = read_target_file(target_file)
        if content is None:
            return 1
        if extension == ".hausa":
            print(hausa_to_english(content))
            return 0
        if extension == ".hrust":
            print(hrust_to_english(content))
            return 0
        print("Kuskure: Yi amfani da .hausa ko .hrust don to-en")
        return 1

    if command == "to-ha":
        content = read_target_file(target_file)
        if content is None:
            return 1
        if extension == ".py":
            print(english_to_hausa(content))
            return 0
        if extension == ".rs":
            print(english_to_hrust(content))
            return 0
        print("Kuskure: Yi amfani da .py ko .rs don to-ha")
        return 1

    print_usage()
    return 1


def run_legacy_file_command(target_file):
    source_path = Path(target_file)
    if not source_path.exists():
        print(f"Ba a sami fayil ba: {source_path}", file=sys.stderr)
        return 1

    if source_path.suffix == ".hausa":
        return run_hausa_code(str(source_path))
    if source_path.suffix == ".hrust":
        return run_rust_code(str(source_path))

    print("Ana goyon bayan .hausa da .hrust kawai.", file=sys.stderr)
    return 1


def run_legacy_option_command(target_file, option, option_value):
    source_path = Path(target_file)
    if option == "--translate":
        return run_command("to-en", target_file)

    translated = translate_by_extension(source_path)
    if translated is None:
        return 1

    Path(option_value).write_text(translated, encoding="utf-8")
    print(f"An rubuta: {option_value}")
    return 0


def translate_by_extension(source_path):
    if not source_path.exists():
        print(f"Ba a sami fayil ba: {source_path}", file=sys.stderr)
        return None

    content = source_path.read_text(encoding="utf-8")
    if source_path.suffix == ".hausa":
        return hausa_to_english(content)
    if source_path.suffix == ".hrust":
        return hrust_to_english(content)

    print("Ana goyon bayan .hausa da .hrust kawai.", file=sys.stderr)
    return None


def read_target_file(target_file):
    try:
        return Path(target_file).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Kuskure: Ba a sami fayil din ba a: {target_file}")
        return None


def print_usage():
    print("Yadda ake amfani da Shiri (Usage Guide):")
    print("\nPYTHON:")
    print("  Gudu da fayil:       python h-run.py run templates/gwaji.hausa")
    print("  Hausa -> English:    python h-run.py to-en templates/gwaji.hausa")
    print("  English -> Hausa:    python h-run.py to-ha example.py")
    print("\nRUST:")
    print("  Gudu da fayil:       python h-run.py run templates/gwaji.hrust")
    print("  H-Rust -> English:   python h-run.py to-en templates/gwaji.hrust")
    print("  Rust -> H-Rust:      python h-run.py to-ha example.rs")


if __name__ == "__main__":
    raise SystemExit(main())
