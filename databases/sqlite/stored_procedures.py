import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "erd", "hr_attrition.db")

def get_department_attrition_stats(department_name=None):
    """
    Stored procedure equivalent: Get attrition statistics by department
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    if department_name:
        query = """
        SELECT d.department_name,
               COUNT(e.employee_id) as total_employees,
               SUM(CASE WHEN TRIM(e.attrition) = 'Yes' THEN 1 ELSE 0 END) as attrition_count,
               ROUND(SUM(CASE WHEN TRIM(e.attrition) = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(e.employee_id), 2) as attrition_rate
        FROM Departments d
        JOIN Employees e ON d.department_id = e.department_id
        WHERE d.department_name = ?
        GROUP BY d.department_id, d.department_name
        """
        cur.execute(query, (department_name,))
    else:
        query = """
        SELECT d.department_name,
               COUNT(e.employee_id) as total_employees,
               SUM(CASE WHEN TRIM(e.attrition) = 'Yes' THEN 1 ELSE 0 END) as attrition_count,
               ROUND(SUM(CASE WHEN TRIM(e.attrition) = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(e.employee_id), 2) as attrition_rate
        FROM Departments d
        JOIN Employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY attrition_rate DESC
        """
        cur.execute(query)
    
    results = cur.fetchall()
    conn.close()
    return results

def update_employee_attrition(employee_id, new_status):
    """
    Stored procedure equivalent: Update employee attrition status
    This will trigger the log_attrition_change trigger
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE Employees 
        SET attrition = ? 
        WHERE employee_id = ?
    """, (new_status, employee_id))
    
    conn.commit()
    affected_rows = cur.rowcount
    conn.close()
    return affected_rows

if __name__ == "__main__":
    # Test the stored procedures
    print("Department Attrition Statistics:")
    stats = get_department_attrition_stats()
    for stat in stats:
        print(f"{stat[0]}: {stat[1]} employees, {stat[2]} attritions ({stat[3]}%)")