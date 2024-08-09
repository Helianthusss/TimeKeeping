from typing import List, Optional
from app.core.domain.salaries import Salary as SalaryModel
from app.infrastructure.schemas.salaries import Salary as SalarySchema, SalaryCreate
from app.infrastructure.repository.salaries_repository import SalaryRepository

class SalaryUseCase:
    def __init__(self, salary_repository: SalaryRepository):
        self.salary_repository = salary_repository

    def create_salary(self, salary_create: SalaryCreate) -> SalarySchema:
        # Tạo lương mới và trả về schema
        salary_model = self.salary_repository.create_salary(salary_create)
        return SalarySchema.from_orm(salary_model)

    def get_salary(self, salary_id: int) -> Optional[SalarySchema]:
        # Lấy thông tin lương và trả về schema
        salary_model = self.salary_repository.get_salary(salary_id)
        if salary_model:
            return SalarySchema.from_orm(salary_model)
        return None

    def get_salaries(self, skip: int = 0, limit: int = 100) -> List[SalarySchema]:
        # Lấy danh sách lương và trả về danh sách schema
        salaries = self.salary_repository.get_salaries(skip, limit)
        return [SalarySchema.from_orm(salary) for salary in salaries]
