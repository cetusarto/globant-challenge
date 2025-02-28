import pdfplumber
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import EmployeeSchema, DepartmentSchema, JobSchema
from services import batch_insert_data
from database import get_db
import re



router = APIRouter(prefix="/upload", tags=["PDF Upload"])

SCHEMA_MAPPING = {
    "employees": EmployeeSchema,
    "departments": DepartmentSchema,
    "jobs": JobSchema
}

EXPECTED_HEADERS = {
    "employees": {
        "first_4_cols" : ["id", "name", "datetime", "department_id"],
        "last_col": ["job_id"]
    },
    "departments": ["id","department"],
    "jobs": ["id","job"]
}

MAX_SIZE = 1024 * 1024 
MAX_ROWS = 1000


def process_employees(pdf):
    pages = pdf.pages
    i = 0
    data = []
    while i < len(pages) - 1:
        # Extract tables from current and next page
        page_4col = pages[i].extract_table()
        page_1col = pages[i + 1].extract_table()

        if page_4col and page_1col:
            # Apply columns and read into pd dataframes
            df_4col = pd.DataFrame(page_4col, columns=EXPECTED_HEADERS["employees"]["first_4_cols"])
            df_1col = pd.DataFrame(page_1col, columns=EXPECTED_HEADERS["employees"]["last_col"])

            # Merge dataframes and apply transformations
            if len(df_4col) == len(df_1col):
                df_4col[EXPECTED_HEADERS["employees"]["last_col"][0]] = df_1col.iloc[:, 0] 

                for index, row in df_4col.iterrows():
                    # Extract datetime column value
                    datetime_value = row["datetime"]
                    # Check if first 4 characters have a digit to start process (Important step due to poor readability on pdf)
                    if datetime_value:
                        if len(datetime_value) >= 4:
                            if not datetime_value[:4].isdigit():
                                extra_char = datetime_value[0]
                                row["datetime"] = datetime_value[1:]
                                # Append extra char to name column based on case
                                if extra_char.isupper():
                                    row["name"] += f" {extra_char}"
                                # Asume the extra char finishes the name
                                else:
                                    row["name"] += extra_char
                        else:
                            print(datetime_value)
                    else:
                        datetime_value = ""

                    # Add space before all middle uppercase letters in name
                    row["name"] = re.sub(r"(?<=\w)([A-Z])", r" \1", row["name"])
                    # Set to None when empty
                    row["datetime"] = row["datetime"] if row["datetime"].strip() else None
                    row["job_id"] = int(row["job_id"]) if row["job_id"].strip() else None
                    row["department_id"] = int(row["department_id"]) if row["department_id"].strip() else None

                    data.append(row.to_dict())
            # Move to next pair
            i += 2 
        if len(data) > MAX_ROWS:
            raise HTTPException(status_code=400, detail="File contains more than 1000 rows.")

    return data
    
def process_else(pdf,table_name):
    data = []
    for page in pdf.pages:
        extracted_table = page.extract_table()
        if extracted_table:
            df = pd.DataFrame(extracted_table)
            df = df.iloc[:, :len(EXPECTED_HEADERS[table_name])]
            df.columns = EXPECTED_HEADERS[table_name]
            data.extend(df.to_dict(orient="records"))
        # Ensure row Limit
        if len(data) > MAX_ROWS:
            raise HTTPException(status_code=400, detail="File contains more than 1000 rows.")
    return data



@router.post("/pdf/{table_name}/")
async def upload_pdf(table_name: str, file: UploadFile = File(...),  db: Session = Depends(get_db)):
    try:
        # Validate table name
        if table_name not in SCHEMA_MAPPING:
            raise HTTPException(status_code=400, detail="Invalid table name. Choose from employees, departments, jobs.")

        # Check file size before processing
        file.file.seek(0, 2) 
        file_size = file.file.tell()
        if file_size > MAX_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")
        file.file.seek(0) 


        # Using pdfplumber to extract tables
        data = []
        with pdfplumber.open(file.file) as pdf:
            if table_name == "employees" : data = process_employees(pdf)
            else: data = process_else(pdf,table_name)                   

        # Ensure no empty file
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="File contains no rows.")

        # Validate using Pydantic Schema
        validated = [SCHEMA_MAPPING[table_name](**row).dict() for row in data]
        
        batch_insert_data(db, table_name, validated)

        return {
            "message": f"Extracted {len(validated)} records from PDF for table '{table_name}'"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
