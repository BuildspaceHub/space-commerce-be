# Development Guide

## Prerequisites

Install:

- Git
- Python
- uv
- PostgreSQL
- Docker (recommended for supporting infrastructure)

The project uses `uv` for Python dependency and environment management.

## Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

## Install Dependencies

Create the project's virtual environment and install dependencies:

```bash
uv sync
```

If development dependency groups are configured:

```bash
uv sync --group dev
```

## Environment Variables

Copy:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Never commit `.env`.

## Run Django

Use `uv run` so commands execute inside the project's managed environment:

```bash
uv run python manage.py runserver
```

## Django Commands

Create migrations:

```bash
uv run python manage.py makemigrations
```

Apply migrations:

```bash
uv run python manage.py migrate
```

Create a superuser:

```bash
uv run python manage.py createsuperuser
```

Open Django shell:

```bash
uv run python manage.py shell
```

## Adding Dependencies

Do not manually edit dependency versions unless the project convention requires it.

Add a runtime dependency:

```bash
uv add <package>
```

Add a development-only dependency:

```bash
uv add --dev <package>
```

If dependency groups are configured, use the project's documented group convention.

After changing dependencies, commit the relevant `pyproject.toml` and `uv.lock` changes.

## Running Tests

Run the project's configured test command.

For Django's test runner:

```bash
uv run python manage.py test
```

If pytest is adopted:

```bash
uv run pytest
```

Do not introduce a second test runner without agreement from the backend lead.

## Creating a New Django App

Create the app under `apps/`.

For example:

```bash
uv run python manage.py startapp products apps/products
```

Then reorganize it into the project's domain structure.

Do not immediately create unnecessary empty folders.

## Running Checks

Before opening a PR:

```bash
uv run python manage.py check
```

Run tests:

```bash
uv run python manage.py test
```

Run any configured linting/formatting/type-checking commands.

## Migrations

Always create migrations after model changes:

```bash
uv run python manage.py makemigrations
```

Review generated migration files before committing them.

Then test:

```bash
uv run python manage.py migrate
```

Never delete or rewrite an already-applied migration to fix a production schema problem without a deliberate migration strategy.

## Local Development

A normal workflow is:

```text
Pull latest changes
    ↓
Create feature branch
    ↓
Install/sync dependencies
    ↓
Configure .env
    ↓
Run migrations
    ↓
Implement task
    ↓
Run checks
    ↓
Run tests
    ↓
Commit
    ↓
Push
    ↓
Open PR
```

## Useful uv Commands

Check uv:

```bash
uv --version
```

Synchronize environment:

```bash
uv sync
```

Add package:

```bash
uv add package-name
```

Add development package:

```bash
uv add --dev package-name
```

Remove package:

```bash
uv remove package-name
```

Run a command in the project environment:

```bash
uv run <command>
```

Update dependencies:

```bash
uv lock --upgrade
```

## Important Rule

Developers should prefer:

```bash
uv run python manage.py ...
```

over manually activating a virtual environment and running:

```bash
python manage.py ...
```

This keeps the project's Python environment reproducible and makes onboarding easier.
