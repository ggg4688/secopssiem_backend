from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth_router,
    alerts_router,
    incidents_router,
    users_router
)

app = FastAPI(
    title="SecOps SIEM API",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "https://secopssiem.space"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")
app.include_router(incidents_router, prefix="/api")
app.include_router(users_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}