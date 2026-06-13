# build_offline_bundle.py
import shutil
from pathlib import Path


EXTENSION_NAME = "vscode-hausa"


def deploy_school_lab_bundle():
    print("=" * 60)
    print("PERA-X ECOSYSTEM: OFFLINE SCHOOL LAB AUTOMATED INSTALLER")
    print("=" * 60 + "\n")

    root_dir = Path.cwd()
    source_extension = root_dir / "extensions" / EXTENSION_NAME

    if not source_extension.exists():
        print("KUSKURE: Ba a sami fayilolin ektenshan dake kan USB ba!")
        print("Tabbatar kana gudanar da wannan shirin daga cikin babban fashin dake kan flash drive dinka.")
        return 1

    user_home = Path.home()
    vscode_extensions_path = user_home / ".vscode" / "extensions"
    target_extension_destination = vscode_extensions_path / EXTENSION_NAME

    print("Mataki na 1: Ana girka ektenshan na Hausa-Python & Rust a cikin VS Code...")
    print(f"   - Daga: {source_extension}")
    print(f"   - Zuwa: {target_extension_destination}")

    if not is_expected_extension_target(target_extension_destination, vscode_extensions_path):
        print("   Kuskure: Target path bai dace da VS Code extension folder ba.")
        return 1

    try:
        vscode_extensions_path.mkdir(parents=True, exist_ok=True)

        if target_extension_destination.exists():
            print("   - An gano tsohon tsarin ektenshan, ana share shi don sabuntawa...")
            shutil.rmtree(target_extension_destination)

        shutil.copytree(source_extension, target_extension_destination)
        print("   An tura ektenshan na VS Code cikin nasara!")
    except Exception as exc:
        print(f"   Kuskure yayin tura ektenshan na VS Code: {exc}")
        return 1

    print("\n" + "-" * 60)
    print("AN GAMA GIRKA SHIRIN LAB LAFIYALAU!")
    print("Uku daga cikin muhimman abubuwan dake gaba:")
    print("  1. Rufe sannan ka sake bude dukkan windows na VS Code.")
    print("  2. Dalibai za su iya rubuta lambobi a cikin '.hausa' ko '.hrust'.")
    print("  3. Don gudanar da lissafi, a shiga terminal a rubuta:")
    print("     python h-run.py run templates/gwaji.hausa")
    print("=" * 60 + "\n")
    return 0


def is_expected_extension_target(target_dir, vscode_extensions_path):
    return target_dir.parent == vscode_extensions_path and target_dir.name == EXTENSION_NAME


if __name__ == "__main__":
    raise SystemExit(deploy_school_lab_bundle())
