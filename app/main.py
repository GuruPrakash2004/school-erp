from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.academics.router import router as academics_router
from app.modules.auth.router import router as auth_router

app = FastAPI(title="School ERP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(academics_router, prefix="/api/v1")
