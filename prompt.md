You are a **Principal/Senior Python Backend Engineer** and **Flask platform architect**. You write production-grade, secure, typed, testable cli instruction and template code with clean structure, excellent defaults, and practical documentation.

## Objective
Generate a **complete, production-ready Flask application scaffold** using **`uv`** for dependency + environment management and **`uv tools`** for tooling of command-line interfaces. The output must be **fully copy/pasteable** and include **all code** for **every file** you mention.

## Non-negotiable Requirements
1. **Architecture**
   - Use Flask’s **Application Factory** pattern: `create_app()` in `app/__init__.py`.
   - Follow the Flask **“Larger Applications” (package-based)** structure.
   - Use an **extensions** pattern: `app/extensions.py` to initialize SQLAlchemy, Migrate, etc.
   - Provide a `main` **Blueprint** with:
     - `/` (index page)
     - `/health` (JSON health endpoint)
   - Include `templates/` and `static/` under the blueprint (or app-level, but be consistent and justify briefly).

2. **Database**
   - Use **SQLAlchemy ORM** with **PostgreSQL**.
   - Read DB connection from environment variable `DATABASE_URL` (Postgres URL).
   - Provide:
     - `app/database.py` utility functions (e.g., init, session helpers if needed)
     - A **sample model** (e.g., `User`) with modern SQLAlchemy conventions.
   - Include **Flask-Migrate** and working migration wiring.

3. **Configuration**
   - Class-based config: `Config`, `DevelopmentConfig`, `ProductionConfig`, `TestingConfig`.
   - Load environment variables via **python-dotenv** (`.env`) for local/dev.
   - Provide `.env.example` with required variables and safe defaults.
   - Ensure config supports:
     - `FLASK_ENV`, `SECRET_KEY`, `DATABASE_URL`
     - logging path, debug flags, etc.

4. **Logging**
   - Implement standard Python logging via `logging.config.dictConfig`.
   - Log to:
     - console (human-readable)
     - rotating file handler (e.g., `logs/app.log`)
   - Ensure log directory creation is handled safely (e.g., `pathlib.Path("logs").mkdir(parents=True, exist_ok=True)`).

5. **Testing (uv-first)**
   - Use **pytest** and keep it in uv’s **dev dependency group** (PEP 735):
     - Prefer: `uv add --dev pytest` (or `uv add --group dev pytest`)
   - Provide:
     - `tests/conftest.py` defining `app` and `client` fixtures.
     - One sample functional test (e.g., `/health`).
   - Running tests must work with:
     - `uv run pytest`
     - (optional one-off) `uvx pytest` if you want tests runnable without “installing” tools in the project env.
   - Testing config should avoid external dependencies where practical.
     - If you use Postgres for tests, provide an alternative (SQLite) and clearly document how to switch.

6. **Tooling / Lint / Types / Build (uv + uv tools)**
   - **Project bootstrap**
     - Initialize with uv and generate a packaged layout:
       - Prefer: `uv init --package`
       - If you need to force a build system: `uv init --build-backend uv_build` (implies `--package`)
   - **Python version management (optional but recommended)**
     - Allow pinning a project Python version via:
       - `uv python install <major.minor>`
       - `uv python pin <major.minor>` (creates a `.python-version` file)
   - **Dependencies + lockfile**
     - Use uv as the single source of truth for dependency changes:
       - Add/remove: `uv add ...`, `uv remove ...`
       - Lock: `uv lock` (commit `uv.lock`)
       - Install/sync: `uv sync` (creates/updates `.venv` from `uv.lock`)
     - Use dependency groups for dev tooling, e.g.:
       - `uv add --dev pytest`
       - `uv add --group lint black flake8`
       - `uv add --group type mypy`
     - Production install should be documented with:
       - `uv sync --no-dev` (exclude dev group)
   - **Run commands in the managed environment**
     - Prefer `uv run ...` for everything (app, scripts, tests, linters, type-checking) so it works even without manual venv activation.
   - **uv tool interface (pipx-like)**
     - Support “tooling without installing tools into the project” using uv’s tool runner:
       - `uvx <tool> ...` (alias for `uv tool run`)
       - Examples:
         - `uvx black .`
         - `uvx flake8 .`
         - `uvx mypy .`
     - If you want persistent global installs for CLIs, document:
       - `uv tool install <package>`
   - **Build backend (packaging)**
     - Use uv’s native build backend for pure-Python packages:
       - In `pyproject.toml` include:
         - `[build-system]`
         - `requires = ["uv_build>=<compatible>,<next-minor>"]`
         - `build-backend = "uv_build"`
     - Document building distributions with:
       - `uv build`
   - **pyproject.toml requirements**
     - Provide a `pyproject.toml` with:
       - runtime dependencies in `[project].dependencies`
       - dev tooling in `[dependency-groups]` (e.g., `dev`, `lint`, `type`)
       - tool configs for **black**, **flake8**, **mypy**, **pytest**
     - Use type hints throughout and make mypy settings realistic (not overly permissive, not impossible).

7. **Automation**
   - Provide automation for windows machine with targets:
     - `install` (uv sync/install)
     - `run` (dev server)
     - `test` (pytest)
     - `lint` (flake8 + mypy; black check optional)
     - `db-migrate` (create migration + upgrade; explain required message arg)
   - Provide `README.md` with exact commands for:
     - setup
     - running app
     - running tests
     - formatting/linting
     - creating and applying migrations

8. **Quality Bar**
   - No placeholders like “TODO: add code here” for required parts.
   - No “...” omissions.
   - Include safe defaults and brief rationale where a decision is non-obvious.
   - Use clear module boundaries; keep each file focused.
   - Ensure imports and package wiring are correct.

## Output Format (STRICT)
Produce the answer in this order:
  ### (MOST IMPORTANT FOLLOW TIPS FROM UV DOCS)[https://docs.astral.sh/uv/]
1. **Quick Start** (exact shell commands)  
2. **Directory Tree** (professional `tree` style)  
3. **File-by-file content**  
   - For every file shown in the tree, output its full contents in its own code fence.
   - Precede each code fence with the file path as a markdown heading, e.g. `### app/__init__.py`
   - Use language hints: ```toml, ```python, ```html, ```makefile, ```env, etc.
4. **How to Run & Verify**
   - list of URLs to hit, expected outputs
5. **Common Troubleshooting**
   - 5–10 practical issues (env vars, migrations, import paths, uv usage)

## Assumptions
- Target Python version: **3.12** (if you choose different, justify).
- Project name: choose a sensible default like `flask_uv_scaffold` (or derive from my message), and use it consistently.
- OS: assume macOS/Linux shell commands unless Windows is explicitly requested.

Now generate the complete scaffold.
