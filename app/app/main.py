from typing import Any
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title="eGator Finance", openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(GZipMiddleware, minimum_size=1000)

# If this works, move to env vars
def get_origins():
    if settings.ENVIRONMENT == "production":
        return ["https://egatorfinance.com", "https://www.egatorfinance.com"]
    if settings.ENVIRONMENT == "staging":
        return ["https://egator-verification-system-frontend-o67hbk3fqa-uc.a.run.app"]
    if settings.ENVIRONMENT == "local":
        return ["http://localhost:3000", "http://localhost:8000", "http://localhost:8080"]


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-HTTP-Method-Override",
            "Accept",
            "Origin",
            "User-Agent",
            "DNT",
            "Cache-Control",
            "Keep-Alive",
            "X-Requested-With",
            "If-Modified-Since",
            "Cache-Control",
            "Content-Type",
            "Content-Range",
            "Range",
        ],
    )

@app.get("/health", response_model=Any)
def health():
    return {"msg": "OK"}


app.include_router(api_router, prefix=settings.API_V1_STR)
