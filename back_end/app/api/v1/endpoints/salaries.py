from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.schemas.salaries import Salary as SalarySchema, SalaryCreate
from app.infrastructure.repository.salaries_repository import SalaryRepository
from app.core.database import get_db
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/", response_model=SalarySchema)
async def create_salary_endpoint(
    salary_create: SalaryCreate, 
    db: Session = Depends(get_db)
):
    try:
        repository = SalaryRepository(db)
        salary = repository.create_salary(salary_create)
        return salary
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/", response_model=List[SalarySchema])
async def read_salaries_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        repository = SalaryRepository(db)
        salaries = repository.get_salaries(skip, limit)
        return salaries
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/{salary_id}", response_model=SalarySchema)
async def read_salary_endpoint(
    salary_id: int, 
    db: Session = Depends(get_db)
):
    try:
        repository = SalaryRepository(db)
        salary = repository.get_salary(salary_id)
        if salary is None:
            raise HTTPException(status_code=404, detail="Salary not found")
        return salary
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
