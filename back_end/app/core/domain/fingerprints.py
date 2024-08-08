from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
class Fingerprint(Base):
    __tablename__ = "fingerprint"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), unique=False, nullable=False)
    finger_print = Column(String, unique=True, nullable=False)  # Storing file path as String

    # Define relationships correctly
    employee = relationship("Employee", back_populates="fingerprints")

    # Add unique constraint for both fields
    __table_args__ = (UniqueConstraint('employee_id', 'finger_print', name='_employee_finger_print_uc'),)