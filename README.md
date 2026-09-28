# Dabbawala Order API

Dabbawala Order API is a lightweight backend service built with FastAPI to simulate a food delivery order management system. The project allows users to create orders, track them through different delivery stages, and generate daily operational insights.

The goal of this project was to practice building production-style REST APIs using FastAPI, SQLModel, and SQLite while following a clean and scalable project structure. It demonstrates API routing, database integration, dependency injection, filtering, and basic analytics endpoints.

## Tech Stack

- FastAPI
- SQLModel
- SQLite
- Uvicorn

## Key Features

- Create and manage food delivery orders
- Filter orders by status and date
- Generate daily order statistics
- Interactive API documentation with Swagger UI

## Run

```bash
uvicorn main:app --reload
