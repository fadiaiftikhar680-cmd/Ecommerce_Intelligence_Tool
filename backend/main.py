"""
backend/main.py
FastAPI Application Entry Point for Pakistan E-Commerce Intelligence Tool (Layer 3).
Provides REST API endpoints, automated Swagger documentation, database persistence,
and real-time ML-powered COD return risk scoring.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.seed_data import seed_initial_data
from backend.ml_model import ml_service
from backend.routers import (
    overview,
    events,
    products,
    pricing,
    cod_risk,
    inventory,
    intelligence
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle handler."""
    # Ensure database schema is created and seeded
    Base.metadata.create_all(bind=engine)
    seed_initial_data()
    # Pre-train or load ML model
    _ = ml_service.pipeline
    print(">> [FastAPI Backend] SQLite Database & ML Model ready.")
    yield
    print(">> [FastAPI Backend] Shutting down cleanly.")


app = FastAPI(
    title="Pakistan E-Commerce Intelligence SaaS API",
    description=(
        "Layer 3 Backend for Pakistan E-Commerce Intelligence Dashboard. "
        "Provides event calendars, winning product discovery, reverse courier margin simulations, "
        "Scikit-learn powered Cash on Delivery (COD) risk scoring, and store inventory liquidation planning."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for cross-origin requests from Streamlit or frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api prefix
app.include_router(overview.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(pricing.router, prefix="/api")
app.include_router(cod_risk.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(intelligence.router, prefix="/api")


@app.get("/health", tags=["System Health"])
def health_check():
    """Health check endpoint to verify backend operational readiness."""
    return {
        "status": "healthy",
        "service": "Pakistan E-Commerce Intelligence API",
        "version": "2.0.0",
        "database": "SQLite (Active)",
        "ml_model": "RandomForest COD Risk Classifier (Loaded)"
    }


@app.get("/", tags=["Root"])
def root_info():
    """Root info endpoint providing documentation links."""
    return {
        "message": "Welcome to Pakistan E-Commerce Intelligence SaaS Platform API",
        "documentation": "/docs",
        "interactive_redoc": "/redoc",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
