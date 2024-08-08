from typing import List, Optional
from app.core.use_cases.employee_use_case import EmployeeUseCase
from app.infrastructure.schemas.employee import Employee as EmployeeSchema, EmployeeCreate

class EmployeeService:
    def __init__(self, employee_use_case: EmployeeUseCase):
        self.employee_use_case = employee_use_case

    def create_employee(self, employee_create: EmployeeCreate) -> EmployeeSchema:
        # Gọi phương thức từ EmployeeUseCase và trả về schema
        return self.employee_use_case.create_employee(employee_create)

    def get_employee(self, employee_id: int) -> Optional[EmployeeSchema]:
        # Gọi phương thức từ EmployeeUseCase và trả về schema
        return self.employee_use_case.get_employee(employee_id)

    def get_employees(self, skip: int = 0, limit: int = 100) -> List[EmployeeSchema]:
        # Gọi phương thức từ EmployeeUseCase và trả về danh sách schema
        return self.employee_use_case.get_employees(skip=skip, limit=limit)
