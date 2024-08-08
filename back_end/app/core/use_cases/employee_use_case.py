from typing import List, Optional
from app.core.domain.employee import Employee
from app.infrastructure.repository.employee_repository import EmployeeRepository
from app.infrastructure.schemas.employee import EmployeeCreate

class EmployeeUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def create_employee(self, employee_create: EmployeeCreate) -> Employee:
        return self.employee_repository.create(
            name=employee_create.name,
            date_of_birth=employee_create.date_of_birth
        )

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        return self.employee_repository.get(employee_id)

    def get_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        return self.employee_repository.list(skip=skip, limit=limit)
