from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "WA_Fn-UseC_-HR-Employee-Attrition.csv")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["hr_db"]

# Drop existing collections if any
db.departments.drop()
db.job_roles.drop()
db.employees.drop()

# Load dataset
df = pd.read_csv(DATA_PATH)

# Insert departments
departments = df["Department"].drop_duplicates().to_list()
dep_map = {}
for dep in departments:
    res = db.departments.insert_one({"department_name": dep})
    dep_map[dep] = res.inserted_id

# Insert job roles
job_roles = df["JobRole"].drop_duplicates().to_list()
role_map = {}
for role in job_roles:
    res = db.job_roles.insert_one({"job_role_name": role})
    role_map[role] = res.inserted_id

# Insert employees
for _, row in df.iterrows():
    db.employees.insert_one({
        "employee_id": int(row.EmployeeNumber),
        "age": int(row.Age),
        "gender": row.Gender,
        "education": int(row.Education),
        "education_field": row.EducationField,
        "marital_status": row.MaritalStatus,
        "business_travel": row.BusinessTravel,
        "distance_from_home": int(row.DistanceFromHome),
        "job_level": int(row.JobLevel),
        "job_involvement": int(row.JobInvolvement),
        "job_satisfaction": int(row.JobSatisfaction),
        "performance_rating": int(row.PerformanceRating),
        "department": dep_map[row.Department],
        "job_role": role_map[row.JobRole],
        "attrition_status": row.Attrition,
        "log": [
            {
                "status": row.Attrition,
                "date": datetime.now()
            }
        ]
    })

print("✅ MongoDB data loaded successfully.")
client.close()
