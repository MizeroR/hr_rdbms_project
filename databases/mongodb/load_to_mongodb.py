from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "WA_Fn-UseC_-HR-Employee-Attrition.csv")

def connect_mongodb():
    connection_string = os.getenv('MONGODB_URI')
    if connection_string:
        try:
            client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            return client
        except:
            pass
    
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        return client
    except Exception as e:
        raise ConnectionError("MongoDB connection failed") from e

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
    
    print("✅ MongoDB data loaded successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'client' in locals():
        client.close()