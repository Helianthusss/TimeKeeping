from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.infrastructure.schemas.timekeepings import Timekeeping as TimekeepingSchema
from app.core.domain.timekeepings import Timekeeping as TimekeepingModel
from app.infrastructure.repository.timekeepings_repository import TimekeepingRepository
from app.core.database import SessionLocal
from sqlalchemy import func
from datetime import datetime
from typing import List
import numpy as np
from PIL import Image
import io
import base64
from sqlalchemy.exc import SQLAlchemyError
from app.api.load_model import load_model
from app.api.utils import compute_similarity
import torch

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

checkpoint_path = 'D:\\datn_tin\\src\\final_model.pth'
device = torch.device('cpu')
model = load_model(checkpoint_path, device)

def preprocess_image(image_data):
    try:
        image_file = io.BytesIO(image_data)
        image = Image.open(image_file).convert("L")
        resized_img = image.resize((96, 96))
        np_array = np.array(resized_img, dtype=np.float32)
        np_array = np.expand_dims(np_array, axis=0)  # Add channel dimension
        np_array /= 255.0
        return np_array
    except Exception as e:
        raise ValueError(f"Failed to preprocess image: {e}")

def base64_to_image(base64_data):
    try:
        image_bytes = base64.b64decode(base64_data)
        image_file = io.BytesIO(image_bytes)
        image = Image.open(image_file).convert("L")
        resized_img = image.resize((96, 96))
        np_array = np.array(resized_img, dtype=np.float32)
        np_array = np.expand_dims(np_array, axis=0)  # Add channel dimension
        np_array /= 255.0
        return np_array
    except Exception as e:
        raise ValueError(f"Failed to decode base64 data: {e}")

@router.get("/{employee_id}/{time_in}", response_model=TimekeepingSchema)
def get_timekeeping(employee_id: int, time_in: datetime, db: Session = Depends(get_db)):
    timekeeping = TimekeepingRepository.get_timekeeping(db, employee_id, time_in)
    if timekeeping is None:
        raise HTTPException(status_code=404, detail="Timekeeping not found")
    return timekeeping

@router.post("/check_in/", response_model=TimekeepingSchema)
async def check_in(
    fingerprint: UploadFile = File(...),
    machine_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Đọc và tiền xử lý dữ liệu dấu vân tay
        fingerprint_data = await fingerprint.read()
        preprocessed_image = preprocess_image(fingerprint_data)
        preprocessed_image = torch.tensor(preprocessed_image).to(device)

        model.eval()
        input_features = model.extract_features(preprocessed_image)

        best_match = None
        best_similarity = -1

        for fingerprint_record in db.query(TimekeepingModel.Fingerprint).all():
            db_image = base64_to_image(fingerprint_record.finger_print)
            db_image = torch.tensor(db_image).to(device)

            db_features = model.extract_features(db_image)
            similarity = compute_similarity(input_features, db_features)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = fingerprint_record
        
        if best_similarity < 0.8:
            raise HTTPException(status_code=401, detail="No matching fingerprint found")
        
        matching_employee_id = best_match.employee_id
        now = datetime.now()

        # In ra terminal employee_id và độ tương đồng
        print(f"Employee ID: {matching_employee_id}, Similarity: {best_similarity.item()}")

        existing_check_in = (
            db.query(TimekeepingModel)
            .filter(
                TimekeepingModel.employee_id == matching_employee_id,
                TimekeepingModel.time_out.is_(None)
            )
            .first()
        )

        if existing_check_in is not None:
            raise HTTPException(status_code=409, detail="Employee is already checked in")

        check_in_today = (
            db.query(TimekeepingModel)
            .filter(
                TimekeepingModel.employee_id == matching_employee_id,
                func.date(TimekeepingModel.time_in) == now.date()
            )
            .first()
        )
        if check_in_today is not None:
            raise HTTPException(status_code=409, detail="Already checked in today")

        new_timekeeping = TimekeepingModel(
            employee_id=matching_employee_id,
            time_in=now,
            in_FM_id=machine_id,
            note="Checked in"
        )
        db.add(new_timekeeping)
        db.commit()
        db.refresh(new_timekeeping)
        return new_timekeeping

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/check_out/", response_model=TimekeepingSchema)
async def check_out(
    fingerprint: UploadFile = File(...),
    machine_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Đọc và tiền xử lý dữ liệu dấu vân tay
        fingerprint_data = await fingerprint.read()
        preprocessed_input_image = preprocess_image(fingerprint_data)
        preprocessed_input_image = torch.tensor(preprocessed_input_image).to(device)

        model.eval()
        input_features = model.extract_features(preprocessed_input_image)

        best_match = None
        best_similarity = -1

        for fingerprint_record in db.query(TimekeepingModel.Fingerprint).all():
            preprocessed_fingerprint_db_image = base64_to_image(fingerprint_record.finger_print)
            preprocessed_fingerprint_db_image = torch.tensor(preprocessed_fingerprint_db_image).to(device)

            db_features = model.extract_features(preprocessed_fingerprint_db_image)
            similarity = compute_similarity(input_features, db_features)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = fingerprint_record

        if best_similarity < 0.8:
            raise HTTPException(status_code=401, detail="No matching fingerprint found")

        matching_employee_id = best_match.employee_id
        now = datetime.now()

        # Kiểm tra xem có check-in mở không
        open_check_in = (
            db.query(TimekeepingModel)
            .filter(
                TimekeepingModel.employee_id == matching_employee_id,
                TimekeepingModel.time_out.is_(None)
            )
            .first()
        )

        if open_check_in is None:
            raise HTTPException(status_code=404, detail="No open check-in found for employee")

        # Cập nhật check-out
        open_check_in.time_out = now
        open_check_in.note = "Checked out"
        
        db.commit()
        db.refresh(open_check_in)
        return open_check_in

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
