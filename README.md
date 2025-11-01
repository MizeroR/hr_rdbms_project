# HR Employee Attrition Database Project

## Dataset

HR Employee Attrition dataset from Kaggle - analyzing employee turnover patterns and factors.

## Project Structure

```
hr_rdbms_project/
├── README.md
├── requirements.txt
├── API/                          # FastAPI CRUD endpoints
│   ├── main.py                   # Application entry point
│   ├── database.py               # Database connections
│   ├── models.py                 # Pydantic models
│   ├── README.md                 # API documentation
│   └── routers/                  # API route handlers
│       ├── employees.py
│       ├── departments.py
│       ├── job_roles.py
│       └── attrition_logs.py
└── databases/
    ├── WA_Fn-UseC_-HR-Employee-Attrition.csv
    ├── erd/
    │   ├── diagram.md            # ERD diagram (Mermaid format)
    │   └── hr_attrition.db       # SQLite database
    ├── mongodb/
    │   └── load_to_mongodb.py    # MongoDB loader
    └── sqlite/
        ├── load_to_sqlite.py     # SQLite loader
        ├── schema.sql            # Database schema
        └── stored_procedures.py  # Stored procedures
```

## Task 1: Database Implementation ✅

### Database Schema

- **4 Tables**: Departments, JobRoles, Employees, AttritionLog
- **Primary Keys**: Defined on all tables
- **Foreign Keys**: Employees references Departments & JobRoles
- **ERD Diagram**: Available in `databases/erd/diagram.md`

### Stored Procedures & Triggers

- **Stored Procedure 1**: `get_department_attrition_stats()` - Calculate attrition statistics
- **Stored Procedure 2**: `update_employee_attrition()` - Update employee status
- **Trigger**: `log_attrition_change` - Automatically logs when attrition changes to "Yes"

### Implementation

- **SQLite** (Relational): Normalized schema with relationships
- **MongoDB** (NoSQL): Document-based collections

## Task 2: FastAPI CRUD Operations ✅

### Technology Stack

- **Framework**: FastAPI
- **Validation**: Pydantic
- **Databases**: SQLite & MongoDB

### CRUD Endpoints

All endpoints available for both SQLite and MongoDB:

#### Employees

- `POST /api/v1/employees/{sqlite|mongodb}` - Create employee
- `GET /api/v1/employees/{sqlite|mongodb}` - Read all employees
- `GET /api/v1/employees/{sqlite|mongodb}/{id}` - Read specific employee
- `PUT /api/v1/employees/{sqlite|mongodb}/{id}` - Update employee
- `DELETE /api/v1/employees/{sqlite|mongodb}/{id}` - Delete employee

#### Departments

- Full CRUD operations at `/api/v1/departments/{sqlite|mongodb}`

#### Job Roles

- Full CRUD operations at `/api/v1/jobroles/{sqlite|mongodb}`

#### Attrition Logs

- Full CRUD operations at `/api/v1/attrition-logs/{sqlite|mongodb}`

### Features

- Pagination support (skip, limit)
- Data filtering (attrition status, department, employee)
- Data validation with Pydantic models
- Automatic API documentation (Swagger/ReDoc)
- Error handling with proper HTTP status codes
- Health check endpoint

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Load Databases

```bash
# SQLite
python databases/sqlite/load_to_sqlite.py

# MongoDB (ensure MongoDB is running)
python databases/mongodb/load_to_mongodb.py
```

### 3. Run the API

```bash
uvicorn API.main:app --reload
```

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing the API

### Example: Create a Department

```bash
curl -X POST "http://localhost:8000/api/v1/departments/sqlite" \
  -H "Content-Type: application/json" \
  -d '{"department_name": "Engineering"}'
```

### Example: Get Employees with Attrition

```bash
curl "http://localhost:8000/api/v1/employees/mongodb?attrition=Yes&limit=10"
```

### Example: Update Employee

```bash
curl -X PUT "http://localhost:8000/api/v1/employees/sqlite/123" \
  -H "Content-Type: application/json" \
  -d '{"job_satisfaction": 4}'
```

## Technologies Used

- **Python 3.x**
- **SQLite** - Relational database
- **MongoDB** - NoSQL database
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **Pandas** - Data processing
- **Uvicorn** - ASGI server
