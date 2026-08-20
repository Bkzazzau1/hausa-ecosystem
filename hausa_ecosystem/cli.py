import argparse
import os
import sys
from pathlib import Path

from core.database import load_dictionary_from_db
from core.python_engine import english_to_hausa, hausa_to_english, run_hausa_code
from core.rust_engine import english_to_hrust, hrust_to_english, run_rust_code
from hausa_ecosystem import __version__
from hausa_ecosystem.api_checker import run_api_tests
from hausa_ecosystem.doctor import run_doctor
from hausa_ecosystem.project_generators import create_project, is_project_generator_request

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


def configure_output_encoding():
    """Use UTF-8 for Hausa characters on Windows terminals and subprocess pipes."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    configure_output_encoding()
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print_usage()
        return 1
    if args[0] == "help":
        args = ["--help", *args[1:]]
    # Preserve the old convenient ``hausa file.hausa`` form.
    if len(args) == 1 and Path(args[0]).suffix in (".hausa", ".hrust"):
        return run_legacy_file_command(args[0])
    parser = build_parser()
    try:
        parsed = parser.parse_args(args)
    except SystemExit as error:
        return int(error.code)
    if parsed.version:
        print(f"Hausa Ecosystem CLI {__version__}")
        return 0
    if parsed.command is None:
        parser.print_help()
        return 1
    if parsed.command == "doctor":
        return run_doctor([])
    if parsed.command == "keywords":
        return run_keywords_command([parsed.language], profile=parsed.profile)
    if parsed.command == "new":
        return run_new_command(parsed.parts)
    if parsed.command == "test-api":
        return run_api_tests([parsed.framework, parsed.base_url])
    if parsed.command == "check":
        from hausa_ecosystem.code_checker import run_check_command
        return run_check_command([parsed.file])
    if parsed.command == "scan":
        from hausa_ecosystem.scan_cli import scan_project
        return scan_project(Path(parsed.path))
    return run_command(
        parsed.command, parsed.file, output_file=getattr(parsed, "output", None),
        profile=getattr(parsed, "profile", "all"), verbose=getattr(parsed, "verbose", False),
        timeout=getattr(parsed, "timeout", 30),
    )


def build_parser():
    parser = argparse.ArgumentParser(prog="hausa", description="Hausa Python da Hausa Rust toolkit")
    parser.add_argument("-v", "--version", action="store_true", help="nuna version")
    sub = parser.add_subparsers(dest="command")
    run_parser = sub.add_parser("run", help="gudanar da .hausa ko .hrust")
    run_parser.add_argument("file")
    profile_choices = ("core", "builtins", "database", "web", "flask", "fastapi", "django", "all")
    run_parser.add_argument("--profile", choices=profile_choices, default="all")
    run_parser.add_argument("--timeout", type=positive_int, default=30)
    run_parser.add_argument("--verbose", action="store_true")
    for name in ("to-en", "to-ha"):
        item = sub.add_parser(name, help="fassara source code")
        item.add_argument("file")
        item.add_argument("-o", "--output")
        item.add_argument("--profile", choices=profile_choices, default="all")
    keywords = sub.add_parser("keywords")
    keywords.add_argument("language", choices=("python", "hausa", "rust", "hrust"))
    keywords.add_argument("--profile", choices=profile_choices, default="all")
    new = sub.add_parser("new")
    new.add_argument("parts", nargs="+")
    api = sub.add_parser("test-api")
    api.add_argument("framework", choices=("flask", "fastapi", "django"))
    api.add_argument("base_url")
    check = sub.add_parser("check")
    check.add_argument("file")
    scan = sub.add_parser("scan")
    scan.add_argument("path", nargs="?", default=".")
    sub.add_parser("doctor")
    return parser


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("dole lambar ta fi sifili")
    return number


def run_command(command, target_file, output_file=None, profile="all", verbose=False, timeout=30):
    _, extension = os.path.splitext(target_file)

    if command == "run":
        if output_file:
            print("Kuskure: Ba a amfani da -o tare da run.")
            return 1
        if extension == ".hausa":
            return run_hausa_code(target_file, profile=profile, verbose=verbose)
        if extension == ".hrust":
            return run_rust_code(target_file, timeout=timeout)
        print("Kuskure: Wannan nau'in fayil din bai dace ba. Yi amfani da .hausa ko .hrust")
        return 1

    if command == "to-en":
        content = read_target_file(target_file)
        if content is None:
            return 1
        if extension == ".hausa":
            try:
                return emit_translation(hausa_to_english(content, profile=profile), output_file)
            except ValueError as error:
                print(f"Kuskuren Fassara: {error}")
                return 1
        if extension == ".hrust":
            return emit_translation(hrust_to_english(content), output_file)
        print("Kuskure: Yi amfani da .hausa ko .hrust don to-en")
        return 1

    if command == "to-ha":
        content = read_target_file(target_file)
        if content is None:
            return 1
        if extension == ".py":
            try:
                return emit_translation(english_to_hausa(content, profile=profile), output_file)
            except ValueError as error:
                print(f"Kuskuren Fassara: {error}")
                return 1
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


def run_keywords_command(args, profile="all"):
    if len(args) != 1 or args[0] not in ("python", "hausa", "rust", "hrust"):
        print("Kuskure: Yi amfani da: hausa keywords python  ko  hausa keywords rust")
        return 1

    python_keywords, rust_keywords, _ = load_dictionary_from_db()
    selected = python_keywords if args[0] in ("python", "hausa") else rust_keywords
    if profile != "all":
        from core.dictionary import get_python_vocabulary, get_rust_vocabulary
        if args[0] in ("python", "hausa"):
            selected = get_python_vocabulary(profile)
        else:
            selected = get_rust_vocabulary("core" if profile != "all" else "all")

    for hausa_word, english_word in sorted(selected.items()):
        print(f"{hausa_word} -> {english_word}")
    return 0


def run_new_command(args):
    if is_project_generator_request(args):
        return create_project(args)

    if len(args) != 2 or args[0] not in STARTER_TEMPLATES:
        print("Kuskure: Yi amfani da: hausa new python app.hausa  ko  hausa new backend flask my_api")
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
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeError) as error:
        print(f"Kuskure: Ba a iya karanta fayil din {target_file}: {error}")
        return None


def print_usage():
    print("Yadda ake amfani da Shiri (Usage Guide):")
    print(f"  Version: Hausa Ecosystem CLI {__version__}")
    print("\nBASIC:")
    print("  Taimako:             hausa --help")
    print("  Version:             hausa --version")
    print("  Doctor:              hausa doctor")
    print("  Sabon Hausa Python:  hausa new python app.hausa")
    print("  Sabon Hausa Rust:    hausa new rust app.hrust")
    print("  Sabon Flask API:     hausa new backend flask my_api")
    print("  Sabon FastAPI API:   hausa new backend fastapi my_api")
    print("  Sabon Django App:    hausa new backend django my_site")
    print("  Sabon SQLite App:    hausa new database sqlite my_db_app")
    print("  Gwada API:           hausa test-api flask BASE_URL")
    print("  Keywords Python:     hausa keywords python")
    print("  Keywords Rust:       hausa keywords rust")
    print("\nPYTHON:")
    print("  Gudu da fayil:       hausa run templates/gwaji.hausa")
    print("  Hausa -> English:    hausa to-en templates/gwaji.hausa")
    print("  Hausa -> English -o: hausa to-en templates/gwaji.hausa -o output.py")
    print("  English -> Hausa:    hausa to-ha example.py")
    print("  English -> Hausa -o: hausa to-ha example.py -o output.hausa")
    print("\nRUST:")
    print("  Gudu da fayil:       hausa run templates/gwaji.hrust")
    print("  H-Rust -> English:   hausa to-en templates/gwaji.hrust")
    print("  H-Rust -> English -o:hausa to-en templates/gwaji.hrust -o output.rs")
    print("  Rust -> H-Rust:      hausa to-ha example.rs")
    print("  Rust -> H-Rust -o:   hausa to-ha example.rs -o output.hrust")


if __name__ == "__main__":
    raise SystemExit(main())
