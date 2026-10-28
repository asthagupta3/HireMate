from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import users , resume

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HireMate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(resume.router)

@app.get("/")
def home():
    return {"message": "HireMate backend running"}