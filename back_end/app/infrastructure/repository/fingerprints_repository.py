from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.fingerprints import Fingerprint

class FingerprintRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_fingerprint_by_id(self, fingerprint_id: int) -> Optional[Fingerprint]:
        return self.db_session.query(Fingerprint).filter(Fingerprint.id == fingerprint_id).first()

    def create_fingerprint(self, employee_id: int, finger_print: str) -> Fingerprint:
        new_fingerprint = Fingerprint(employee_id=employee_id, finger_print=finger_print)
        self.db_session.add(new_fingerprint)
        self.db_session.commit()
        self.db_session.refresh(new_fingerprint)  # Refresh to get the updated state
        return new_fingerprint
