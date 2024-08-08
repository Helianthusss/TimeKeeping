from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
class Salary(Base):
    __tablename__ = "salary"

    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    date_of_decision = Column(DateTime, primary_key=True)
    salary = Column(Integer, index=True)

    # Define relationships correctly
    employee = relationship("Employee", back_populates="salaries")