# ![RealWorld Example App](.github/assets/logo.png)


> ### Python / FastAPI codebase containing real world examples (CRUD, auth, middlewares advanced patterns, etc.) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged backend application built with **[FastAPI](https://fastapi.tiangolo.com/)** including CRUD operations, authentication, routing, and more.

For more information on how this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


## Description
This project is a Python-based API that uses SQLite as its database for simple local development.
It is built with FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3 based on standard Python type hints.

## Prerequisites
- Python 3.12
- Node.js (for frontend)

## Quick Start

### Backend

1. Create a virtual environment and install dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy the example environment file:

```sh
cp .env.example .env
```

3. Run the backend:

```sh
python app.py
```

The API will be available at http://localhost:8000. The SQLite database will be automatically created on first run.

### Frontend

1. Install dependencies:

```sh
cd frontend
npm install
```

2. Run the frontend:

```sh
npm run dev
```

The frontend will be available at http://localhost:3000.

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
DATABASE_URL=sqlite+aiosqlite:///./conduit.db
```

## Run tests

Tests for this project are defined in the ``tests/`` folder.

Run the tests:

```sh
APP_ENV=test python -m pytest -v ./tests
```

Or run the tests with coverage:

```sh
APP_ENV=test python -m pytest --cov=./conduit ./tests
```

## Run Conduit Postman collection tests

For running tests for local application:

```sh
APIURL=http://127.0.0.1:8000/api ./postman/run-api-tests.sh
```

## Web routes

All routes are available on / or /redoc paths with Swagger or ReDoc.

## Advanced: Using Docker (Optional)

If you prefer to use Docker, you can use the docker-compose setup:

```sh
docker-compose up -d --build
```

The Docker setup uses the same SQLite database configuration as local development.
