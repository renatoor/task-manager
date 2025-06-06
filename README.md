# Task Manager

A **FastAPI** application leveraging **PostgreSQL** (with **SQLite** for testing), **Redis**, **Celery** for background tasks, and **fastapi-limiter** for rate limiting. The app is containerized using **Docker Compose** for easy setup and deployment.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Configuration & Good Practices](#configuration--good-practices)
- [Key Implementation Decisions](#key-implementation-decisions)
- [Testing](#testing)

---

## Features

- RESTful API endpoints built with FastAPI
- **Rate limiting** via `fastapi-limiter` and Redis
- **Background job processing** with Celery and Redis as the broker
- Persistent storage with **PostgreSQL** (and **SQLite** for testing)
- OpenAPI/Swagger UI for interactive API docs

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/) (production) / [SQLite](https://www.sqlite.org/) (testing)
- [Redis](https://redis.io/) (caching, rate limiting, Celery broker)
- [fastapi-limiter](https://github.com/long2ice/fastapi-limiter)
- [Celery](https://docs.celeryproject.org/)
- [Docker Compose](https://docs.docker.com/compose/)
- [uv](https://docs.astral.sh/uv/) for dependency management

---

## Setup Instructions

### 1. Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2. Clone the Repository

```bash
git clone https://github.com/renatoor/task-manager.git
cd task-manager
```

### 3. Start the Services

```bash
docker compose up --build
```

This command will start:
- FastAPI app (default at `http://localhost:8000`)
- PostgreSQL database
- Redis server
- Celery worker

---

## API Documentation

After starting the app, access interactive API docs at:

- **Swagger UI:** [`http://localhost:8000/docs`](http://localhost:8000/docs)

OpenAPI schema is automatically generated by FastAPI.

---

## Configuration & Good Practices

### Dependency Management

- All Python dependencies are managed via `uv` in `pyproject.toml`.

### Rate Limiting

- Configured with `fastapi-limiter`, using Redis as the backend.

### Background Jobs

- Celery worker is started automatically via Docker Compose.
- Tasks are submitted via API endpoints and processed asynchronously.

---

## Key Implementation Decisions

1. **Containerization:**  
   Using Docker Compose ensures all services (app, DB, Redis, Celery) run in isolated, reproducible environments.

2. **Database:**  
   PostgreSQL is used in production for robustness; SQLite is used for faster, lightweight testing.

3. **Rate Limiting:**  
   `fastapi-limiter` in conjunction with Redis is chosen for distributed and scalable rate-limiting.

4. **Background Processing:**  
   Celery enables offloading long-running or async tasks without blocking API requests.

5. **Clean Architecture**:
   The project follows Clean Architecture principles to ensure separation of concerns, maintainability, and testability:

6. **Testing:**  
   The application supports easy switching to SQLite for unit tests to speed up CI pipelines.

---

## Testing

To run tests:

```bash
uv run pytest
```

