# Hausa Ecosystem

Hausa Ecosystem 1.0 is a beginner-friendly programming toolkit for writing
Python and Rust with Hausa vocabulary. It translates to standard source code;
it is not a separate VM or sandbox.

## Features

- `.hausa` translation and execution on Python 3.10+
- `.hrust` translation, checking, compilation, and execution with stable Rust
- Hausa-localized diagnostics with source lines
- Core, database, web, Django, and complete vocabulary profiles
- Flask, FastAPI, Django, and SQLite learning-project generators
- File/project checks, CRUD API checks, and environment diagnostics
- VS Code syntax highlighting and snippets

## Install

```bash
python -m pip install .
hausa --version
hausa doctor
```

The installed package does not write into its installation directory. Built-in
vocabulary comes from package source. Optional user overrides live under the
operating system's user-data directory, or `HAUSA_DATA_DIR` when set.

## Commands

```bash
hausa new python app.hausa
hausa run app.hausa
hausa run app.hausa --profile core --verbose
hausa to-en app.hausa -o app.py
hausa to-ha app.py -o app.hausa
hausa check app.hausa
hausa scan .
hausa keywords python --profile core
hausa new backend flask my_api
hausa new backend fastapi my_api
hausa new database sqlite my_db
hausa test-api flask http://127.0.0.1:5000
```

Profiles are cumulative: `builtins` means core plus Python 3.14 built-ins;
`database` means core plus database vocabulary;
`flask` and `fastapi` add only their framework vocabulary; and `web` enables
both frameworks. `all` preserves pre-1.0 behavior.

## Safety

`hausa run` executes translated programs with the current user's permissions.
Only run code you trust. Rust compilation and execution have a configurable
timeout and use an isolated temporary build directory; this is resource control,
not a security sandbox.

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python -m build
python -m pip install --force-reinstall dist/*.whl
```

See [the Version 1 language specification](docs/language-spec-v1.md) for the
stable translation contract and [project generator documentation](docs/project-generators.md)
for generated application guidance.

## Editor extension

Run `python install_extension.py`, restart VS Code, and open a `.hausa` or
`.hrust` file. The local extension supplies highlighting and snippets.

## License

MIT
