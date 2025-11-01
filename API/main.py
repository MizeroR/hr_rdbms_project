"""
FastAPI application for HR Employee Attrition Database
Provides CRUD operations for both SQLite and MongoDB
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from API.routers import employees, departments, job_roles, attrition_logs
from API.database import sqlite_db, mongodb_db

app = FastAPI(
    title="HR Employee Attrition API",
    description="CRUD API for HR Employee Attrition Database (SQLite & MongoDB)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
app.include_router(departments.router, prefix="/api/v1/departments", tags=["Departments"])
app.include_router(job_roles.router, prefix="/api/v1/jobroles", tags=["Job Roles"])
app.include_router(attrition_logs.router, prefix="/api/v1/attrition-logs", tags=["Attrition Logs"])

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "HR Employee Attrition API",
        "version": "1.0.0",
        "databases": ["SQLite", "MongoDB"],
        "endpoints": {
            "employees": "/api/v1/employees",
            "departments": "/api/v1/departments",
            "job_roles": "/api/v1/jobroles",
            "attrition_logs": "/api/v1/attrition-logs"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    sqlite_status = "connected" if sqlite_db.test_connection() else "disconnected"
    mongo_status = "connected" if mongodb_db.test_connection() else "disconnected"
    
    return {
        "status": "healthy",
        "databases": {
            "sqlite": sqlite_status,
            "mongodb": mongo_status
        }
    }

@app.on_event("startup")
async def startup_event():
    """Initialize database connections on startup"""
    print("🚀 Starting up HR Attrition API...")
    print(f"📊 SQLite: {sqlite_db.test_connection()}")
    print(f"📊 MongoDB: {mongodb_db.test_connection()}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    mongodb_db.close()
    print("👋 Shutting down HR Attrition API...")
