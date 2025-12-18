---
name: Run Tests
description: Execute tests and fix any failures
---

# Run Tests and Fix

This workflow runs the test suite and helps resolve any failures.

## Step 1: Run All Tests
```bash
pytest tests/ -v
```

## Step 2: Analyze Failures
For any failing tests, I will:
- Identify the root cause
- Determine if it's a test issue or implementation bug
- Propose a fix

## Step 3: Fix Issues
Apply fixes to either:
- The test if expectations are incorrect
- The implementation if there's a bug

## Step 4: Re-run Tests
Verify all tests pass after fixes:
```bash
pytest tests/ -v
```

## Step 5: Coverage Report (Optional)
Generate a coverage report:
```bash
pytest tests/ --cov=conduit --cov-report=term-missing
```

Would you like me to run the tests now?
