from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables, get_session
from routes.reviews import router as reviews_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    # Create database tables on startup
    create_tables()
    yield
    # Perform any cleanup tasks here if needed
    print("Application shutdown. Cleanup tasks can be performed here.")


app = FastAPI(
    title="Rangmanch Reviews API",
    description="This is a simple API for Rangmanch Reviews",
    lifespan=lifespan
)

app.include_router(reviews_router)
@app.get("/")
async def root():
    return {"message": "Welcome to the Rangmanch Reviews API!"} 
