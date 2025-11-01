"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# Department Models
class DepartmentBase(BaseModel):
    department_name: str = Field(..., min_length=1, max_length=100)

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = Field(None, min_length=1, max_length=100)

class DepartmentResponse(DepartmentBase):
    department_id: int

    class Config:
        from_attributes = True

# Job Role Models
class JobRoleBase(BaseModel):
    job_role_name: str = Field(..., min_length=1, max_length=100)

class JobRoleCreate(JobRoleBase):
    pass

class JobRoleUpdate(BaseModel):
    job_role_name: Optional[str] = Field(None, min_length=1, max_length=100)

class JobRoleResponse(JobRoleBase):
    job_role_id: int

    class Config:
        from_attributes = True

# Employee Models
class EmployeeBase(BaseModel):
    age: int = Field(..., ge=18, le=100)
    attrition: str = Field(..., pattern="^(Yes|No)$")
    gender: str
    education: int = Field(..., ge=1, le=5)
    education_field: str
    marital_status: str
    business_travel: str
    distance_from_home: int = Field(..., ge=0)
    job_level: int = Field(..., ge=1, le=5)
    job_involvement: int = Field(..., ge=1, le=4)
    job_satisfaction: int = Field(..., ge=1, le=4)
    performance_rating: int = Field(..., ge=1, le=4)
    environment_satisfaction: int = Field(..., ge=1, le=4)
    work_life_balance: int = Field(..., ge=1, le=4)
    total_working_years: int = Field(..., ge=0)
    years_at_company: int = Field(..., ge=0)
    years_in_current_role: int = Field(..., ge=0)
    years_since_last_promotion: int = Field(..., ge=0)
    years_with_curr_manager: int = Field(..., ge=0)
    hourly_rate: int = Field(..., ge=0)
    monthly_income: int = Field(..., ge=0)
    monthly_rate: int = Field(..., ge=0)
    daily_rate: int = Field(..., ge=0)
    num_companies_worked: int = Field(..., ge=0)
    stock_option_level: int = Field(..., ge=0, le=3)
    over_time: str = Field(..., pattern="^(Yes|No)$")
    over18: str = Field(..., pattern="^(Y|N)$")
    percent_salary_hike: int = Field(..., ge=0)
    department_id: int
    job_role_id: int

class EmployeeCreate(EmployeeBase):
    employee_id: int

class EmployeeUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=18, le=100)
    attrition: Optional[str] = Field(None, pattern="^(Yes|No)$")
    gender: Optional[str] = None
    education: Optional[int] = Field(None, ge=1, le=5)
    education_field: Optional[str] = None
    marital_status: Optional[str] = None
    business_travel: Optional[str] = None
    distance_from_home: Optional[int] = Field(None, ge=0)
    job_level: Optional[int] = Field(None, ge=1, le=5)
    job_involvement: Optional[int] = Field(None, ge=1, le=4)
    job_satisfaction: Optional[int] = Field(None, ge=1, le=4)
    performance_rating: Optional[int] = Field(None, ge=1, le=4)
    environment_satisfaction: Optional[int] = Field(None, ge=1, le=4)
    work_life_balance: Optional[int] = Field(None, ge=1, le=4)
    total_working_years: Optional[int] = Field(None, ge=0)
    years_at_company: Optional[int] = Field(None, ge=0)
    years_in_current_role: Optional[int] = Field(None, ge=0)
    years_since_last_promotion: Optional[int] = Field(None, ge=0)
    years_with_curr_manager: Optional[int] = Field(None, ge=0)
    hourly_rate: Optional[int] = Field(None, ge=0)
    monthly_income: Optional[int] = Field(None, ge=0)
    monthly_rate: Optional[int] = Field(None, ge=0)
    daily_rate: Optional[int] = Field(None, ge=0)
    num_companies_worked: Optional[int] = Field(None, ge=0)
    stock_option_level: Optional[int] = Field(None, ge=0, le=3)
    over_time: Optional[str] = Field(None, pattern="^(Yes|No)$")
    over18: Optional[str] = Field(None, pattern="^(Y|N)$")
    percent_salary_hike: Optional[int] = Field(None, ge=0)
    department_id: Optional[int] = None
    job_role_id: Optional[int] = None

class EmployeeResponse(EmployeeBase):
    employee_id: int

    class Config:
        from_attributes = True

# Attrition Log Models
class AttritionLogBase(BaseModel):
    employee_id: int
    attrition_status: str = Field(..., pattern="^(Yes|No)$")

class AttritionLogCreate(AttritionLogBase):
    pass

class AttritionLogResponse(AttritionLogBase):
    log_id: int
    log_date: str

    class Config:
        from_attributes = True
