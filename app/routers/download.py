import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()
MAPS = ["job_department","department"]

@router.get("/{view_name}}/", response_class=Response)
def get_employees_csv(view_name: str, db: Session = Depends(get_db)):
    
    if view_name not in MAPS : raise HTTPException(status_code=400, detail="Invalid view name. Choose from job_department or departments.")

    query = f"SELECT * FROM \"public\".{view_name}_view"
    try:
        # Execute the query
        result = db.execute(query).fetchall()

        # Get column names from the result
        column_names = result.keys()

        # Convert result to a list of dictionaries
        employees = [dict(zip(column_names, row)) for row in result]

        # Return the structured data
        return employees

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
