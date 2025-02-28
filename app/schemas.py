from pydantic import BaseModel
from typing import Optional

class EmployeeSchema(BaseModel):
    id: int
    name: Optional[str] = None
    datetime: Optional[str] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None

class DepartmentSchema(BaseModel):
    id: int
    department: Optional[str] = None

class JobSchema(BaseModel):
    id: int
    job: Optional[str] = None
