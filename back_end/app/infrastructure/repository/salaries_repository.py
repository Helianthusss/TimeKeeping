from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.salaries import Salary as SalaryModel
from app.infrastructure.schemas.salaries import SalaryCreate, Salary
from sqlalchemy.exc import NoResultFound

class SalaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_salary(self, salary_create: SalaryCreate) -> Salary:
        salary = SalaryModel(**salary_create.dict())
        self.db.add(salary)
        self.db.commit()
        self.db.refresh(salary)
        return Salary.from_orm(salary)

    def get_salary(self, salary_id: int) -> Optional[Salary]:
        try:
            salary = self.db.query(SalaryModel).filter(SalaryModel.id == salary_id).one()
            return Salary.from_orm(salary)
        except NoResultFound:
            return None

    def get_salaries(self, skip: int = 0, limit: int = 100) -> List[Salary]:
        salaries = self.db.query(SalaryModel).offset(skip).limit(limit).all()
        return [Salary.from_orm(salary) for salary in salaries]
