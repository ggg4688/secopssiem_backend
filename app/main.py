from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.init_db import init_db

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
    "https://secopssiem.vercel.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(auth_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")
app.include_router(incidents_router, prefix="/api")
app.include_router(users_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


# 🔐 ADD THIS BLOCK
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="SecOps SIEM API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
