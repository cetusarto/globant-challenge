from sqlalchemy.orm import Session
from models import Employee, Department, Job

# Mapping tables to models
MODEL_MAPPING = {
    "employees": Employee,
    "departments": Department,
    "jobs": Job
}

def batch_insert_data(db: Session, table_name: str, data: list):
    if table_name not in MODEL_MAPPING:
        raise ValueError("Invalid table name")

    model = MODEL_MAPPING[table_name]

    # Convert records to model instances
    objects = [model(**row) for row in data]

    # Use bulk insert for efficiency
    db.bulk_save_objects(objects)
    db.commit()

    return len(objects)
