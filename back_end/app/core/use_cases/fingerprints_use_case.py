from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.fingerprints import Fingerprint
from app.infrastructure.schemas.fingerprints import FingerprintCreate
from app.infrastructure.repository.fingerprints_repository import FingerprintRepository

class FingerprintUseCase:
    def __init__(self, db: Session):
        self.repository = FingerprintRepository(db)

    def create_fingerprint(self, fingerprint_create: FingerprintCreate) -> Fingerprint:
        return self.repository.create_fingerprint(fingerprint_create)

    def get_fingerprint(self, fingerprint_id: int) -> Optional[Fingerprint]:
        return self.repository.get_fingerprint(fingerprint_id)

    def get_fingerprints(self, skip: int = 0, limit: int = 100) -> List[Fingerprint]:
        return self.repository.get_fingerprints(skip, limit)
