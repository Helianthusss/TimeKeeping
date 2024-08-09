from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
class Timekeeping(Base):
    __tablename__ = "timekeeping"

    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    time_in = Column(DateTime, primary_key=True)
    time_out = Column(DateTime, index=True, nullable=True)  # Allow null if not checked out yet
    in_FM_id = Column(Integer, ForeignKey('fingerprint_machine.id'))
    out_FM_id = Column(Integer, ForeignKey('fingerprint_machine.id'), nullable=True)  # Allow null if not checked out yet
    note = Column(String, index=True)

    # Define relationships correctly
    employee = relationship("Employee", back_populates="timekeepings")
    in_fingerprint_machine = relationship("FingerprintMachine", foreign_keys=[in_FM_id], back_populates="timekeepings_in")
    out_fingerprint_machine = relationship("FingerprintMachine", foreign_keys=[out_FM_id], back_populates="timekeepings_out")