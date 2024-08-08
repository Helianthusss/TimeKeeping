from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
class FingerprintMachine(Base):
    __tablename__ = "fingerprint_machine"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    location = Column(String, index=True)

    # Define relationships correctly
    timekeepings_in = relationship("Timekeeping", foreign_keys="Timekeeping.in_FM_id", back_populates="in_fingerprint_machine")
    timekeepings_out = relationship("Timekeeping", foreign_keys="Timekeeping.out_FM_id", back_populates="out_fingerprint_machine")