param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("install","run","test","lint","format","db-init","db-migrate")]
  [string]$Task,

  [string]$Message
)

$ErrorActionPreference = "Stop"

function Require-Message {
  if ([string]::IsNullOrWhiteSpace($Message)) {
    throw "Message is required. Example: .\scripts\tasks.ps1 db-migrate -Message 'add users table'"
  }
}

switch ($Task) {
  "install" {
    uv sync
  }
  "run" {
    uv run flask --app app:create_app --debug run --host 127.0.0.1 --port 5000
  }
  "test" {
    uv run pytest
  }
  "format" {
    uv run --group format black .
  }
  "lint" {
    uv run --group lint flake8 .
    uv run --group type mypy .
  }
  "db-init" {
    uv run flask --app app:create_app db init
  }
  "db-migrate" {
    Require-Message
    uv run flask --app app:create_app db migrate -m "$Message"
    uv run flask --app app:create_app db upgrade
  }
}
