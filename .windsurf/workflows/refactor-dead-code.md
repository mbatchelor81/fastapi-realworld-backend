---
name: Refactor Dead Code
description: Identify and remove v1/v2 API duplication in the codebase
---

# Refactor: Remove v1/v2 Duplication

This workflow guides you through removing dead code from the article service layer.

## Step 1: Identify Dead Code
Analyze the article service and repository for v1 methods that are no longer used:
- Search for `_v1` and `_v2` method suffixes in `conduit/domain/services/`
- Check which methods are actually called from the API routes

## Step 2: Remove v1 Methods
For each identified v1 method:
1. Remove from the interface in `conduit/domain/repositories/`
2. Remove implementation from `conduit/infrastructure/repositories/`
3. Remove from the service layer in `conduit/domain/services/`

## Step 3: Rename v2 Methods
Rename remaining v2 methods to their original names:
- Remove the `_v2` suffix
- Update all call sites

## Step 4: Verify Changes
Run the test suite to ensure nothing is broken:
```bash
pytest tests/ -v
```

## Step 5: Review
Summarize the changes made and confirm all tests pass.

Would you like me to start by identifying the dead code in the article service?
