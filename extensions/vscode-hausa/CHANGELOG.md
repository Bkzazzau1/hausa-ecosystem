# Changelog

## 1.2.0

- Added optional, debounced diagnostics for unsaved Hausa source while typing.
- Made Hausa-Python completions respect the selected vocabulary profile.
- Added verification that translation commands created their requested output.
- Kept temporary diagnostic files outside the project and removed them after every check.

## 1.1.0

- Added Run, Check, Translate to English, Translate to Hausa, and Select
  Vocabulary Profile commands.
- Added Hausa keyword completion and English hover documentation generated
  from the canonical vocabulary.
- Added Problems-panel diagnostics on open and save.
- Added settings for CLI location, vocabulary profile, and automatic diagnostics.
- Added editor-title and editor-context actions.

## 1.0.1

- Added a custom Hausa Ecosystem Marketplace icon.
- Added distinct highlighting scopes for control flow, constants, types,
  built-in functions, framework functions, and Rust declarations.
- Fixed highlighting for Hausa-Rust words containing apostrophes such as
  `jama'a`.
- Expanded Marketplace documentation and editor-configuration tests.

## 1.0.0

- Initial Marketplace-ready release.
- Added Hausa Python and Hausa Rust language registration.
- Added syntax highlighting, snippets, and language-specific editor settings.
- Added Python 3.14 keyword and built-in vocabulary highlighting.
