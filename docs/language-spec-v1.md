# Hausa Ecosystem Language Specification, Version 1

## Status and compatibility

This document defines the stable Version 1 source-translation contract. A
Version 1 release may add vocabulary, diagnostics, or tooling without breaking
valid Version 1 programs. Removing a canonical word or changing its meaning
requires a new major version.

Hausa Python targets Python 3.10 or newer. Hausa Rust targets the stable Rust
edition selected by the installed `rustc` unless the caller supplies a compiler
configuration in a future compatible release.

## File types and encoding

`.hausa` is Hausa Python and `.hrust` is Hausa Rust. Source files are UTF-8.
Identifiers follow the target language's Unicode identifier rules. Comments and
string contents are never vocabulary-translated.

## Translation model

Hausa Ecosystem performs lexical translation and then delegates parsing,
execution, and semantics to Python or Rust. It does not change the target
language type system, control flow, module system, or security model.

Python translation operates only on `NAME` tokens. Rust translation operates on
identifiers while preserving normal strings, raw strings, character literals,
lifetimes, line comments, and nested block comments. Incomplete Python input
that cannot be safely tokenized is rejected instead of being modified with a
textual replacement fallback.

Reverse translation uses the first declared Hausa spelling as the canonical
word when aliases map to the same target word. Consequently, reverse translation
is deterministic but is not guaranteed to reproduce an alias from the original
source.

## Vocabulary profiles

- `core`: syntax, control flow, built-in constants, and beginner-facing types.
- `builtins`: core plus all functions built into Python 3.14.
- `database`: core plus SQLite, MongoDB, and common persistence vocabulary.
- `web`: core plus Flask, FastAPI, routing, and HTTP vocabulary.
- `flask`: core and database vocabulary plus Flask-specific names.
- `fastapi`: core and database vocabulary plus FastAPI-specific names.
- `all`: every built-in Version 1 word; this is the compatibility default.

Profiles limit accidental translation of application identifiers. Projects
should choose the narrowest profile they require. The authoritative mappings
are in `core/dictionary.py`; `hausa keywords` exposes them to users.

## Spelling and aliases

Dictionary keys are case-sensitive. Underscores are part of multiword tokens.
Canonical terms are the first spelling declared for a target token. Additional
spellings are compatibility aliases, not separate semantics. New terminology
should be reviewed by fluent Hausa speakers and educators before being marked
stable.

## Diagnostics

Translation failures, target-language syntax/compiler errors, and program
runtime errors are distinct failures and return a non-zero status. Python
diagnostics show the original Hausa line when available. `--verbose` may expose
the target-language traceback. Rust compiler paths are remapped to the original
source filename where possible.

## Execution and trust

Hausa source has exactly the authority of the translated target program.
`hausa run` is not a sandbox. Rust build isolation and timeouts prevent leftover
artifacts and unbounded waiting but do not make untrusted native code safe.

## Out of scope for Version 1

SQL text inside strings is not translated. Automatic dialect detection,
translation of arbitrary library APIs, formatting, a language server, package
management, and secure execution of untrusted programs are not language
features in Version 1.
