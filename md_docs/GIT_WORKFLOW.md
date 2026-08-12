# Git and Pull Request Workflow

## Branch Protection

The `main` branch should be protected.

Developers should not push directly to `main`.

Production changes should enter through reviewed Pull Requests.

## Branch Naming

Use:

```text
feature/<short-description>
fix/<short-description>
refactor/<short-description>
test/<short-description>
docs/<short-description>
chore/<short-description>
```

Examples:

```text
feature/auth-registration
feature/order-creation
fix/payment-webhook
refactor/order-selector
test/product-api
docs/api-authentication
chore/update-dependencies
```

## Starting a Task

Update your local main branch:

```bash
git checkout main
git pull origin main
```

Create a branch:

```bash
git checkout -b feature/auth-registration
```

## Working

Make small, focused commits.

Example:

```bash
git add apps/authentication/
git commit -m "feat(auth): implement registration service"
```

## Conventional Commits

Use:

```text
feat
fix
refactor
test
docs
chore
perf
build
ci
```

Examples:

```text
feat(auth): add email verification
fix(orders): prevent duplicate order creation
test(payments): add webhook idempotency tests
refactor(users): move profile queries to selectors
docs(api): document authentication endpoints
chore(deps): update Django
```

## Before Push

Run:

```bash
uv run python manage.py check
uv run python manage.py test
```

Also run configured formatting, linting, and type checking.

Then:

```bash
git status
git diff
```

Review your changes before pushing.

## Push

```bash
git push -u origin feature/auth-registration
```

## Pull Request

The PR should explain:

### What

What was implemented?

### Why

Why was the change necessary?

### Testing

How was it tested?

### Database

Were migrations created?

### API

Were endpoints added or changed?

### Configuration

Were environment variables added?

## PR Review

Do not merge your own PR unless the repository's branch policy explicitly permits it.

Address review comments through new commits or clean amendments according to the team's workflow.

## Keep Branches Focused

Avoid:

```text
feature/product-search

+ authentication refactor

+ payment fixes

+ unrelated formatting

+ dependency upgrades
```

Prefer separate PRs.

Small PRs are easier to review and safer to merge.
