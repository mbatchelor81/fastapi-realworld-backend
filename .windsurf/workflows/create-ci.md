---
name: Create CI
description: Set up GitHub Actions for linting and testing
---

# Create CI/CD Pipeline

This workflow helps you set up automated checks with GitHub Actions.

## Step 1: Create CI Requirements
Create a `requirements-ci.txt` with linting tools:
- black (code formatting)
- ruff (fast linting)
- mypy (type checking)

## Step 2: Create GitHub Action
Generate a workflow file at `.github/workflows/lint.yml` that:
- Triggers on push to `dev/*` branches and pull requests
- Sets up Python environment
- Installs dependencies
- Runs linting checks

## Step 3: Configure Linters
Create configuration files as needed:
- `pyproject.toml` for black and ruff settings
- `mypy.ini` or pyproject.toml section for mypy

## Step 4: Test Locally
Run the linters locally to verify configuration:
```bash
black --check conduit/
ruff check conduit/
mypy conduit/
```

## Step 5: Commit and Push
Commit the CI configuration and push to trigger the workflow.

Would you like me to start creating the CI pipeline?
