# ![RealWorld Example App](.github/assets/logo.png)

# Windsurf Demo Project

This is a hands-on demo project showcasing **Windsurf's AI-powered development capabilities** using a real-world FastAPI + Next.js application.

> Based on the [RealWorld](https://github.com/gothinkster/realworld) spec — a Python/FastAPI codebase with CRUD, auth, middlewares, and advanced patterns.

---

## Getting Started

Use these Windsurf workflows to get oriented and set up:

| Workflow | Command | Description |
|----------|---------|-------------|
| **Demo Overview** | `/demo` | Introduction to the project and what you'll experience |
| **Setup** | `/setup` | Configure your development environment and run the app |
| **Run Tests** | `/run-tests` | Execute the test suite and fix any failures |

**Start here:** Type `/demo` in Windsurf to get an overview, then `/setup` to get the application running locally.

---

## Hands-On Exercises

After setup, explore these exercises to see Windsurf in action. **Note:** Workflows exist for these exercises but are intended as reference — try working through them manually first to experience Windsurf's capabilities.

### 1. Refactoring — Codebase Exploration

**Goal:** Remove dead code (v1/v2 API duplication) from the article service layer.

**What you'll learn:**
- How Cascade navigates and understands complex codebases
- Identifying unused code paths and dependencies
- Safe refactoring with test verification

**Try it yourself:**
1. Ask Cascade to find all methods with `_v1` and `_v2` suffixes
2. Explore which methods are actually called from API routes
3. Remove dead code and rename methods
4. Verify changes with the test suite

*Reference workflow: `/refactor-dead-code`*

---

### 2. New Feature Development — Spec-Driven TDD

**Goal:** Build a new Bookmarks feature from scratch using test-driven development.

**What you'll learn:**
- Creating functional and technical specifications with Windsurf
- Writing tests before implementation (TDD)
- Full-stack feature development with Cascade guidance

**Try it yourself:**
1. Ask Cascade to help define requirements for a Bookmarks feature
2. Generate a technical spec covering API endpoints, data models, and edge cases
3. Write failing tests first based on the spec
4. Implement the feature to make tests pass

*Reference workflow: `/new-feature`*

---

### 3. Creating CI — Adding Determinism to AI Code

**Goal:** Set up GitHub Actions for automated linting and testing.

**What you'll learn:**
- How Windsurf helps add quality gates to AI-generated code
- Creating linting configurations (black, ruff, mypy)
- Building CI/CD pipelines that enforce code standards

**Try it yourself:**
1. Ask Cascade to set up linting tools for the project
2. Create a GitHub Actions workflow for automated checks
3. Configure linters to match project conventions
4. Test the pipeline locally before committing

*Reference workflow: `/create-ci`*

---

## Project Structure

```
conduit/           # Backend application
├── api/           # Routes, schemas, middlewares
├── core/          # Configuration, dependency injection
├── domain/        # DTOs, repositories, services
└── infrastructure/# Database models, repository implementations

frontend/          # Next.js frontend application
tests/             # Backend test suite
```

## Prerequisites

- Python 3.12
- Node.js (for frontend)

## Create Python Virtual Environment
```bash
python -m venv .venv # python3.12 -m venv .venv if multiple versions available
source .venv/bin/activate
pip install -r requirements.txt
```

## Seed demo data 
```bash
python seed_data.py           # First run
python seed_data.py --force   # Overwrite existing data
```

## Quick Reference

| Task | Command |
|------|---------|
| Run backend | `uvicorn conduit.app:app --reload` |
| Run frontend | `cd frontend && npm run dev` |
| Run tests | `pytest tests/ -v` |
| API docs (Swagger) | http://localhost:8000/ |
| Frontend | http://localhost:3000 |

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [RealWorld Spec](https://github.com/gothinkster/realworld)
- [Windsurf Documentation](https://docs.windsurf.com/)

