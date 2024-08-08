from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.fingerprints import Fingerprint as FingerprintModel
from app.infrastructure.schemas.fingerprints import Fingerprint as FingerprintSchema, FingerprintCreate
from app.infrastructure.repository.fingerprints_repository import FingerprintRepository

class FingerprintUseCase:
    def __init__(self, db: Session):
        self.repository = FingerprintRepository(db)

    def create_fingerprint(self, fingerprint_create: FingerprintCreate) -> FingerprintSchema:
        # Tạo dấu vân tay mới và trả về schema
        created_fingerprint = self.repository.create_fingerprint(fingerprint_create)
        return FingerprintSchema.from_orm(created_fingerprint)

    def get_fingerprint(self, fingerprint_id: int) -> Optional[FingerprintSchema]:
        # Lấy thông tin dấu vân tay và trả về schema
        fingerprint = self.repository.get_fingerprint(fingerprint_id)
        if fingerprint:
            return FingerprintSchema.from_orm(fingerprint)
        return None

    def get_fingerprints(self, skip: int = 0, limit: int = 100) -> List[FingerprintSchema]:
        # Lấy danh sách dấu vân tay và trả về danh sách schema
        fingerprints = self.repository.get_fingerprints(skip, limit)
        return [FingerprintSchema.from_orm(fingerprint) for fingerprint in fingerprints]
