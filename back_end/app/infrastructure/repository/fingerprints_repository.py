from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.fingerprints import Fingerprint as FingerprintModel
from app.infrastructure.schemas.fingerprints import FingerprintCreate
from sqlalchemy.exc import SQLAlchemyError

class FingerprintRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_fingerprint(self, fingerprint_create: FingerprintCreate) -> FingerprintModel:
        fingerprint = FingerprintModel(**fingerprint_create.dict())
        try:
            self.db.add(fingerprint)
            self.db.commit()
            self.db.refresh(fingerprint)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return fingerprint

    def get_fingerprint(self, fingerprint_id: int) -> Optional[FingerprintModel]:
        return self.db.query(FingerprintModel).filter(FingerprintModel.id == fingerprint_id).first()

    def get_fingerprints(self, skip: int = 0, limit: int = 100) -> List[FingerprintModel]:
        return self.db.query(FingerprintModel).offset(skip).limit(limit).all()
