import os
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import db_health
from app.routes import (
    magnetometer,
    prospectivity,
    satellite,
    samples,
)


app = FastAPI(
    title="GoldHunterAI v5 API",
    description="Backend API for GoldHunterAI v5 — Satellite Database",
    version="1.0.0",
)


origins = [
    item.strip()
    for item in os.getenv("CORS_ORIGINS", "*").split(",")
    if item.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "GoldHunterAI v5 API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    try:
        database = db_health()

        return {
            "status": "ok",
            "api": "ok",
            "database