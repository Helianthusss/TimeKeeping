from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    date_of_birth = Column(DateTime, index=True)

    # Define relationships correctly
    timekeepings = relationship("Timekeeping", back_populates="employee")
    salaries = relationship("Salary", back_populates="employee")
    fingerprints = relationship("Fingerprint", back_populates="employee")