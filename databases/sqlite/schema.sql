-- db/schema.sql

-- Drop existing tables (for re-runs)
DROP TABLE IF EXISTS AttritionLog;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Departments;
DROP TABLE IF EXISTS JobRoles;

-- Department table
CREATE TABLE Departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE NOT NULL
);

-- Job Role table
CREATE TABLE JobRoles (
    job_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_role_name TEXT UNIQUE NOT NULL
);

-- Employees main table
CREATE TABLE Employees (
    employee_id INTEGER PRIMARY KEY,
    age INTEGER,
    attrition TEXT,
    gender TEXT,
    education INTEGER,
    education_field TEXT,
    marital_status TEXT,
    business_travel TEXT,
    distance_from_home INTEGER,
    job_level INTEGER,
    job_involvement INTEGER,
    job_satisfaction INTEGER,
    performance_rating INTEGER,
    environment_satisfaction INTEGER,
    work_life_balance INTEGER,
    total_working_years INTEGER,
    years_at_company INTEGER,
    years_in_current_role INTEGER,
    years_since_last_promotion INTEGER,
    years_with_curr_manager INTEGER,
    hourly_rate INTEGER,
    monthly_income INTEGER,
    monthly_rate INTEGER,
    daily_rate INTEGER,
    num_companies_worked INTEGER,
    stock_option_level INTEGER,
    over_time TEXT,
    percent_salary_hike INTEGER,
    relationship_satisfaction INTEGER,
    standard_hours INTEGER,
    training_times_last_year INTEGER,
    department_id INTEGER,
    job_role_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (job_role_id) REFERENCES JobRoles(job_role_id)
);

-- Attrition log table (to record employee exits)
CREATE TABLE AttritionLog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    attrition_status TEXT,
    log_date TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- View: Get employee count by department
CREATE VIEW employee_count_by_dept AS
SELECT d.department_name, COUNT(e.employee_id) as employee_count
FROM Departments d
LEFT JOIN Employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name;

-- Trigger: When employee attrition is updated to 'Yes', insert log entry
CREATE TRIGGER log_attrition_change
AFTER UPDATE OF attrition ON Employees
WHEN NEW.attrition = 'Yes' AND OLD.attrition != 'Yes'
BEGIN
    INSERT INTO AttritionLog (employee_id, attrition_status, log_date)
    VALUES (NEW.employee_id, 'Yes', datetime('now'));
END;
