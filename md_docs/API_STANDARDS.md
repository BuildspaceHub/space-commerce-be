# API Standards

## Base URL

All APIs are versioned.

Example:

```text
/api/v1/
```

## Resource URLs

Use resource-oriented URLs.

Preferred:

```text
GET    /api/v1/products/
GET    /api/v1/products/{id}/
POST   /api/v1/products/
PATCH  /api/v1/products/{id}/
DELETE /api/v1/products/{id}/
```

Avoid action-heavy URLs when a resource-oriented design is possible.

## Versioning

Breaking changes require a new API version.

Example:

```text
/api/v1/orders/
/api/v2/orders/
```

Non-breaking additions should not automatically create a new version.

## Validation

Validate all client input at the API boundary.

Use DRF serializers and validators.

Example:

```python
serializer = OrderCreateSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
```

## Success Response

Use the project's standard success response.

Example:

```json
{
  "statusCode": 200,
  "message": "Order retrieved successfully",
  "data": {}
}
```

## Error Response

Use the global error response format.

Example:

```json
{
  "statusCode": 404,
  "message": "Order not found",
  "error": "Not Found",
  "details": null
}
```

Validation:

```json
{
  "statusCode": 400,
  "message": "Validation failed",
  "error": "Bad Request",
  "details": {
    "email": [
      "This field is required."
    ]
  }
}
```

## HTTP Status Codes

Use status codes correctly.

Common codes:

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
429 Too Many Requests
500 Internal Server Error
```

Do not use `200` for every response.

## Pagination

Paginated endpoints must use the project's standard pagination format.

Do not create endpoint-specific pagination structures without approval.

## Filtering

Use query parameters:

```text
GET /api/v1/products/?category=electronics
GET /api/v1/products/?status=active
```

Document allowed filtering fields.

## Sorting

Use query parameters where appropriate:

```text
GET /api/v1/products/?ordering=-created_at
```

Only expose approved sortable fields.

## Authentication

Protected endpoints must enforce authentication server-side.

For bearer access tokens:

```text
Authorization: Bearer <access-token>
```

Refresh-token behavior follows the project's authentication architecture.

## Idempotency

Critical operations should support idempotency where duplicate requests could create duplicate business effects.

Examples:

- Payments
- Refunds
- Checkout
- External webhooks

## API Documentation

Every public endpoint must be documented.

Documentation should include:

- Method
- URL
- Authentication requirements
- Request body
- Query parameters
- Response
- Error responses
- Permissions
- Important business rules
