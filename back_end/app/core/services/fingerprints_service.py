from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.use_cases.fingerprints_use_case import FingerprintUseCase
from app.infrastructure.schemas.fingerprints import FingerprintCreate, Fingerprint as FingerprintSchema

class FingerprintService:
    def __init__(self, db_session: Session):
        # Khởi tạo lớp use case với db_session
        self.use_case = FingerprintUseCase(db_session)

    def create_fingerprint(self, fingerprint_create: FingerprintCreate) -> FingerprintSchema:
        # Gọi phương thức từ FingerprintUseCase và trả về FingerprintSchema
        return self.use_case.create_fingerprint(fingerprint_create)

    def get_fingerprint(self, fingerprint_id: int) -> Optional[FingerprintSchema]:
        # Gọi phương thức từ FingerprintUseCase và trả về FingerprintSchema hoặc None
        return self.use_case.get_fingerprint(fingerprint_id)

    def get_fingerprints(self, skip: int = 0, limit: int = 100) -> List[FingerprintSchema]:
        # Gọi phương thức từ FingerprintUseCase để lấy danh sách FingerprintSchema
        return self.use_case.get_fingerprints(skip, limit)
