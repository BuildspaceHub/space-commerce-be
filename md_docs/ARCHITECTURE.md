# Backend Architecture

## Overview

This backend uses a domain-oriented Django architecture.

The primary goal is to keep business domains independent, maintainable, testable, and easy for multiple developers to work on simultaneously.

## High-Level Structure

```text
project/
├── apps/
├── common/
├── config/
├── docs/
├── scripts/
├── requirements/
├── tests/
├── manage.py
├── .env.example
└── pyproject.toml
```

## Domain Structure

A typical domain:

```text
apps/orders/
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

## Layer Responsibilities

### API

Handles HTTP concerns.

```text
Request
  ↓
URL
  ↓
View
  ↓
Serializer
```

### Services

Handles business actions.

```text
Service
  ↓
Business rules
  ↓
Database operations / domain logic
```

### Selectors

Handles data retrieval.

```text
Selector
  ↓
QuerySet
  ↓
Database
```

### Models

Represent persistent domain data.

## Preferred Request Flow

```text
Client
  ↓
API URL
  ↓
View
  ↓
Serializer validation
  ↓
Service / Selector
  ↓
Model / ORM
  ↓
Database
```

## Important Principle

Keep views thin.

Bad:

```python
def post(self, request):
    # 100 lines of order creation logic
```

Preferred:

```python
def post(self, request):
    serializer.is_valid(raise_exception=True)

    order = create_order(
        user=request.user,
        data=serializer.validated_data,
    )

    return success_response(...)
```

## Domain Boundaries

A domain should expose clear interfaces.

For example:

```python
from apps.orders.services.order_service import create_order
```

Prefer calling a service over manipulating another domain's models directly throughout the codebase.

## Shared Code

`common/` contains genuinely reusable infrastructure.

Examples:

```text
common/
├── exceptions/
├── responses.py
├── pagination.py
├── middleware.py
└── authentication.py
```

Do not put domain-specific logic in `common/`.

## API Versioning

Version APIs at the domain level:

```text
apps/orders/api/v1/
apps/orders/api/v2/
```

Breaking changes require a new API version.

## Scalability

This architecture allows teams to work independently:

```text
Developer A → apps/authentication/
Developer B → apps/products/
Developer C → apps/orders/
Developer D → apps/payments/
```

The goal is not to eliminate dependencies between domains. The goal is to make those dependencies explicit and controlled.
