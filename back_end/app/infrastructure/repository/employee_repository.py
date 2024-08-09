from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.employee import Employee as EmployeeModel
from app.infrastructure.schemas.employee import EmployeeCreate
from sqlalchemy.exc import SQLAlchemyError

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_employee(self, employee_create: EmployeeCreate) -> EmployeeModel:
        # Tạo đối tượng EmployeeModel từ dữ liệu trong EmployeeCreate
        employee = EmployeeModel(
            name=employee_create.name,
            date_of_birth=employee_create.date_of_birth
        )
        try:
            self.db.add(employee)
            self.db.commit()
            self.db.refresh(employee)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return employee

    def get_employee(self, employee_id: int) -> Optional[EmployeeModel]:
        return self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()

    def get_employees(self, skip: int = 0, limit: int = 100) -> List[EmployeeModel]:
        return self.db.query(EmployeeModel).offset(skip).limit(limit).all()
    
    def update_employee(self, employee: EmployeeModel) -> EmployeeModel:
        try:
            self.db.commit()
            self.db.refresh(employee)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return employee

    def delete_employee(self, employee: EmployeeModel) -> None:
        try:
            self.db.delete(employee)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
