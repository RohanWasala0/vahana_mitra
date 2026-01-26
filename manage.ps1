param(
  [Parameter(Position=0)]
  [ValidateSet("install", "run", "test", "lint", "db-migrate")]
  [string]$Command,

  [Parameter(Position=1)]
  [string]$Message
)

function Fail($Text) {
  Write-Host $Text
  exit 1
}

function Run-Step([string]$Step) {
  Write-Host "==> $Step"
  iex $Step
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

switch ($Command) {
  "install" {
    Run-Step "uv sync"
    break
  }

  "run" {
    # Ensure an app factory is discoverable even if user didn't set FLASK_APP
    if (-not $env:FLASK_APP -or $env:FLASK_APP.Trim().Length -eq 0) {
      $env:FLASK_APP = "app:create_app"
    }
    Run-Step "uv run flask run"
    break
  }

  "test" {
    Run-Step "uv run pytest"
    break
  }

  "lint" {
    Run-Step "uv run black ."
    Run-Step "uv run flake8 ."
    Run-Step "uv run mypy ."
    break
  }

  "db-migrate" {
    if (-not $Message -or $Message.Trim().Length -eq 0) {
      Fail 'Usage: ./manage.ps1 db-migrate "your migration message"'
    }
    if (-not $env:FLASK_APP -or $env:FLASK_APP.Trim().Length -eq 0) {
      $env:FLASK_APP = "app:create_app"
    }
    Run-Step "uv run flask db migrate -m `"$Message`""
    Run-Step "uv run flask db upgrade"
    break
  }
}
