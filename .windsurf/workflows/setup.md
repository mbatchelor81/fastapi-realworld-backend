---
name: Project Setup
description: Set up the development environment for the FastAPI backend
---

# Project Setup

Follow these steps to set up the development environment:

## Step 1: Create Virtual Environment (Terminal 1)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Step 2: Install Backend Dependencies (Terminal 1)
```bash
pip install -r requirements.txt
```

## Step 3: Configure Environment (Terminal 1)
Copy the example environment file and configure as needed:
```bash
cp .env.example .env
```

## Step 4: Seed the Database (Terminal 1)
Populate the database with sample data:
```bash
python seed_data.py
```

This creates sample users, articles, tags, and comments. Login credentials will be displayed.

## Step 5: Run the Backend (Terminal 1)
Start the FastAPI server:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## Step 6: Install Frontend Dependencies (Terminal 2)
Open a **new terminal** and run:
```bash
cd frontend
npm install
```

## Step 7: Run the Frontend (Terminal 2)
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Step 8: Verify Setup (Terminal 3)
Open a **third terminal** to run tests or interact with the API:
- Backend API docs: `http://localhost:8000/docs`
- Frontend app: `http://localhost:3000`
- Run backend tests: `pytest`

Would you like me to execute these setup steps for you?
