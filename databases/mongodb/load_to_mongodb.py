from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)

DATA_PATH = os.path.join(BASE_DIR, "WA_Fn-UseC_-HR-Employee-Attrition.csv")

def connect_mongodb():
    connection_string = os.getenv('MONGODB_URI')
    print(f"Attempting MongoDB connection...")
    
    if connection_string:
        print(f"Using URI from .env file: {connection_string[:30]}...")
        try:
            client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
            client.admin.command('ping')
            print("Connected to MongoDB Atlas!")
            return client
        except Exception as e:
            print(f"Atlas connection failed: {e}")
    
    print("Trying local MongoDB...")
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("Connected to local MongoDB!")
        return client
    except Exception as e:
        raise ConnectionError(f"MongoDB connection failed. Atlas error (if tried), Local error: {e}") from e

try:
    client = connect_mongodb()
    db = client["hr_rdbms_project"]
    
    for collection in ["Departments", "JobRoles", "Employees", "AttritionLog"]:
        db[collection].drop()
    
    df = pd.read_csv(DATA_PATH)
    
    departments = [{"department_name": dep.strip()} 
                  for dep in df[" Department            "].drop_duplicates()]
    db.Departments.insert_many(departments)
    
    job_roles = [{"job_role_name": role.strip()} 
                for role in df[" JobRole                  "].drop_duplicates()]
    db.JobRoles.insert_many(job_roles)
    
    employees = [{
        "employee_id": int(row[" EmployeeNumber"]),
        "age": int(row["Age"]),
        "gender": row[" Gender"].strip(),
        "education": int(row[" Education"]),
        "education_field": row[" EducationField  "].strip(),
        "marital_status": row[" MaritalStatus"].strip(),
        "business_travel": row[" BusinessTravel   "].strip(),
        "distance_from_home": int(row[" DistanceFromHome"]),
        "job_level": int(row[" JobLevel"]),
        "job_involvement": int(row[" JobInvolvement"]),
        "job_satisfaction": int(row[" JobSatisfaction"]),
        "performance_rating": int(row[" PerformanceRating"]),
        "department": row[" Department            "].strip(),
        "job_role": row[" JobRole                  "].strip(),
        "attrition_status": row[" Attrition"].strip()
    } for _, row in df.iterrows()]
    
    db.Employees.insert_many(employees)
    
    attrition_logs = [{
        "employee_id": int(row[" EmployeeNumber"]),
        "attrition_status": row[" Attrition"].strip(),
        "log_date": datetime.now(timezone.utc)
    } for _, row in df.iterrows()]
    
    db.AttritionLog.insert_many(attrition_logs)
    
    print("MongoDB data loaded successfully!")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'client' in locals():
        client.close()