# install_extension.py
import os
import shutil
from pathlib import Path


EXTENSION_NAME = "vscode-hausa"


def deploy_extension():
    source_dir = Path.cwd() / "extensions" / EXTENSION_NAME

    if not source_dir.exists():
        print("Kuskure: Ba a sami babban fashin extension din ba a wannan hanyar:")
        print(source_dir)
        return 1

    home_dir = Path(os.path.expanduser("~"))
    vscode_ext_base = home_dir / ".vscode" / "extensions"
    target_dir = vscode_ext_base / EXTENSION_NAME

    print("Ana kokarin gano inda VS Code yake...")
    print(f"Hanyar Tsarin: {target_dir}")

    source_resolved = source_dir.resolve()
    target_resolved = target_dir.resolve()
    base_resolved = vscode_ext_base.resolve()

    if source_resolved == target_resolved:
        print("Kuskure: Source da target iri daya ne, ba za a kwafe ba.")
        return 1

    if not is_expected_extension_target(target_resolved, base_resolved):
        print("Kuskure: Target path bai dace da VS Code extension folder ba:")
        print(target_resolved)
        return 1

    try:
        vscode_ext_base.mkdir(parents=True, exist_ok=True)

        if target_dir.exists():
            print("An sami tsohon extension girkawa, ana wanke shi...")
            shutil.rmtree(target_dir)

        shutil.copytree(source_dir, target_dir)
        print("\n" + "=" * 60)
        print("AN YI NASARA! AN SAMAR DA HAUSA VS CODE EXTENSION!")
        print("Yadda zaka kunna shi:")
        print("  1. Rufe duka windows na VS Code da suke bude yanzu.")
        print("  2. Sake bude VS Code dinka.")
        print("  3. Bude fayil mai karshen '.hausa' ko '.hrust' don ganin launuka.")
        print("=" * 60 + "\n")
        return 0
    except Exception as exc:
        print(f"Kuskuren tura fayiloli: {exc}")
        return 1


def is_expected_extension_target(target_dir, vscode_ext_base):
    try:
        return target_dir.parent == vscode_ext_base and target_dir.name == EXTENSION_NAME
    except OSError:
        return False


if __name__ == "__main__":
    raise SystemExit(deploy_extension())
