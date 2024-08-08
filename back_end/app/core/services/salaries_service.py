from typing import List, Optional
from app.core.domain.salaries import Salary
from app.core.use_cases.salaries_use_case import SalaryUseCase
from app.infrastructure.schemas.salaries import SalaryCreate

class SalaryService:
    def __init__(self, salary_use_case: SalaryUseCase):
        self.salary_use_case = salary_use_case

    def create_salary(self, salary_create: SalaryCreate) -> Salary:
        return self.salary_use_case.create_salary(salary_create)

    def get_salary(self, salary_id: int) -> Optional[Salary]:
        return self.salary_use_case.get_salary(salary_id)

    def get_salaries(self, skip: int = 0, limit: int = 100) -> List[Salary]:
        return self.salary_use_case.get_salaries(skip, limit)
