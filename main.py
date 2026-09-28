from fastapi import FastAPI
from contextlib import asynccontextmanager 
from database import create_tables
from routes.orders import router as orders_router
from routes.stats import router as stats_router
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Application startup")
    yield
    print("Application shutdown")



app = FastAPI(title = "Dabbewala",
              description = "Dabbewala is a food delivery service that connects customers with local restaurants and food providers.",
              version = "1",
              lifespan=lifespan,)  

app.include_router(orders_router)
app.include_router(stats_router)    

@app.get("/health",tags=["Health"])
def health_check():
    return {"status": "ok"}