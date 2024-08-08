from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.fingerprints import Fingerprint as FingerprintModel
from app.core.use_cases.fingerprints_use_case import FingerprintUseCase
from app.infrastructure.schemas.fingerprints import FingerprintCreate, Fingerprint as FingerprintSchema

class FingerprintService:
    def __init__(self, db_session: Session):
        self.use_case = FingerprintUseCase(db_session)

    def create_fingerprint(self, fingerprint_create: FingerprintCreate) -> FingerprintSchema:
        return self.use_case.create_fingerprint(fingerprint_create)

    def get_fingerprint(self, fingerprint_id: int) -> Optional[FingerprintSchema]:
        return self.use_case.get_fingerprint(fingerprint_id)
