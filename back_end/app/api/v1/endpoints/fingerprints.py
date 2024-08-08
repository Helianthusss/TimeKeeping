from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.infrastructure.schemas.fingerprints import Fingerprint as FingerprintSchema
from app.core.domain.fingerprints import Fingerprint as FingerprintModel
from app.infrastructure.repository.fingerprints_repository import FingerprintRepository
from app.core.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import base64

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FingerprintSchema)
async def register_fingerprint(
    employee_id: int = Form(...),
    fingerprint: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Đọc dữ liệu từ file và mã hóa nó thành base64
        fingerprint_data = await fingerprint.read()
        fingerprint_base64 = base64.b64encode(fingerprint_data).decode('utf-8')
        
        # Kiểm tra xem dấu vân tay đã tồn tại chưa
        existing_fingerprint = FingerprintRepository.get_fingerprint_by_data(db, fingerprint_base64)
        if existing_fingerprint:
            raise HTTPException(status_code=400, detail="Fingerprint already exists")
        
        # Tạo một bản ghi dấu vân tay mới và lưu vào cơ sở dữ liệu
        fingerprint_record = FingerprintModel(employee_id=employee_id, finger_print=fingerprint_base64)
        FingerprintRepository.create_fingerprint(db, fingerprint_record)
        
        return fingerprint_record

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
