import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import EmployeeSchema, DepartmentSchema, JobSchema
from services import batch_insert_data
from database import get_db


router = APIRouter(prefix="/upload", tags=["Uploads"])

# Table name mapping to schemas
SCHEMA_MAPPING = {
    "employees": EmployeeSchema,
    "departments": DepartmentSchema,
    "jobs": JobSchema
}

MAX_SIZE = 1024 * 1024 
MAX_ROWS = 1000

EXPECTED_HEADERS = {
    "employees": ["id", "name", "datetime", "department_id,job_id"],
    "departments": ["id","department"],
    "jobs": ["id","job"]
}

@router.post("/csv/{table_name}/")
async def upload_csv(table_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Validate table name
        if table_name not in SCHEMA_MAPPING:
            raise HTTPException(status_code=400, detail="Invalid table name. Choose from employees, departments, jobs.")

        # Check file size before reading
        file.file.seek(0, 2)
        file_size = file.file.tell()
        if file_size > MAX_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")
        file.file.seek(0)

        # Read CSV file in chunks to avoid memory overload
        chunks = pd.read_csv(file.file, chunksize=500)
        data = []
        row_count = 0

        # Evaluate chunk by chunk searching for rows
        for chunk in chunks:
            chunk.columns = EXPECTED_HEADERS[table_name]
            row_count += len(chunk)
            if row_count == 0:
                raise HTTPException(status_code=400, detail="File contains no rows.")
            if row_count > MAX_ROWS:
                raise HTTPException(status_code=400, detail="File contains more than 1000 rows.")
            data.extend(chunk.to_dict(orient="records"))

        # Validate using Pydantic Schema
        validated = [SCHEMA_MAPPING[table_name](**row).dict() for row in data]

        batch_insert_data(db, table_name, validated)

        return {
            "message": f"Processed {len(validated)} records for table '{table_name}'"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))