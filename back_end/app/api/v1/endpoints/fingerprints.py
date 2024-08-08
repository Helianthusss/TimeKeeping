from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.infrastructure.schemas.fingerprints import Fingerprint as FingerprintSchema
from app.infrastructure.schemas.fingerprints import FingerprintCreate
from app.core.domain.fingerprints import Fingerprint as FingerprintModel
from app.infrastructure.repository.fingerprints_repository import FingerprintRepository
from app.core.database import get_db
from sqlalchemy.exc import SQLAlchemyError
import base64

router = APIRouter()

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
        
        # Tạo một bản ghi dấu vân tay mới và lưu vào cơ sở dữ liệu
        fingerprint_create = FingerprintCreate(employee_id=employee_id, finger_print=fingerprint_base64)
        repo = FingerprintRepository(db)
        
        # Kiểm tra xem dấu vân tay đã tồn tại chưa
        existing_fingerprints = repo.get_fingerprints()
        for fp in existing_fingerprints:
            if fp.finger_print == fingerprint_base64:
                raise HTTPException(status_code=400, detail="Fingerprint already exists")
        
        # Tạo dấu vân tay mới
        fingerprint_record = repo.create_fingerprint(fingerprint_create)
        
        return fingerprint_record

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
