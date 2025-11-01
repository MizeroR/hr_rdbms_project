"""
Department CRUD endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from API.models import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from API.database import sqlite_db, mongodb_db
import sqlite3

router = APIRouter()

# SQLite CRUD Operations

@router.post("/sqlite", response_model=DepartmentResponse, status_code=201)
def create_department_sqlite(department: DepartmentCreate):
    """Create a new department in SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Departments (department_name) VALUES (?)", (department.department_name,))
        conn.commit()
        return {"department_id": cur.lastrowid, "department_name": department.department_name}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Department already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite", response_model=List[DepartmentResponse])
def get_departments_sqlite(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all departments from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Departments LIMIT ? OFFSET ?", (limit, skip))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite/{department_id}", response_model=DepartmentResponse)
def get_department_sqlite(department_id: int):
    """Get a specific department by ID from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Departments WHERE department_id = ?", (department_id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Department {department_id} not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.put("/sqlite/{department_id}", response_model=DepartmentResponse)
def update_department_sqlite(department_id: int, department: DepartmentUpdate):
    """Update a department in SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        
        if department.department_name:
            cur.execute("UPDATE Departments SET department_name = ? WHERE department_id = ?",
                       (department.department_name, department_id))
            conn.commit()
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Department {department_id} not found")
        
        cur.execute("SELECT * FROM Departments WHERE department_id = ?", (department_id,))
        row = cur.fetchone()
        return dict(row)
    except HTTPException:
        raise
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Department name already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.delete("/sqlite/{department_id}", status_code=204)
def delete_department_sqlite(department_id: int):
    """Delete a department from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Departments WHERE department_id = ?", (department_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Department {department_id} not found")
        
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# MongoDB CRUD Operations

@router.post("/mongodb", status_code=201)
def create_department_mongodb(department: DepartmentCreate):
    """Create a new department in MongoDB database"""
    try:
        db = mongodb_db.get_db()
        
        # Check if department already exists
        if db.Departments.find_one({"department_name": department.department_name}):
            raise HTTPException(status_code=400, detail="Department already exists")
        
        result = db.Departments.insert_one(department.dict())
        department_dict = department.dict()
        department_dict["_id"] = str(result.inserted_id)
        return department_dict
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb")
def get_departments_mongodb(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all departments from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        departments = list(db.Departments.find().skip(skip).limit(limit))
        
        for dept in departments:
            dept["_id"] = str(dept["_id"])
        
        return departments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb/{department_name}")
def get_department_mongodb(department_name: str):
    """Get a specific department by name from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        department = db.Departments.find_one({"department_name": department_name})
        
        if department is None:
            raise HTTPException(status_code=404, detail=f"Department '{department_name}' not found")
        
        department["_id"] = str(department["_id"])
        return department
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/mongodb/{department_name}")
def update_department_mongodb(department_name: str, department: DepartmentUpdate):
    """Update a department in MongoDB database"""
    try:
        db = mongodb_db.get_db()
        update_data = department.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.Departments.update_one(
            {"department_name": department_name},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Department '{department_name}' not found")
        
        updated_dept = db.Departments.find_one({"department_name": department.department_name or department_name})
        updated_dept["_id"] = str(updated_dept["_id"])
        return updated_dept
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/mongodb/{department_name}", status_code=204)
def delete_department_mongodb(department_name: str):
    """Delete a department from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        result = db.Departments.delete_one({"department_name": department_name})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Department '{department_name}' not found")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
