from typing import List, Optional
from app.infrastructure.schemas.employee import Employee as EmployeeSchema, EmployeeCreate
from app.infrastructure.repository.employee_repository import EmployeeRepository
from app.core.domain.employee import Employee as EmployeeModel

class EmployeeUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def create_employee(self, employee_create: EmployeeCreate) -> EmployeeSchema:
        # Tạo nhân viên mới và trả về EmployeeSchema
        created_employee_model = self.employee_repository.create_employee(employee_create)
        return EmployeeSchema.from_orm(created_employee_model)

    def get_employee(self, employee_id: int) -> Optional[EmployeeSchema]:
        # Lấy thông tin nhân viên và trả về EmployeeSchema
        employee_model = self.employee_repository.get_employee(employee_id)
        if employee_model:
            return EmployeeSchema.from_orm(employee_model)
        return None

    def get_employees(self, skip: int = 0, limit: int = 100) -> List[EmployeeSchema]:
        # Lấy danh sách nhân viên và trả về danh sách EmployeeSchema
        employees = self.employee_repository.get_employees(skip, limit)
        return [EmployeeSchema.from_orm(employee) for employee in employees]
