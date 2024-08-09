from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.salaries import Salary as SalaryModel
from app.infrastructure.schemas.salaries import SalaryCreate
from sqlalchemy.exc import SQLAlchemyError

class SalaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_salary(self, salary_create: SalaryCreate) -> SalaryModel:
        salary = SalaryModel(**salary_create.dict())
        try:
            self.db.add(salary)
            self.db.commit()
            self.db.refresh(salary)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return salary

    def get_salary(self, salary_id: int) -> Optional[SalaryModel]:
        return self.db.query(SalaryModel).filter(SalaryModel.id == salary_id).first()

    def get_salaries(self, skip: int = 0, limit: int = 100) -> List[SalaryModel]:
        return self.db.query(SalaryModel).offset(skip).limit(limit).all()
