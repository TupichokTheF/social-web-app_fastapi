from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from api.api_router import api_router
from database import database

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await database.init_database()
    yield
    await database.dispose_database()

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)