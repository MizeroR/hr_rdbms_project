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
        TEXT gender
        TEXT education_field
        TEXT marital_status
        TEXT business_travel
        INTEGER job_level
        INTEGER performance_rating
        TEXT over_time
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
