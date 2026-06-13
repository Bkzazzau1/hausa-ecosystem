# Hausa Ecosystem

Hausa Ecosystem is a programming-language support project that makes it possible to write and run beginner-friendly code using Hausa keywords.

The project currently supports:

- **Hausa Python** with `.hausa` files
- **Hausa Rust** with `.hrust` files
- Hausa-to-English code translation
- English-to-Hausa code translation
- Hausa-localized runtime and compiler error messages
- A Visual Studio Code extension for syntax highlighting
- Developer-friendly CLI helpers for starter files, keyword lookup, and output files

## Why this project matters

Programming is easier to learn when students can connect concepts with their own language. Hausa Ecosystem is designed to help Hausa-speaking learners understand programming logic faster while still producing valid Python and Rust code behind the scenes.

## Project structure

```text
hausa-ecosystem/
├── core/
│   ├── database.py          # SQLite-backed keyword loading
│   ├── dictionary.py        # Hausa <-> English keyword and error dictionaries
│   ├── python_engine.py     # Hausa Python translator and runner
│   └── rust_engine.py       # Hausa Rust translator, compiler and runner
├── extensions/
│   └── vscode-hausa/        # VS Code syntax highlighting extension
├── templates/
│   ├── gwaji.hausa          # Hausa Python example
│   └── gwaji.hrust          # Hausa Rust example
├── tests/                   # Automated pytest tests
├── h-run.py                 # Main command-line runner
├── install_extension.py     # Local VS Code extension installer
└── update_vs_extension.py   # Rebuilds extension syntax keywords
```

## Requirements

- Python 3.10+
- Visual Studio Code, for the extension
- Rust installed through Rustup, only if you want to run `.hrust` files
- Flask, only if you want to run the web-server example in `templates/gwaji.hausa`

## Basic usage

Check CLI version:

```bash
python h-run.py --version
```

Create a new Hausa Python starter file:

```bash
python h-run.py new python app.hausa
```

Create a new Hausa Rust starter file:

```bash
python h-run.py new rust app.hrust
```

List available Hausa Python keywords:

```bash
python h-run.py keywords python
```

List available Hausa Rust keywords:

```bash
python h-run.py keywords rust
```

Run a Hausa Python file:

```bash
python h-run.py run templates/gwaji.hausa
```

Translate Hausa Python to normal Python:

```bash
python h-run.py to-en templates/gwaji.hausa
```

Translate Hausa Python to a Python output file:

```bash
python h-run.py to-en templates/gwaji.hausa -o output.py
```

Translate normal Python to Hausa Python:

```bash
python h-run.py to-ha example.py
```

Translate normal Python to a Hausa output file:

```bash
python h-run.py to-ha example.py -o output.hausa
```

Run a Hausa Rust file:

```bash
python h-run.py run templates/gwaji.hrust
```

Translate Hausa Rust to normal Rust:

```bash
python h-run.py to-en templates/gwaji.hrust
```

Translate Hausa Rust to a Rust output file:

```bash
python h-run.py to-en templates/gwaji.hrust -o output.rs
```

Translate normal Rust to Hausa Rust:

```bash
python h-run.py to-ha example.rs
```

Translate normal Rust to a Hausa Rust output file:

```bash
python h-run.py to-ha example.rs -o output.hrust
```

## Install the VS Code extension locally

From the project root, run:

```bash
python install_extension.py
```

Then restart VS Code and open any `.hausa` or `.hrust` file.

## Run automated tests

Install the development test dependency:

```bash
pip install -r requirements-dev.txt
```

Run the full test suite:

```bash
python -m pytest
```

The Rust execution test runs only when `rustc` is installed. If Rust is not installed, that test is skipped instead of failing.

## Update VS Code syntax rules

When new Hausa keywords are added to `core/dictionary.py`, run:

```bash
python update_vs_extension.py
```

This updates the TextMate grammar files inside `extensions/vscode-hausa/syntaxes/`.

## Notes for contributors

- Keep local database files out of GitHub.
- Use `core/dictionary.py` as the main source for built-in keyword mappings.
- Keep examples simple enough for beginners.
- Test both translation directions before publishing changes.

## Roadmap

- Package the runner as a proper CLI command
- Add more beginner examples in Hausa
- Improve Rust translation so strings and comments are preserved more safely
- Prepare the VS Code extension for marketplace publishing
