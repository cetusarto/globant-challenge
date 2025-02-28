from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    datetime = Column(DateTime, nullable=True)
    department_id = Column(Integer, nullable=True)
    job_id = Column(Integer, nullable=True)

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=True)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=True)
