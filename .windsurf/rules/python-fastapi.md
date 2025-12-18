---
trigger: glob
globs: conduit/**/*.py
description: Use this when working on any python file in this project
---
# Python & FastAPI Best Practices

## Type Hints & Validation
- Use type hints for **all** function parameters and return values
- Use Pydantic models for request/response validation
- Leverage `Optional`, `Union`, and generics from `typing` module
- Enable strict mode in Pydantic for better validation

## API Design
- Use appropriate HTTP methods with path operation decorators (`@app.get`, `@app.post`, etc.)
- Use dependency injection for shared logic (database sessions, auth, config)
- Group related endpoints using `APIRouter`
- Return appropriate HTTP status codes (201 for creation, 204 for deletion)

## Code Structure
- Follow domain-driven design patterns as established in `conduit/`
- Separate concerns: `api/` for routes, `domain/` for business logic, `infrastructure/` for data access
- Use DTOs for data transfer between layers
- Keep route handlers thin—delegate to services

## Async Patterns
- Use `async def` for I/O-bound operations
- Use `await` for all async calls
- Prefer `asyncio.gather()` for concurrent operations
- Use async context managers for resource management

## Error Handling
- Create custom exception classes inheriting from `HTTPException`
- Use exception handlers for consistent error responses
- Return structured error responses with detail messages
- Log errors with appropriate severity levels using `structlog`

## Database (SQLAlchemy)
- Use async sessions with `aiosqlite`
- Define models with proper relationships and constraints
- Use repository pattern for data access abstraction
- Always use parameterized queries to prevent SQL injection

## Testing
- Use `pytest` with `pytest-asyncio` for async tests
- Mock external dependencies
- Test edge cases and error conditions
- Aim for high coverage on business logic

## Code Style
- Follow PEP 8 conventions
- Use early returns to reduce nesting
- Add docstrings to public functions and classes
- Keep functions focused and under 20 lines when possible
