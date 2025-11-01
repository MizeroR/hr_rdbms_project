erDiagram
    DEPARTMENTS {
        INTEGER department_id PK
        TEXT department_name
    }

    JOBROLES {
        INTEGER job_role_id PK
        TEXT job_role_name
    }

    EMPLOYEES {
        INTEGER employee_id PK
        INTEGER age
        TEXT attrition
        TEXT gender
        INTEGER education
        TEXT education_field
        TEXT marital_status
        TEXT business_travel
        INTEGER distance_from_home
        INTEGER job_level
        INTEGER job_involvement
        INTEGER job_satisfaction
        INTEGER performance_rating
        INTEGER environment_satisfaction
        INTEGER work_life_balance
        INTEGER total_working_years
        INTEGER years_at_company
        INTEGER years_in_current_role
        INTEGER years_since_last_promotion
        INTEGER years_with_curr_manager
        INTEGER hourly_rate
        INTEGER monthly_income
        INTEGER monthly_rate
        INTEGER daily_rate
        INTEGER num_companies_worked
        INTEGER stock_option_level
        TEXT over_time
        TEXT over18
        INTEGER percent_salary_hike
        INTEGER department_id FK
        INTEGER job_role_id FK
    }

    ATTRITIONLOG {
        INTEGER log_id PK
        INTEGER employee_id FK
        TEXT attrition_status
        TEXT log_date
    }

    DEPARTMENTS ||--o{ EMPLOYEES : "has"
    JOBROLES ||--o{ EMPLOYEES : "includes"
    EMPLOYEES ||--o{ ATTRITIONLOG : "logs"
