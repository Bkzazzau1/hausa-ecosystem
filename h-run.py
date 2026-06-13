#!/usr/bin/env python3
# h-run.py
import os
import sys
from pathlib import Path

from core.database import load_dictionary_from_db
from core.python_engine import english_to_hausa, hausa_to_english, run_hausa_code
from core.rust_engine import english_to_hrust, hrust_to_english, run_rust_code

VERSION = "0.2.0"

STARTER_TEMPLATES = {
    "python": {
        "suffix": ".hausa",
        "content": '''# Hausa Python starter file
suna = "Bashir"
buga("Sannu", suna)

idan gaskiya:
    buga("Hausa Python yana aiki")
''',
    },
    "hausa": {
        "suffix": ".hausa",
        "content": '''# Hausa Python starter file
suna = "Bashir"
buga("Sannu", suna)

idan gaskiya:
    buga("Hausa Python yana aiki")
''',
    },
    "rust": {
        "suffix": ".hrust",
        "content": '''// Hausa Rust starter file
jama'a aiki main() {
    bari sauya kudi = 1000;
    kudi = kudi + 500;

    idan gaskiya {
        println!("Kudin dake asusunka shine: {}", kudi);
    }
}
''',
    },
    "hrust": {
        "suffix": ".hrust",
        "content": '''// Hausa Rust starter file
jama'a aiki main() {
    bari sauya kudi = 1000;
    kudi = kudi + 500;

    idan gaskiya {
        println!("Kudin dake asusunka shine: {}", kudi);
    }
}
''',
    },
}


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args[0] in ("-h", "--help", "help"):
        print_usage()
        return 0 if args else 1

    if args[0] in ("-v", "--version", "version"):
        print(f"Hausa Ecosystem CLI {VERSION}")
        return 0

    if args[0] == "keywords":
        return run_keywords_command(args[1:])

    if args[0] == "new":
        return run_new_command(args[1:])

    # Modern output mode:
    #   python h-run.py to-en input.hausa -o output.py
    #   python h-run.py to-ha input.py -o output.hausa
    if len(args) == 4 and args[2] == "-o" and args[0] in ("to-en", "to-ha"):
        return run_command(args[0], args[1], output_file=args[3])

    # Legacy support:
    #   python h-run.py --translate file.hausa
    #   python h-run.py file.hausa --translate
    #   python h-run.py file.hausa -o output.py
    if len(args) == 2 and args[0] == "--translate":
        return run_command("to-en", args[1])

    if len(args) == 2 and args[1] == "--translate":
        return run_command("to-en", args[0])

    if len(args) == 3 and args[1] in ("--translate", "-o"):
        return run_legacy_option_command(args[0], args[1], args[2])

    if len(args) >= 2:
        return run_command(args[0], args[1])

    if len(args) == 1:
        return run_legacy_file_command(args[0])

    print_usage()
    return 1


def run_command(command, target_file, output_file=None):
    _, extension = os.path.splitext(target_file)

    if command == "run":
        if output_file:
            print("Kuskure: Ba a amfani da -o tare da run.")
            return 1
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
            return emit_translation(hausa_to_english(content), output_file)
        if extension == ".hrust":
            return emit_translation(hrust_to_english(content), output_file)
        print("Kuskure: Yi amfani da .hausa ko .hrust don to-en")
        return 1

    if command == "to-ha":
        content = read_target_file(target_file)
        if content is None:
            return 1
        if extension == ".py":
            return emit_translation(english_to_hausa(content), output_file)
        if extension == ".rs":
            return emit_translation(english_to_hrust(content), output_file)
        print("Kuskure: Yi amfani da .py ko .rs don to-ha")
        return 1

    print_usage()
    return 1


def emit_translation(translated_text, output_file=None):
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(translated_text, encoding="utf-8")
        print(f"An rubuta: {output_path}")
        return 0

    print(translated_text)
    return 0


def run_keywords_command(args):
    if len(args) != 1 or args[0] not in ("python", "hausa", "rust", "hrust"):
        print("Kuskure: Yi amfani da: python h-run.py keywords python  ko  python h-run.py keywords rust")
        return 1

    python_keywords, rust_keywords, _ = load_dictionary_from_db()
    selected = python_keywords if args[0] in ("python", "hausa") else rust_keywords

    for hausa_word, english_word in sorted(selected.items()):
        print(f"{hausa_word} -> {english_word}")
    return 0


def run_new_command(args):
    if len(args) != 2 or args[0] not in STARTER_TEMPLATES:
        print("Kuskure: Yi amfani da: python h-run.py new python app.hausa  ko  python h-run.py new rust app.hrust")
        return 1

    language, output_file = args
    template = STARTER_TEMPLATES[language]
    output_path = Path(output_file)

    if output_path.suffix != template["suffix"]:
        print(f"Kuskure: Fayil din {language} yana bukatar karshen {template['suffix']}")
        return 1

    if output_path.exists():
        print(f"Kuskure: Fayil din ya riga ya wanzu: {output_path}")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template["content"], encoding="utf-8")
    print(f"An kirkiro sabon fayil: {output_path}")
    return 0


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

    return emit_translation(translated, option_value)


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
        return Path(target_file).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Kuskure: Ba a sami fayil din ba a: {target_file}")
        return None


def print_usage():
    print("Yadda ake amfani da Shiri (Usage Guide):")
    print(f"  Version: Hausa Ecosystem CLI {VERSION}")
    print("\nBASIC:")
    print("  Taimako:             python h-run.py --help")
    print("  Version:             python h-run.py --version")
    print("  Sabon Hausa Python:  python h-run.py new python app.hausa")
    print("  Sabon Hausa Rust:    python h-run.py new rust app.hrust")
    print("  Keywords Python:     python h-run.py keywords python")
    print("  Keywords Rust:       python h-run.py keywords rust")
    print("\nPYTHON:")
    print("  Gudu da fayil:       python h-run.py run templates/gwaji.hausa")
    print("  Hausa -> English:    python h-run.py to-en templates/gwaji.hausa")
    print("  Hausa -> English -o: python h-run.py to-en templates/gwaji.hausa -o output.py")
    print("  English -> Hausa:    python h-run.py to-ha example.py")
    print("  English -> Hausa -o: python h-run.py to-ha example.py -o output.hausa")
    print("\nRUST:")
    print("  Gudu da fayil:       python h-run.py run templates/gwaji.hrust")
    print("  H-Rust -> English:   python h-run.py to-en templates/gwaji.hrust")
    print("  H-Rust -> English -o:python h-run.py to-en templates/gwaji.hrust -o output.rs")
    print("  Rust -> H-Rust:      python h-run.py to-ha example.rs")
    print("  Rust -> H-Rust -o:   python h-run.py to-ha example.rs -o output.hrust")


if __name__ == "__main__":
    raise SystemExit(main())
