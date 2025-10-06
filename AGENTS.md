# Repository Guidelines

## Architecture & Responsibilities
Maintain the layered separation of concerns outlined in `CLAUDE.md`: presentation (`main.py`, `server.py`) delegates to manager workflows, which call business logic (`classification/`, `crawler/`, `extract/`), which rely on data models (`extract/structure.py`) and infrastructure utilities (`tools/`, `common/`, `spkg/`). Keep dependencies flowing inward and favor small, focused modules.

## Project Structure & Module Organization
Backend Python code lives in `dlsite_classification/` with focused subpackages for scraping (`crawler`), extraction (`extract`), utilities (`tools`), and classification/management pipelines. The Nuxt frontend sits in `dlsite_classification_web/`; CLI entry points are `main.py` and `server.py`, docs and assets stay under `doc/`, tests in `tests/`, and generated artifacts like `htmlcov/` or `log/` should remain untracked.

## Development Workflow
Create a virtualenv with `uv venv` then install dependencies via `uv pip install -r requirements.txt`. Run the CLI with `uv run python main.py` or launch the API using `uv run python server.py --data-path <dir>` plus optional `--host/--port`. For the web UI, run `yarn install` then `yarn dev` inside `dlsite_classification_web/`; validate production builds with `yarn build && yarn preview`.

## Static Analysis & Formatting
Always run these commands after making changes:
```bash
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
```
Ruff enforces formatting (88-char lines, double quotes, import ordering) and a broad lint rule set. Keep functions annotated and respect `snake_case` / `PascalCase` / `UPPER_CASE` naming conventions.

## Testing Workflow
Prefer the standardized script from `CLAUDE.md`:
```bash
./run_tests.sh
```
This maintains consistent coverage settings and fast feedback. Use `./run_tests.sh --verbose` or `--html` as needed. For quick iterations you may still use `uv run pytest`, but always finish with the script. On WSL, fix potential `bad interpreter` errors via `sed -i 's/\r$//' run_tests.sh && chmod +x run_tests.sh`.

## CI/CD Automation
GitHub Actions workflows in `.github/workflows/` mirror the local quality gates. Keep triggers on `main`, `develop`, and `feat/**` branches aligned with release policy and update secrets when rotating tokens.

- **CI** runs lint, test, and security summary jobs across Python 3.10–3.13. Lint installs dependencies with `uv sync --dev --frozen`, then executes `uv run ruff check dlsite_classification/ --output-format=github`, `uv run ruff format --check dlsite_classification/`, `uv run mypy dlsite_classification/ --strict --show-error-codes`, and layered Bandit scans over `dlsite_classification/` while uploading JSON/txt artifacts. Tests reuse the same matrix, call `uv sync --dev --frozen`, execute `./run_tests.sh` (or its coverage equivalent), generate coverage XML/HTML, upload to Codecov (`CODECOV_TOKEN`), and publish `htmlcov/` as an artifact. A dedicated security job performs comprehensive Bandit passes with multiple reporters and uploads every result.
- **CodeQL** analyses Python weekly (Monday 03:00 UTC) and on PRs. It initializes with `.github/codeql/codeql-config.yml`, installs dependencies via `uv sync --frozen`, exports `PYTHONPATH=$PWD`, then runs `github/codeql-action/analyze@v3` with uploads disabled for local control. Keep the config file authoritative for query packs.
- **Gitleaks** downloads the latest release, scans the full history (`fetch-depth: 0`), and fails the workflow on secret findings. Ensure `GITLEAKS_LICENSE` is configured in repository secrets when required.
- **Semgrep Security Scan** installs Semgrep on Python 3.13 runners, executes `semgrep --config=p/security-audit --config=p/python --config=p/bandit --sarif --output=semgrep.sarif .`, uploads SARIF to GitHub’s code scanning dashboard, and stores artifacts for manual review. Treat false positives by adding rules to `.semgrepignore` rather than editing the workflow.
- **PR Agent Review** triggers on PR open/reopen/sync, clones `qodo-ai/pr-agent`, installs it in editable mode, and runs describe/review/improve flows using `OPENAI_API_KEY` and the provided `GITHUB_TOKEN`. It can also update changelog entries and labels; adjust `.secrets.toml` overrides for repository-specific behavior.

## Commit & Pull Request Guidelines
History shows Conventional Commit prefixes (`feat:`, `fix:`, `doc:`); keep subjects imperative and note touched subsystems when possible. Ensure every commit passes lint, static analysis, tests, and CI workflows. Avoid coupling unrelated frontend/backends changes. Pull requests need a clear summary, proof of testing (`./run_tests.sh`, `uv run pytest`, `./run_tests.sh --html`, or UI screenshots), and cross-links to issues or DLsite tickets.

## Security & Configuration Tips
Set `DLSITE_DATA_PATH` or pass `--data-path` when running `server.py` to pin classification sources; document defaults if you add new env vars. Reuse helpers in `dlsite_classification/common/security.py` for sanitizing crawler output, and update `.gitignore` whenever new tooling introduces cache or report directories.
