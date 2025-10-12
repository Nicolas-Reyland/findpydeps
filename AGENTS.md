# Repository Guidelines
This guide helps maintainers extend the `findpydeps` CLI while keeping packaging and tests consistent.

## Project Structure & Module Organization
- `src/findpydeps/` holds the CLI implementation; `findpydeps.py` defines the parser, dependency scanning, and console entrypoint used by `__main__.py`.
- `tests/functional.py` covers end-to-end behaviour; it compares CLI output against golden files under `tests/functional/`.
- `tests/functional/help-message` stores the expected `--help` banner; regenerate it when updating parser text.
- `pyproject.toml` and `setup.cfg` contain packaging metadata, define the `findpydeps` console script, and use the `src` layout.

## Build, Test, and Development Commands
- `pip install -e .` installs the CLI in editable mode so you can exercise the console script locally.
- `python -m unittest tests.functional` runs the functional regression suite and validates the help message.
- `python -m build` produces source and wheel artifacts via setuptools for release validation.
- `python -m findpydeps --help` is a quick smoke test; redirect output to refresh golden files when changes are intentional.

## Coding Style & Naming Conventions
- Use 4-space indentation, standard library imports first, and keep type hints for public functions as in `findpydeps.py`.
- Name modules and functions with `snake_case`, reserve `UPPER_CASE` for constants like `HEADER`, and keep CLI flag names descriptive.
- When adding options, update both the argparse configuration and the README usage examples in the same patch.

## Testing Guidelines
- Add regression tests beside existing ones in `tests/functional.py`; mirror the CLI scenario name in the fixture path.
- Prefer golden-file comparisons for CLI output; refresh fixtures with `python -m findpydeps --help > tests/functional/help-message`.
- Ensure new behaviour defaults remain backwards compatible; expand tests to cover edge cases for new flags or scanning modes.

## Commit & Pull Request Guidelines
- Follow the existing history of concise titles (`chore:`, `fix:`, etc.) with the imperative mood and reference issues when applicable.
- Describe behavioural changes, updated fixtures, and manual test commands in the PR body; attach before/after snippets for CLI output tweaks.
- Confirm CI or local `python -m unittest` results before requesting review and note any follow-up tasks as checklist items.
