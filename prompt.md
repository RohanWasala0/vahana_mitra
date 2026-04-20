You are a **Senior Python Engineer** and **Flask Web platform architect**. You write production-grade, secure, typed, testable cli instruction and template code with clean structure, excellent defaults, and practical documentation.

## Objective
Generate a **complete, production-ready Flask application scaffold** using **`uv`** for dependency + environment management and **`uv tools`** for tooling of command-line interfaces. The output must be **detailed step-by-step** guide.

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
   - Search (optional but common in logistics):
     - Start with Postgres full-text + indexes

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

Here’s a “best-practice, professional” Flask-centric stack for a logistics web app (shipments, tracking, dispatch, billing, warehouses), optimized for reliability, maintainability, and growth. I’ll list a solid default stack first, then common upgrades depending on scale/requirements.

## Recommended professional stack (Flask)

### Backend (Flask API)

* **Python**: 3.11+ (fast, mature ecosystem)
* **Framework**: **Flask** (API-focused) + **Blueprints** (modular structure)
* **API style**: REST (simple) or GraphQL (only if you truly need it)
* **Validation/serialization**: **Pydantic** (strong typing + validation) or **Marshmallow**
* **Auth**:

  * **JWT** for SPA/mobile clients (access + refresh tokens)
  * **Session + CSRF** if you’re doing server-rendered templates
  * **RBAC** (roles like Admin/Dispatcher/Driver/Customer) as first-class design

### Data layer

* **Database**: **PostgreSQL** (best general-purpose choice for logistics data)
* **ORM**: **SQLAlchemy 2.x**
* **Migrations**: **Alembic** (often via Flask-Migrate)
* **Search (optional but common in logistics)**:

  * Start with Postgres full-text + indexes
  * Upgrade to **OpenSearch/Elasticsearch** if you need advanced search across shipments, PODs, addresses, etc.

### Background jobs & async work (critical for logistics)

Logistics apps almost always need async processing:

* webhook processing, label generation, ETA calculation, batch imports, notifications, route optimization calls, etc.
* **Task queue**: **Celery**
* **Broker**: **Redis** (simple) or RabbitMQ (heavier-duty)
* **Scheduler**: Celery Beat or APScheduler (Celery Beat is common)
* **Realtime updates (optional)**: Flask-SocketIO or push via polling + events

### Caching & rate limiting

* **Redis**: caching, session storage (if needed), idempotency keys
* **Rate limiting**: Flask-Limiter (protect APIs, especially tracking endpoints)

### Frontend

Two good “professional” options:

1. **SPA**: **React (Next.js)** or **Vue (Nuxt)**

   * best for dispatcher dashboards, maps, complex UIs
2. **Server-rendered**: Flask + **Jinja2** + HTMX (fast to ship, simpler infra)

For logistics specifically, dashboards often benefit from SPA + component libraries:

* **UI**: MUI/Ant Design (React) or Vuetify (Vue)

### Maps, geocoding, routing (logistics-specific)

* **Maps**: Mapbox or Google Maps
* **Geocoding**: Mapbox/Google or open-source **Nominatim** (OSM) depending on budget
* **Distance matrix / routing**: Google Distance Matrix, Mapbox Directions, or OSRM (self-host)

### Observability (this is where “professional” shows)

* **Structured logging**: `structlog` or Python logging with JSON format
* **Error tracking**: Sentry
* **Metrics**: Prometheus + Grafana
* **Tracing**: OpenTelemetry (optional but great for distributed systems)

### Testing & quality

* **pytest** + coverage
* **Factory Boy** (fixtures), Faker
* **Lint/format**: Ruff + Black
* **Type checking**: mypy (optional but recommended on larger codebases)
* **API contracts**: OpenAPI/Swagger (Flask-RESTX / flask-smorest / apispec)

### Deployment & infrastructure

* **WSGI server**: Gunicorn (common)
* **Reverse proxy**: Nginx or an equivalent managed load balancer
* **Containers**: Docker (standard)
* **CI/CD**: GitHub Actions / GitLab CI
* **Hosting**:

  * AWS (ECS/Fargate), GCP (Cloud Run), Azure (Container Apps), or Kubernetes if you truly need it
* **Secrets/config**: environment variables + a secrets manager (AWS Secrets Manager, etc.)

---

## Default architecture I’d choose for a logistics web app

**Flask (REST API) + Postgres + Redis + Celery + React dashboard**
This covers:

* operational dashboards
* async workflows (notifications, imports, integration polling)
* scalable read paths (caching)
* strong transactional integrity (Postgres)

---

## “It depends” upgrades (when you need them)

* **High throughput / many integrations** → add **Kafka** (event streaming) or RabbitMQ with stronger patterns
* **Complex reporting** → add a **warehouse** (BigQuery/Redshift) + ETL
* **Multi-tenant SaaS** → enforce tenant isolation (schema-per-tenant or row-level) + strict RBAC
* **Heavy read APIs (public tracking)** → cache aggressively + CDN + rate limit + idempotency keys
* **Hard geospatial needs** → **PostGIS** in Postgres (geofencing, proximity queries, heatmaps)

---

## Practical stack summary (copy/paste)

* Backend: Flask, SQLAlchemy, Alembic, Pydantic, JWT/RBAC
* Data: PostgreSQL (+ PostGIS if needed)
* Async: Celery + Redis
* Frontend: Next.js (React) or Nuxt (Vue)
* Infra: Docker, Gunicorn, Nginx, CI/CD
* Observability: Sentry, Prometheus/Grafana, structured logs

If you tell me whether your logistics site is **B2B dispatch dashboard**, **customer shipment tracking**, **last-mile delivery**, or **warehouse/inventory**, I’ll tailor the stack (and module breakdown) to the exact workflows.
Now generate the complete scaffold.
