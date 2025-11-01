"""
Employee CRUD endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from API.models import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from API.database import sqlite_db, mongodb_db
import sqlite3

router = APIRouter()

# SQLite CRUD Operations

@router.post("/sqlite", response_model=EmployeeResponse, status_code=201)
def create_employee_sqlite(employee: EmployeeCreate):
    """Create a new employee in SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Employees (
                employee_id, age, attrition, gender, education, education_field,
                marital_status, business_travel, distance_from_home, job_level,
                job_involvement, job_satisfaction, performance_rating,
                environment_satisfaction, work_life_balance, total_working_years,
                years_at_company, years_in_current_role, years_since_last_promotion,
                years_with_curr_manager, hourly_rate, monthly_income, monthly_rate,
                daily_rate, num_companies_worked, stock_option_level, over_time,
                over18, percent_salary_hike, department_id, job_role_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee.employee_id, employee.age, employee.attrition, employee.gender,
            employee.education, employee.education_field, employee.marital_status,
            employee.business_travel, employee.distance_from_home, employee.job_level,
            employee.job_involvement, employee.job_satisfaction, employee.performance_rating,
            employee.environment_satisfaction, employee.work_life_balance, employee.total_working_years,
            employee.years_at_company, employee.years_in_current_role, employee.years_since_last_promotion,
            employee.years_with_curr_manager, employee.hourly_rate, employee.monthly_income,
            employee.monthly_rate, employee.daily_rate, employee.num_companies_worked,
            employee.stock_option_level, employee.over_time, employee.over18,
            employee.percent_salary_hike, employee.department_id, employee.job_role_id
        ))
        conn.commit()
        return employee.dict()
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Employee with ID {employee.employee_id} already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite", response_model=List[EmployeeResponse])
def get_employees_sqlite(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    attrition: Optional[str] = Query(None, pattern="^(Yes|No)$"),
    department_id: Optional[int] = None
):
    """Get all employees from SQLite database with optional filtering"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM Employees WHERE 1=1"
        params = []
        
        if attrition:
            query += " AND attrition = ?"
            params.append(attrition)
        if department_id:
            query += " AND department_id = ?"
            params.append(department_id)
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        cur.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/sqlite/{employee_id}", response_model=EmployeeResponse)
def get_employee_sqlite(employee_id: int):
    """Get a specific employee by ID from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Employees WHERE employee_id = ?", (employee_id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.put("/sqlite/{employee_id}", response_model=EmployeeResponse)
def update_employee_sqlite(employee_id: int, employee: EmployeeUpdate):
    """Update an employee in SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        params = []
        for field, value in employee.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = ?")
                params.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        params.append(employee_id)
        query = f"UPDATE Employees SET {', '.join(update_fields)} WHERE employee_id = ?"
        
        cur.execute(query, params)
        conn.commit()
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
        # Fetch and return updated employee
        cur.execute("SELECT * FROM Employees WHERE employee_id = ?", (employee_id,))
        row = cur.fetchone()
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.delete("/sqlite/{employee_id}", status_code=204)
def delete_employee_sqlite(employee_id: int):
    """Delete an employee from SQLite database"""
    conn = sqlite_db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Employees WHERE employee_id = ?", (employee_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# MongoDB CRUD Operations

@router.post("/mongodb", status_code=201)
def create_employee_mongodb(employee: EmployeeCreate):
    """Create a new employee in MongoDB database"""
    try:
        db = mongodb_db.get_db()
        employee_dict = employee.dict()
        
        # Check if employee already exists
        if db.Employees.find_one({"employee_id": employee.employee_id}):
            raise HTTPException(status_code=400, detail=f"Employee with ID {employee.employee_id} already exists")
        
        result = db.Employees.insert_one(employee_dict)
        employee_dict["_id"] = str(result.inserted_id)
        return employee_dict
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb")
def get_employees_mongodb(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    attrition: Optional[str] = Query(None, pattern="^(Yes|No)$")
):
    """Get all employees from MongoDB database with optional filtering"""
    try:
        db = mongodb_db.get_db()
        query = {}
        
        if attrition:
            query["attrition"] = attrition
        
        employees = list(db.Employees.find(query).skip(skip).limit(limit))
        
        # Convert ObjectId to string
        for emp in employees:
            emp["_id"] = str(emp["_id"])
        
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mongodb/{employee_id}")
def get_employee_mongodb(employee_id: int):
    """Get a specific employee by ID from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        employee = db.Employees.find_one({"employee_id": employee_id})
        
        if employee is None:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
        employee["_id"] = str(employee["_id"])
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/mongodb/{employee_id}")
def update_employee_mongodb(employee_id: int, employee: EmployeeUpdate):
    """Update an employee in MongoDB database"""
    try:
        db = mongodb_db.get_db()
        update_data = employee.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.Employees.update_one(
            {"employee_id": employee_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
        # Fetch and return updated employee
        updated_employee = db.Employees.find_one({"employee_id": employee_id})
        updated_employee["_id"] = str(updated_employee["_id"])
        return updated_employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/mongodb/{employee_id}", status_code=204)
def delete_employee_mongodb(employee_id: int):
    """Delete an employee from MongoDB database"""
    try:
        db = mongodb_db.get_db()
        result = db.Employees.delete_one({"employee_id": employee_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
