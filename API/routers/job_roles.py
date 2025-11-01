"""
Job Role CRUD endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from API.models import JobRoleCreate, JobRoleUpdate, JobRoleResponse
from API.database import sqlite_db, mongodb_db
import sqlite3

router = APIRouter()

# SQLite CRUD Operations

@router.post("/sqlite", response_model=JobRoleResponse, status_code=201)
def create_job_role_sqlite(job_role: JobRoleCreate):
    """Create a new job role in SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO JobRoles (job_role_name) VALUES (?)", (job_role.job_role_name,))
        conn.commit()
        return {"job_role_id": cur.lastrowid, "job_role_name": job_role.job_role_name}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Job role already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite", response_model=List[JobRoleResponse])
def get_job_roles_sqlite(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all job roles from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM JobRoles LIMIT ? OFFSET ?", (limit, skip))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite/{job_role_id}", response_model=JobRoleResponse)
def get_job_role_sqlite(job_role_id: int):
    """Get a specific job role by ID from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM JobRoles WHERE job_role_id = ?", (job_role_id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Job role {job_role_id} not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.put("/sqlite/{job_role_id}", response_model=JobRoleResponse)
def update_job_role_sqlite(job_role_id: int, job_role: JobRoleUpdate):
    """Update a job role in SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        
        if job_role.job_role_name:
            cur.execute("UPDATE JobRoles SET job_role_name = ? WHERE job_role_id = ?",
                       (job_role.job_role_name, job_role_id))
            conn.commit()
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Job role {job_role_id} not found")
        
        cur.execute("SELECT * FROM JobRoles WHERE job_role_id = ?", (job_role_id,))
        row = cur.fetchone()
        return dict(row)
    except HTTPException:
        raise
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Job role name already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.delete("/sqlite/{job_role_id}", status_code=204)
def delete_job_role_sqlite(job_role_id: int):
    """Delete a job role from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM JobRoles WHERE job_role_id = ?", (job_role_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Job role {job_role_id} not found")
        
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# MongoDB CRUD Operations

@router.post("/mongodb", status_code=201)
def create_job_role_mongodb(job_role: JobRoleCreate):
    """Create a new job role in MongoDB database"""
    try:
        db = mongodb_db.get_db()
        
        # Check if job role already exists
        if db.JobRoles.find_one({"job_role_name": job_role.job_role_name}):
            raise HTTPException(status_code=400, detail="Job role already exists")
        
        result = db.JobRoles.insert_one(job_role.dict())
        job_role_dict = job_role.dict()
        job_role_dict["_id"] = str(result.inserted_id)
        return job_role_dict
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb")
def get_job_roles_mongodb(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all job roles from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        job_roles = list(db.JobRoles.find().skip(skip).limit(limit))
        
        for role in job_roles:
            role["_id"] = str(role["_id"])
        
        return job_roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb/{job_role_name}")
def get_job_role_mongodb(job_role_name: str):
    """Get a specific job role by name from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        job_role = db.JobRoles.find_one({"job_role_name": job_role_name})
        
        if job_role is None:
            raise HTTPException(status_code=404, detail=f"Job role '{job_role_name}' not found")
        
        job_role["_id"] = str(job_role["_id"])
        return job_role
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/mongodb/{job_role_name}")
def update_job_role_mongodb(job_role_name: str, job_role: JobRoleUpdate):
    """Update a job role in MongoDB database"""
    try:
        db = mongodb_db.get_db()
        update_data = job_role.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.JobRoles.update_one(
            {"job_role_name": job_role_name},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Job role '{job_role_name}' not found")
        
        updated_role = db.JobRoles.find_one({"job_role_name": job_role.job_role_name or job_role_name})
        updated_role["_id"] = str(updated_role["_id"])
        return updated_role
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/mongodb/{job_role_name}", status_code=204)
def delete_job_role_mongodb(job_role_name: str):
    """Delete a job role from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        result = db.JobRoles.delete_one({"job_role_name": job_role_name})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Job role '{job_role_name}' not found")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
