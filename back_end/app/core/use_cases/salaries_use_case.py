from typing import List, Optional
from app.core.domain.salaries import Salary
from app.infrastructure.schemas.salaries import SalaryCreate
from app.infrastructure.repository.salaries_repository import SalaryRepository

class SalaryUseCase:
    def __init__(self, salary_repository: SalaryRepository):
        self.salary_repository = salary_repository

    def create_salary(self, salary_create: SalaryCreate) -> Salary:
        return self.salary_repository.create_salary(salary_create)

    def get_salary(self, salary_id: int) -> Optional[Salary]:
        return self.salary_repository.get_salary(salary_id)

    def get_salaries(self, skip: int = 0, limit: int = 100) -> List[Salary]:
        return self.salary_repository.get_salaries(skip, limit)
