# Contributing Guide

## 1. Purpose

This document defines the development standards and workflow for the backend team.

The goal is to keep the codebase:

- Modular
- Maintainable
- Testable
- Secure
- Consistent
- Easy for new developers to understand

Every developer is expected to follow these conventions unless a technical decision has been explicitly approved by the backend lead.

---

## 2. Project Architecture

The project uses a domain-oriented Django architecture.

Each business domain is isolated inside `apps/`.

Example:

```text
apps/
├── authentication/
├── users/
├── products/
├── categories/
├── inventory/
├── carts/
├── checkout/
├── payments/
├── orders/
├── shipping/
├── notifications/
├── reviews/
└── analytics/
```

A domain should generally follow this structure:

```text
domain/
├── api/
│   └── v1/
│       ├── views.py
│       ├── serializers.py
│       └── urls.py
├── services/
├── selectors/
├── models/
├── permissions/
├── admin/
├── migrations/
├── tests/
└── apps.py
```

Do not create files or folders simply to satisfy the structure. Add them when the domain actually needs them.

---

## 3. Responsibilities of Each Layer

### `models/`

Contains database models and relationships.

Models should represent the domain's data.

Avoid putting large business workflows inside models.

### `services/`

Contains business operations and commands.

Examples:

```python
create_order()
cancel_order()
process_payment()
register_user()
verify_email()
```

A service should represent an action the system performs.

### `selectors/`

Contains read/query logic.

Examples:

```python
get_user_orders()
get_pending_orders()
get_product_by_slug()
```

Complex ORM queries should generally live here rather than being repeated throughout views.

### `api/v1/`

Contains the HTTP interface:

- Views
- Serializers
- URLs

Views should remain thin and delegate business operations to services/selectors.

### `permissions/`

Contains domain-specific authorization rules.

### `admin/`

Contains Django Admin configuration for the domain.

### `tests/`

Tests are organized around the architecture.

Recommended structure:

```text
tests/
├── test_models.py
├── test_services.py
├── test_selectors.py
└── test_api.py
```

---

## 4. Dependency Direction

Prefer this flow:

```text
HTTP Request
     |
     v
API View
     |
     +----> Serializer
     |
     v
Service / Selector
     |
     v
Model / ORM
     |
     v
Database
```

Do not place business logic in serializers or API views when it belongs in a service.

A serializer should primarily validate and transform API data.

A selector should primarily retrieve data.

A service should primarily perform business operations.

---

## 5. Domain Boundaries

Each domain owns its internal implementation.

For example:

```text
apps/orders/
```

owns order-related business logic.

Other domains should not directly manipulate internal Order implementation unless there is a clear reason.

Prefer public service/selector interfaces:

```python
from apps.orders.services.order_service import create_order
```

instead of spreading direct model manipulation across unrelated domains.

If another domain needs functionality that does not exist, discuss adding a proper service/selector rather than bypassing the domain boundary.

---

## 6. API Versioning

APIs are versioned.

Example:

```text
/api/v1/products/
/api/v1/orders/
```

A breaking API change requires a new version.

Example:

```text
/api/v1/orders/
/api/v2/orders/
```

Do not create a new API version for non-breaking changes such as adding an optional response field.

Breaking changes include:

- Removing response fields
- Renaming response fields
- Changing response structures
- Changing authentication requirements
- Changing endpoint behavior in an incompatible way

---

## 7. API Response Standards

Success responses should use the project's standard response helper/class.

Example:

```json
{
  "statusCode": 200,
  "message": "Order retrieved successfully",
  "data": {}
}
```

Errors should use the project's global exception handler.

Example:

```json
{
  "statusCode": 400,
  "message": "Validation failed",
  "error": "Bad Request",
  "details": {}
}
```

Do not create custom response formats for individual endpoints without approval.

---

## 8. Validation

Never trust client input.

Validate data at the API boundary using DRF serializers and appropriate validators.

Example:

```python
serializer.is_valid(raise_exception=True)
```

Business rules that go beyond simple input validation should be handled in services.

---

## 9. Database Changes

Database schema changes must be performed through Django migrations.

Use:

```bash
uv run python manage.py makemigrations
```

Then:

```bash
uv run python manage.py migrate
```

Never manually modify the production database schema with ad-hoc `ALTER TABLE` commands.

Always commit migration files with the code that requires them.

Before creating a migration, make sure your model changes are intentional.

---

## 10. Database Indexing

Indexes should be based on actual query patterns.

Do not add indexes to every field.

Consider indexes for fields frequently used in:

- `filter()`
- `get()`
- `order_by()`
- joins
- composite query conditions

Example:

```python
class Meta:
    indexes = [
        models.Index(
            fields=["user", "status"],
            name="idx_order_user_status",
        ),
    ]
```

Before adding an index, understand the query it is intended to optimize.

For performance-sensitive queries, verify the query plan using database tools such as `EXPLAIN ANALYZE`.

---

## 11. Authentication and Security

Authentication-related code must follow the project's security standards.

General rules:

- Never store passwords in plain text.
- Never commit secrets.
- Do not put sensitive tokens in logs.
- Use secure cookies for refresh tokens where applicable.
- Validate authentication and authorization server-side.
- Do not expose internal exception traces to API clients.
- Do not trust frontend authorization checks.

Sensitive configuration must come from environment variables.

---

## 12. Environment Variables

Never commit `.env`.

The repository should contain:

```text
.env.example
```

Example:

```text
DJANGO_SECRET_KEY=
DEBUG=False
DATABASE_URL=
REDIS_URL=
```

Developers create their own local `.env` from `.env.example`.

If a new environment variable is introduced:

1. Add it to `.env.example`.
2. Document its purpose.
3. Update the relevant settings.
4. Do not commit its real value.

---

## 13. Branching Strategy

Do not work directly on `main`.

Use feature branches.

Examples:

```text
feature/auth-registration
feature/order-creation
feature/product-search
fix/payment-webhook
refactor/order-service
```

Branch names should clearly communicate the purpose of the work.

---

## 14. Commit Messages

Use Conventional Commit style.

Examples:

```text
feat(auth): add user registration
feat(orders): implement order creation
fix(auth): prevent expired OTP verification
fix(payments): handle duplicate webhook events
refactor(products): move query logic to selectors
test(orders): add order service tests
docs(api): document order endpoints
chore(deps): update project dependencies
```

Keep commits focused.

Avoid commits such as:

```text
update
changes
fix stuff
final
final2
```

---

## 15. Pull Requests

Every feature or fix should be submitted through a Pull Request.

A PR should contain:

- What changed
- Why it changed
- How it was tested
- Any migration changes
- Any API changes
- Any environment variables added
- Any known limitations

Keep PRs focused.

Avoid combining unrelated features into one PR.

---

## 16. Code Review

Reviewers should check:

### Correctness

- Does the implementation solve the intended problem?
- Are edge cases handled?

### Architecture

- Is business logic in the correct layer?
- Are domain boundaries respected?

### Security

- Is user input validated?
- Are permissions enforced?
- Are sensitive values protected?

### Database

- Are queries efficient?
- Are indexes appropriate?
- Are migrations included?

### Testing

- Are important paths covered?
- Are failure cases tested?

### Maintainability

- Is the code readable?
- Are names meaningful?
- Is unnecessary duplication avoided?

---

## 17. Testing

Run the test suite before opening a PR.

The exact command depends on the project's configured test runner, but the standard project command should be documented in the development guide.

Tests should cover:

- Models
- Services
- Selectors
- API endpoints
- Authentication
- Permissions
- Important failure cases

Do not only test successful requests.

---

## 18. Idempotency

Critical operations must be designed to handle duplicate requests safely.

Examples include:

- Checkout
- Payment confirmation
- Refunds
- Webhooks
- Order creation where applicable

A request being retried should not accidentally create duplicate financial or business records.

---

## 19. Event-Driven Side Effects

Long-running or independent side effects should not unnecessarily block the main request.

Examples:

```text
Order placed
    |
    +--> Send notification
    +--> Update analytics
    +--> Adjust inventory
```

Queues/events should be used where appropriate.

Do not introduce asynchronous infrastructure merely for the sake of using it. Use it when it provides a clear reliability or performance benefit.

---

## 20. Logging

Logs should help developers diagnose production problems without exposing sensitive information.

Do not log:

- Passwords
- Access tokens
- Refresh tokens
- OTP codes
- Payment secrets
- API keys

Prefer structured, meaningful logs.

---

## 21. Documentation

API behavior should be documented using OpenAPI.

When an endpoint changes:

- Update the API documentation.
- Update request/response examples where necessary.
- Update tests.

Architecture decisions that affect multiple developers should be documented.

---

## 22. Adding a New Domain

When adding a new domain:

1. Create the Django app under `apps/`.
2. Add its `AppConfig`.
3. Register it in settings.
4. Create the domain structure.
5. Add models.
6. Add migrations.
7. Add services/selectors where needed.
8. Add API v1.
9. Add tests.
10. Register URLs.
11. Update documentation.

Do not copy another domain blindly. Keep only the layers the new domain actually needs.

---

## 23. Definition of Done

A task is not complete simply because the code works locally.

Before considering a task complete:

- [ ] Code follows the project architecture.
- [ ] Input validation is implemented.
- [ ] Authorization is implemented where required.
- [ ] Tests are added or updated.
- [ ] Database migrations are included if needed.
- [ ] API documentation is updated if needed.
- [ ] Environment variables are documented if added.
- [ ] No secrets are committed.
- [ ] Relevant tests pass.
- [ ] Code has been reviewed.
- [ ] The branch is ready to merge.

---

## 24. When in Doubt

If a task does not clearly fit the architecture, do not introduce a new pattern independently.

Discuss it with the backend lead before creating a new architectural convention.

Consistency across the codebase is more valuable than having multiple technically valid patterns.
