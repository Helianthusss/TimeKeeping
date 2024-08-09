from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.fingerprint_machines import FingerprintMachine as FingerprintMachineModel
from app.infrastructure.schemas.fingerprint_machines import FingerprintMachineCreate
from sqlalchemy.exc import SQLAlchemyError

class FingerprintMachineRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_fingerprint_machine(self, machine_create: FingerprintMachineCreate) -> FingerprintMachineModel:
        machine = FingerprintMachineModel(**machine_create.dict())
        try:
            self.db.add(machine)
            self.db.commit()
            self.db.refresh(machine)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return machine

    def get_fingerprint_machine(self, machine_id: int) -> Optional[FingerprintMachineModel]:
        return self.db.query(FingerprintMachineModel).filter(FingerprintMachineModel.id == machine_id).first()

    def get_fingerprint_machines(self, skip: int = 0, limit: int = 100) -> List[FingerprintMachineModel]:
        return self.db.query(FingerprintMachineModel).offset(skip).limit(limit).all()
