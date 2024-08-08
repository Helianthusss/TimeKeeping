from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.schemas.employee import Employee as EmployeeSchemas
from app.core.domain.employee import Employee as EmployeeModels
from app.infrastructure.repository.employee_repository import EmployeeRepository
from app.core.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

router = APIRouter()

def parse_date(date_str: str) -> datetime:
    """
    Phân tích chuỗi ngày theo các định dạng ngày khác nhau.
    """
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
    """
    Tạo một nhân viên mới.
    """
    try:
        dob = parse_date(date_of_birth)
        employee_repo = EmployeeRepository(db)
        
        # Kiểm tra nhân viên đã tồn tại với tên và ngày sinh trùng khớp
        existing_employee = (
            db.query(EmployeeModels)
            .filter(
                EmployeeModels.name == name,
                EmployeeModels.date_of_birth == dob
            )
            .first()
        )
        
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee already exists")
        
        # Tạo và lưu nhân viên mới
        employee = EmployeeModels(name=name, date_of_birth=dob)
        created_employee = employee_repo.create_employee(employee)
        return created_employee
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")


@router.get("/", response_model=List[EmployeeSchemas])
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách nhân viên với phân trang.
    """
    employee_repo = EmployeeRepository(db)
    employees = employee_repo.get_employees(skip, limit)
    return employees

@router.get("/{employee_id}", response_model=EmployeeSchemas)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin một nhân viên theo ID.
    """
    employee_repo = EmployeeRepository(db)
    employee = employee_repo.get_employee(employee_id)
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
    """
    Cập nhật thông tin của một nhân viên.
    """
    try:
        dob = parse_date(date_of_birth)
        employee_repo = EmployeeRepository(db)
        employee = employee_repo.get_employee(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        # Cập nhật thông tin nhân viên
        employee.name = name
        employee.date_of_birth = dob
        updated_employee = employee_repo.update_employee(employee)
        return updated_employee
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Xóa một nhân viên theo ID.
    """
    try:
        employee_repo = EmployeeRepository(db)
        employee = employee_repo.get_employee(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        # Xóa nhân viên
        employee_repo.delete_employee(employee)
        return {"detail": "Employee deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
