from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.schemas.employee import Employee as EmployeeSchemas
from app.core.domain.employee import Employee as EmployeeModels
from app.infrastructure.repository.employee_repository import EmployeeRepository
from app.core.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_date(date_str: str) -> datetime:
    for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Invalid date format: {date_str}")

@router.post("/", response_model=EmployeeSchemas)
async def create_employee(
    name: str = Form(...),
    date_of_birth: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        dob = parse_date(date_of_birth)
        existing_employee = EmployeeRepository.get_employee_by_name_and_dob(db, name, dob)
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee already exists")
        employee = EmployeeModels(name=name, date_of_birth=dob)
        EmployeeRepository.create_employee(db, employee)
        return employee
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[EmployeeSchemas])
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    employees = EmployeeRepository.get_employees(db, skip, limit)
    return employees

@router.get("/{employee_id}", response_model=EmployeeSchemas)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = EmployeeRepository.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/{employee_id}", response_model=EmployeeSchemas)
async def update_employee(
    employee_id: int,
    name: str = Form(...),
    date_of_birth: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        dob = parse_date(date_of_birth)
        employee = EmployeeRepository.get_employee(db, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee.name = name
        employee.date_of_birth = dob
        EmployeeRepository.update_employee(db, employee)
        return employee
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    try:
        employee = EmployeeRepository.get_employee(db, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        EmployeeRepository.delete_employee(db, employee)
        return {"detail": "Employee deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
