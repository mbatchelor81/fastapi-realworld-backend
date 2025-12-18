---
name: New Feature
description: Create a new feature using test-driven development
---

# Create a New Feature

This workflow guides you through building a new feature with TDD principles.

## Step 1: Define the Feature
Describe the feature you want to build. I'll help you:
- Clarify requirements
- Identify affected components
- Plan the implementation approach

## Step 2: Create a Specification
Generate a technical spec including:
- API endpoints (if applicable)
- Data models and schemas
- Business logic requirements
- Edge cases to handle

## Step 3: Write Test Cases
Before implementation, create tests for:
- Happy path scenarios
- Error conditions
- Edge cases
- Integration points

## Step 4: Implement the Feature
Build the feature following the project structure:
- Domain models in `conduit/domain/`
- Repository interfaces and implementations
- Service layer logic
- API routes in `conduit/api/routes/`

## Step 5: Run Tests and Iterate
```bash
pytest tests/ -v --tb=short
```

Fix any failing tests and refine the implementation.

## Step 6: Review
Summarize what was built and confirm all tests pass.

What feature would you like to build?
