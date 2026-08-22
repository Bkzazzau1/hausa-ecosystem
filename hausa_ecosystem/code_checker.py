import shutil
import subprocess
import tempfile
from pathlib import Path

from core.python_engine import TranslationError, hausa_to_english
from core.rust_engine import hrust_to_english


CHECK_USAGE = "Kuskure: Yi amfani da: hausa check app.hausa  ko  hausa check app.hrust"


def run_check_command(args):
    if len(args) != 1:
        print(CHECK_USAGE)
        return 1

    source_path = Path(args[0])
    if not source_path.exists():
        print(f"FAIL: Ba a sami fayil ba: {source_path}")
        return 1

    if source_path.suffix == ".hausa":
        return check_hausa_python(source_path)

    if source_path.suffix == ".hrust":
        return check_hausa_rust(source_path)

    print("FAIL: Ana goyon bayan .hausa da .hrust kawai")
    return 1


def check_hausa_python(source_path):
    source = source_path.read_text(encoding="utf-8")
    try:
        translated = hausa_to_english(source)
    except TranslationError as error:
        print(f"FAIL: Kuskuren fassara: {error}")
        return 1

    try:
        compile(translated, str(source_path), "exec")
    except SyntaxError as error:
        print(f"FAIL: Kuskuren tsarin Python a layi {error.lineno}: {error.msg}")
        if error.text:
            print(error.text.strip())
        return 1

    print(f"PASS: {source_path} ta wuce binciken Hausa Python")
    return 0


def check_hausa_rust(source_path):
    rustc = shutil.which("rustc")
    if rustc is None:
        print("FAIL: Ba a sami rustc ba. Install Rust kafin binciken .hrust")
        return 1

    source = source_path.read_text(encoding="utf-8")
    translated = hrust_to_english(source)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "check.rs"
        output_path = Path(temp_dir) / "check_output"
        temp_path.write_text(translated, encoding="utf-8")

        result = subprocess.run(
            [rustc, str(temp_path), "-o", str(output_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    if result.returncode != 0:
        print(f"FAIL: Kuskuren Rust a cikin {source_path}")
        if result.stderr:
            print(result.stderr.strip())
        return 1

    print(f"PASS: {source_path} ta wuce binciken Hausa Rust")
    return 0
