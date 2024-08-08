from typing import List, Optional
from app.core.domain.salaries import Salary as SalaryModel
from app.core.use_cases.salaries_use_case import SalaryUseCase
from app.infrastructure.schemas.salaries import Salary as SalarySchema, SalaryCreate

class SalaryService:
    def __init__(self, salary_use_case: SalaryUseCase):
        self.salary_use_case = salary_use_case

    def create_salary(self, salary_create: SalaryCreate) -> SalarySchema:
        # Tạo một salary mới và trả về schema Salary
        return self.salary_use_case.create_salary(salary_create)

    def get_salary(self, salary_id: int) -> Optional[SalarySchema]:
        # Lấy thông tin salary và trả về schema Salary hoặc None
        return self.salary_use_case.get_salary(salary_id)

    def get_salaries(self, skip: int = 0, limit: int = 100) -> List[SalarySchema]:
        # Lấy danh sách salaries và trả về danh sách schema Salary
        return self.salary_use_case.get_salaries(skip, limit)
