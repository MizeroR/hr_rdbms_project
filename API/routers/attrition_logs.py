"""
Attrition Log CRUD endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from API.models import AttritionLogCreate, AttritionLogResponse
from API.database import sqlite_db, mongodb_db
from datetime import datetime, timezone

router = APIRouter()

# SQLite CRUD Operations

@router.post("/sqlite", response_model=AttritionLogResponse, status_code=201)
def create_attrition_log_sqlite(log: AttritionLogCreate):
    """Create a new attrition log in SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO AttritionLog (employee_id, attrition_status)
            VALUES (?, ?)
        """, (log.employee_id, log.attrition_status))
        conn.commit()
        
        log_id = cur.lastrowid
        cur.execute("SELECT * FROM AttritionLog WHERE log_id = ?", (log_id,))
        row = cur.fetchone()
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite", response_model=List[AttritionLogResponse])
def get_attrition_logs_sqlite(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    employee_id: int = None
):
    """Get all attrition logs from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        
        if employee_id:
            cur.execute("""
                SELECT * FROM AttritionLog 
                WHERE employee_id = ?
                ORDER BY log_date DESC
                LIMIT ? OFFSET ?
            """, (employee_id, limit, skip))
        else:
            cur.execute("""
                SELECT * FROM AttritionLog 
                ORDER BY log_date DESC
                LIMIT ? OFFSET ?
            """, (limit, skip))
        
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite/{log_id}", response_model=AttritionLogResponse)
def get_attrition_log_sqlite(log_id: int):
    """Get a specific attrition log by ID from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM AttritionLog WHERE log_id = ?", (log_id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Attrition log {log_id} not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.delete("/sqlite/{log_id}", status_code=204)
def delete_attrition_log_sqlite(log_id: int):
    """Delete an attrition log from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM AttritionLog WHERE log_id = ?", (log_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Attrition log {log_id} not found")
        
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# MongoDB CRUD Operations

@router.post("/mongodb", status_code=201)
def create_attrition_log_mongodb(log: AttritionLogCreate):
    """Create a new attrition log in MongoDB database"""
    try:
        db = mongodb_db.get_db()
        log_dict = log.dict()
        log_dict["log_date"] = datetime.now(timezone.utc)
        
        result = db.AttritionLog.insert_one(log_dict)
        log_dict["_id"] = str(result.inserted_id)
        log_dict["log_date"] = log_dict["log_date"].isoformat()
        return log_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb")
def get_attrition_logs_mongodb(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    employee_id: int = None
):
    """Get all attrition logs from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        query = {}
        
        if employee_id:
            query["employee_id"] = employee_id
        
        logs = list(db.AttritionLog.find(query).sort("log_date", -1).skip(skip).limit(limit))
        
        for log in logs:
            log["_id"] = str(log["_id"])
            if isinstance(log.get("log_date"), datetime):
                log["log_date"] = log["log_date"].isoformat()
        
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb/{log_id}")
def get_attrition_log_mongodb(log_id: str):
    """Get a specific attrition log by ID from MongoDB database"""
    try:
        from bson import ObjectId
        db = mongodb_db.get_db()
        
        log = db.AttritionLog.find_one({"_id": ObjectId(log_id)})
        
        if log is None:
            raise HTTPException(status_code=404, detail=f"Attrition log {log_id} not found")
        
        log["_id"] = str(log["_id"])
        if isinstance(log.get("log_date"), datetime):
            log["log_date"] = log["log_date"].isoformat()
        return log
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/mongodb/{log_id}", status_code=204)
def delete_attrition_log_mongodb(log_id: str):
    """Delete an attrition log from MongoDB database"""
    try:
        from bson import ObjectId
        db = mongodb_db.get_db()
        
        result = db.AttritionLog.delete_one({"_id": ObjectId(log_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Attrition log {log_id} not found")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
