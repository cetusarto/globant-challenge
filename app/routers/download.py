import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import get_db

router = APIRouter(prefix="/download", tags=["PDF Download"])
MAPS = ["job_department", "department"]

@router.get("/{view_name}/", response_class=Response)
def get_employees_csv(view_name: str, db: Session = Depends(get_db)):
    # Validate the view name
    if view_name not in MAPS:
        raise HTTPException(status_code=400, detail="Invalid view name. Choose from job_department or department.")

    query = text(f'SELECT * FROM "public"."{view_name}_view"')
    try:
        result_proxy = db.execute(query)

        column_names = result_proxy.keys()

        rows = result_proxy.fetchall()

        employees = [dict(zip(column_names, row)) for row in rows]

        # Return the structured data
        return employees

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))