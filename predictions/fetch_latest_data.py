#!/usr/bin/env python3
"""
Activity A: Fetch latest employee data from API
"""
import requests
import json
import sys

API_BASE_URL = "http://localhost:8000/api/v1"

def fetch_latest_employee(database="sqlite"):
    """Fetch the latest employee entry from the API"""
    try:
        url = f"{API_BASE_URL}/employees/{database}"
        response = requests.get(url, params={"limit": 1, "skip": 0})
        response.raise_for_status()
        
        employees = response.json()
        if not employees:
            print("No employees found")
            return None
            
        latest_employee = employees[0]
        print(f"Fetched employee ID: {latest_employee.get('employee_id', 'N/A')}")
        return latest_employee
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the FastAPI server is running.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def prepare_data_for_prediction(employee_data):
    """Prepare employee data for ML prediction"""
    if not employee_data:
        return None
        
    # Extract features needed for prediction
    features = {
        'Age': employee_data.get('age', 0),
        'Education': employee_data.get('education', 0),
        'JobLevel': employee_data.get('job_level', 0),
        'JobSatisfaction': employee_data.get('job_satisfaction', 0),
        'MonthlyIncome': employee_data.get('monthly_income', 0),
        'TotalWorkingYears': employee_data.get('total_working_years', 0),
        'YearsAtCompany': employee_data.get('years_at_company', 0)
    }
    
    return features

def main():
    database = sys.argv[1] if len(sys.argv) > 1 else "sqlite"
    
    print(f"Fetching latest employee data from {database} database...")
    employee = fetch_latest_employee(database)
    
    if employee:
        features = prepare_data_for_prediction(employee)
        
        # Save data for prediction script
        with open('latest_employee_data.json', 'w') as f:
            json.dump({
                'employee_id': employee.get('employee_id'),
                'features': features,
                'raw_data': employee
            }, f, indent=2)
        
        print("Employee data saved to 'latest_employee_data.json'")
        print(f"Features for prediction: {features}")
        return features
    
    return None

if __name__ == "__main__":
    main()