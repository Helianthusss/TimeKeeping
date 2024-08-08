from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.employee import Employee as EmployeeModel
from app.infrastructure.schemas.employee import Employee as EmployeeSchema
from app.infrastructure.schemas.employee import EmployeeCreate

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_employee(self, employee_create: EmployeeCreate) -> EmployeeSchema:
        # Tạo đối tượng Employee từ dữ liệu đầu vào
        employee = EmployeeModel(name=employee_create.name, date_of_birth=employee_create.date_of_birth)
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)  # Làm mới đối tượng để đảm bảo thông tin chính xác
        return EmployeeSchema.from_orm(employee)

    def get_employee(self, employee_id: int) -> Optional[EmployeeSchema]:
        # Lấy thông tin nhân viên theo ID
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if employee:
            return EmployeeSchema.from_orm(employee)
        return None

    def get_employees(self, skip: int = 0, limit: int = 100) -> List[EmployeeSchema]:
        # Lấy danh sách nhân viên với phân trang
        employees = self.db.query(EmployeeModel).offset(skip).limit(limit).all()
        return [EmployeeSchema.from_orm(emp) for emp in employees]
