# scripts/load_to_sqlite.py

import sqlite3
import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "hr_attrition.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")
DATA_PATH = os.path.join(BASE_DIR, "data", "WA_Fn-UseC_-HR-Employee-Attrition.csv")

# Step 1 — Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Step 2 — Create tables from schema.sql
with open(SCHEMA_PATH, "r") as f:
    cur.executescript(f.read())
print("✅ Schema created successfully.")

# Step 3 — Load dataset
df = pd.read_csv(DATA_PATH)

# Step 4 — Normalize lookup tables
departments = df["Department"].drop_duplicates().reset_index(drop=True)
job_roles = df["JobRole"].drop_duplicates().reset_index(drop=True)

for dep in departments:
    cur.execute("INSERT INTO Departments (department_name) VALUES (?)", (dep,))

for role in job_roles:
    cur.execute("INSERT INTO JobRoles (job_role_name) VALUES (?)", (role,))

# Step 5 — Insert employees
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO Employees (
            employee_id, age, gender, education, education_field, marital_status,
            business_travel, distance_from_home, job_level, job_involvement,
            job_satisfaction, performance_rating, environment_satisfaction,
            work_life_balance, total_working_years, years_at_company,
            years_in_current_role, years_since_last_promotion, years_with_curr_manager,
            hourly_rate, monthly_income, monthly_rate, daily_rate, num_companies_worked,
            stock_option_level, over_time, over18, percent_salary_hike,
            department_id, job_role_id
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            (SELECT department_id FROM Departments WHERE department_name = ?),
            (SELECT job_role_id FROM JobRoles WHERE job_role_name = ?)
        )
    """, (
        int(row.EmployeeNumber),
        int(row.Age),
        row.Gender,
        int(row.Education),
        row.EducationField,
        row.MaritalStatus,
        row.BusinessTravel,
        int(row.DistanceFromHome),
        int(row.JobLevel),
        int(row.JobInvolvement),
        int(row.JobSatisfaction),
        int(row.PerformanceRating),
        int(row.EnvironmentSatisfaction),
        int(row.WorkLifeBalance),
        int(row.TotalWorkingYears),
        int(row.YearsAtCompany),
        int(row.YearsInCurrentRole),
        int(row.YearsSinceLastPromotion),
        int(row.YearsWithCurrManager),
        int(row.HourlyRate),
        int(row.MonthlyIncome),
        int(row.MonthlyRate),
        int(row.DailyRate),
        int(row.NumCompaniesWorked),
        int(row.StockOptionLevel),
        row.OverTime,
        row.Over18,
        int(row.PercentSalaryHike),
        row.Department,
        row.JobRole
    ))

    # Insert into AttritionLog
    cur.execute("""
        INSERT INTO AttritionLog (employee_id, attrition_status)
        VALUES (?, ?)
    """, (int(row.EmployeeNumber), row.Attrition))

conn.commit()
print("✅ Data loaded successfully.")

conn.close()
