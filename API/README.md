# HR Employee Attrition API

FastAPI-based CRUD API for managing HR Employee Attrition data across SQLite and MongoDB databases.

## Features

- **Full CRUD Operations** (Create, Read, Update, Delete) for:

  - Employees
  - Departments
  - Job Roles
  - Attrition Logs

- **Dual Database Support**:

  - SQLite (Relational)
  - MongoDB (NoSQL)

- **RESTful API** with automatic documentation
- **Data Validation** using Pydantic models
- **Error Handling** with proper HTTP status codes

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Databases are Loaded

Make sure you've run the database loading scripts:

```bash
# Load SQLite database
python databases/sqlite/load_to_sqlite.py

# Load MongoDB database (ensure MongoDB is running)
python databases/mongodb/load_to_mongodb.py
```

### 3. Run the API Server

```bash
uvicorn API.main:app --reload
```

Or from the project root:

```bash
python -m uvicorn API.main:app --reload
```

The API will start at: `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

### Employees

#### SQLite

- `POST /employees/sqlite` - Create employee
- `GET /employees/sqlite` - Get all employees (with filters)
- `GET /employees/sqlite/{employee_id}` - Get employee by ID
- `PUT /employees/sqlite/{employee_id}` - Update employee
- `DELETE /employees/sqlite/{employee_id}` - Delete employee

#### MongoDB

- `POST /employees/mongodb` - Create employee
- `GET /employees/mongodb` - Get all employees (with filters)
- `GET /employees/mongodb/{employee_id}` - Get employee by ID
- `PUT /employees/mongodb/{employee_id}` - Update employee
- `DELETE /employees/mongodb/{employee_id}` - Delete employee

### Departments

#### SQLite

- `POST /departments/sqlite` - Create department
- `GET /departments/sqlite` - Get all departments
- `GET /departments/sqlite/{department_id}` - Get department by ID
- `PUT /departments/sqlite/{department_id}` - Update department
- `DELETE /departments/sqlite/{department_id}` - Delete department

#### MongoDB

- `POST /departments/mongodb` - Create department
- `GET /departments/mongodb` - Get all departments
- `GET /departments/mongodb/{department_name}` - Get department by name
- `PUT /departments/mongodb/{department_name}` - Update department
- `DELETE /departments/mongodb/{department_name}` - Delete department

### Job Roles

#### SQLite

- `POST /jobroles/sqlite` - Create job role
- `GET /jobroles/sqlite` - Get all job roles
- `GET /jobroles/sqlite/{job_role_id}` - Get job role by ID
- `PUT /jobroles/sqlite/{job_role_id}` - Update job role
- `DELETE /jobroles/sqlite/{job_role_id}` - Delete job role

#### MongoDB

- `POST /jobroles/mongodb` - Create job role
- `GET /jobroles/mongodb` - Get all job roles
- `GET /jobroles/mongodb/{job_role_name}` - Get job role by name
- `PUT /jobroles/mongodb/{job_role_name}` - Update job role
- `DELETE /jobroles/mongodb/{job_role_name}` - Delete job role

### Attrition Logs

#### SQLite

- `POST /attrition-logs/sqlite` - Create attrition log
- `GET /attrition-logs/sqlite` - Get all logs
- `GET /attrition-logs/sqlite/{log_id}` - Get log by ID
- `DELETE /attrition-logs/sqlite/{log_id}` - Delete log

#### MongoDB

- `POST /attrition-logs/mongodb` - Create attrition log
- `GET /attrition-logs/mongodb` - Get all logs
- `GET /attrition-logs/mongodb/{log_id}` - Get log by ID
- `DELETE /attrition-logs/mongodb/{log_id}` - Delete log

## Example Usage

### Create a Department (SQLite)

```bash
curl -X POST "http://localhost:8000/api/v1/departments/sqlite" \
  -H "Content-Type: application/json" \
  -d '{"department_name": "Engineering"}'
```

### Get All Employees with Attrition (MongoDB)

```bash
curl "http://localhost:8000/api/v1/employees/mongodb?attrition=Yes&limit=10"
```

### Update an Employee (SQLite)

```bash
curl -X PUT "http://localhost:8000/api/v1/employees/sqlite/123" \
  -H "Content-Type: application/json" \
  -d '{"job_satisfaction": 4, "attrition": "No"}'
```

### Delete a Department (MongoDB)

```bash
curl -X DELETE "http://localhost:8000/api/v1/departments/mongodb/Sales"
```

## Query Parameters

### Pagination

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

### Filtering (Employees)

- `attrition`: Filter by attrition status (Yes/No)
- `department_id`: Filter by department ID (SQLite only)

### Filtering (Attrition Logs)

- `employee_id`: Filter logs by employee ID

## Response Formats

### Success Response

```json
{
  "employee_id": 123,
  "age": 35,
  "gender": "Male",
  "attrition": "No",
  ...
}
```

### Error Response

```json
{
  "detail": "Employee 999 not found"
}
```

## Health Check

```bash
curl http://localhost:8000/health
```

Returns database connection status:

```json
{
  "status": "healthy",
  "databases": {
    "sqlite": "connected",
    "mongodb": "connected"
  }
}
```

## Project Structure

```
API/
├── main.py              # FastAPI application entry point
├── database.py          # Database connection handlers
├── models.py            # Pydantic models for validation
├── routers/
│   ├── __init__.py
│   ├── employees.py     # Employee CRUD endpoints
│   ├── departments.py   # Department CRUD endpoints
│   ├── job_roles.py     # Job Role CRUD endpoints
│   └── attrition_logs.py # Attrition Log CRUD endpoints
└── README.md
```

## Notes

- All endpoints include proper error handling and validation
- SQLite uses integer IDs for primary keys
- MongoDB uses ObjectId for document IDs
- Both databases maintain the same logical data structure
- API supports CORS for frontend integration
