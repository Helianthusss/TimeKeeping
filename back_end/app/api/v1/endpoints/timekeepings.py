from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.schemas.timekeepings import Timekeeping as TimekeepingSchema
from app.core.domain.timekeepings import Timekeeping as TimekeepingModel
from app.core.domain.fingerprints import Fingerprint as FingerprintModel
from app.infrastructure.repository.timekeepings_repository import TimekeepingRepository
from app.core.database import get_db
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.api.load_model import load_model
from app.api.utils import compute_similarity, preprocess_image, base64_to_image
import torch

router = APIRouter()

# Load model once to avoid reloading on each request
checkpoint_path = 'D:\\datn_tin\\src\\final_model.pth'
device = torch.device('cpu')
model = load_model(checkpoint_path, device)

@router.get("/{employee_id}/{time_in}", response_model=TimekeepingSchema)
def get_timekeeping(employee_id: int, time_in: datetime, db: Session = Depends(get_db)):
    try:
        timekeeping = TimekeepingRepository.get_timekeeping(db, employee_id, time_in)
        if timekeeping is None:
            raise HTTPException(status_code=404, detail="Timekeeping not found")
        return timekeeping
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

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
        preprocessed_image = torch.tensor(preprocessed_image).unsqueeze(0).to(device)  # Thêm dimension batch

        model.eval()
        input_features = model.extract_features(preprocessed_image)

        best_match = None
        best_similarity = -1

        # Lấy tất cả các dấu vân tay từ cơ sở dữ liệu
        all_fingerprints = db.query(FingerprintModel).all()
        print(f"Number of fingerprints in DB: {len(all_fingerprints)}")  # Kiểm tra số lượng bản ghi

        for record in all_fingerprints:
            print("Processing record...")  # Đảm bảo vòng lặp đang chạy
            db_image = base64_to_image(record.finger_print)
            db_image = torch.tensor(db_image).unsqueeze(0).to(device)  # Thêm dimension batch

            db_features = model.extract_features(db_image)
            similarity = compute_similarity(input_features, db_features)
            print(f"Similarity: {similarity}")

            # Kiểm tra kiểu dữ liệu và giá trị
            if isinstance(similarity, torch.Tensor):
                similarity_value = similarity.item()
            else:
                raise ValueError("Similarity is not a tensor.")
            
            if similarity_value > best_similarity:
                best_similarity = similarity_value
                best_match = record

        # In ra terminal giá trị độ tương đồng cao nhất
        print(f"Best Similarity: {best_similarity}")

        # Kiểm tra nếu không tìm thấy dấu vân tay phù hợp
        if best_match is None:
            raise HTTPException(status_code=401, detail="No matching fingerprint found")
        
        # In ra terminal employee_id và độ tương đồng
        print(f"Similarity: {best_similarity}")

        # Kiểm tra nếu nhân viên đã check-in hoặc đã check-in hôm nay
        matching_employee_id = best_match.employee_id
        now = datetime.now()

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
        raise HTTPException(status_code=500, detail="Database error occurred")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))





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
        preprocessed_input_image = torch.tensor(preprocessed_input_image).unsqueeze(0).to(device)  # Thêm dimension batch

        model.eval()
        input_features = model.extract_features(preprocessed_input_image)

        best_match = None
        best_similarity = -1

        # Lấy tất cả các dấu vân tay từ cơ sở dữ liệu
        all_fingerprints = db.query(FingerprintModel).all()
        print(f"Number of fingerprints in DB: {len(all_fingerprints)}")
        
        for record in all_fingerprints:
            print("Processing record...")
            db_image = base64_to_image(record.finger_print)  # Sử dụng FingerprintModel
            db_image = torch.tensor(db_image).unsqueeze(0).to(device)  # Thêm dimension batch

            db_features = model.extract_features(db_image)
            similarity = compute_similarity(input_features, db_features)
            print(f"Similarity: {similarity}")

            if isinstance(similarity, torch.Tensor):
                similarity_value = similarity.item()
            else:
                raise ValueError("Similarity is not a tensor.")
            
            if similarity_value > best_similarity:
                best_similarity = similarity_value
                best_match = record

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
        open_check_in.in_FM_id = machine_id
        open_check_in.note = "Checked out"
        
        db.commit()
        db.refresh(open_check_in)
        return open_check_in

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


