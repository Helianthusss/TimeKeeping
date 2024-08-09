from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.schemas.fingerprint_machines import FingerprintMachine as FingerprintMachineSchema
from app.infrastructure.schemas.fingerprint_machines import FingerprintMachineCreate 
from app.core.domain.fingerprint_machines import FingerprintMachine as FingerprintMachineModel
from app.infrastructure.repository.fingerprint_machines_repository import FingerprintMachineRepository
from app.core.database import get_db
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/", response_model=FingerprintMachineSchema)
async def create_fingerprint_machine_endpoint(
    machine_name: str,
    location: str,
    db: Session = Depends(get_db)
):
    try:
        repo = FingerprintMachineRepository(db)
        # Kiểm tra máy quét dấu vân tay đã tồn tại
        existing_machine = repo.get_fingerprint_machines()
        for machine in existing_machine:
            if machine.name == machine_name:
                raise HTTPException(status_code=400, detail="Machine already exists")
        
        # Tạo máy quét dấu vân tay mới
        fingerprint_machine_create = FingerprintMachineCreate(name=machine_name, location=location)
        fingerprint_machine = repo.create_fingerprint_machine(fingerprint_machine_create)
        return fingerprint_machine
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/", response_model=List[FingerprintMachineSchema])
async def read_fingerprint_machines_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        repo = FingerprintMachineRepository(db)
        machines = repo.get_fingerprint_machines(skip, limit)
        return machines
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/{machine_id}", response_model=FingerprintMachineSchema)
async def read_fingerprint_machine_endpoint(
    machine_id: int,
    db: Session = Depends(get_db)
):
    try:
        repo = FingerprintMachineRepository(db)
        machine = repo.get_fingerprint_machine(machine_id)
        if machine is None:
            raise HTTPException(status_code=404, detail="Machine not found")
        return machine
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
