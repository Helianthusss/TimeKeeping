from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.fingerprint_machines import FingerprintMachine as FingerprintMachineModel
from app.infrastructure.schemas.fingerprint_machines import FingerprintMachineCreate, FingerprintMachine
from sqlalchemy.exc import NoResultFound

class FingerprintMachineRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_fingerprint_machine(self, machine_create: FingerprintMachineCreate) -> FingerprintMachine:
        machine = FingerprintMachineModel(**machine_create.dict())
        self.db.add(machine)
        self.db.commit()
        self.db.refresh(machine)
        return FingerprintMachine.from_orm(machine)

    def get_fingerprint_machine(self, machine_id: int) -> Optional[FingerprintMachine]:
        try:
            machine = self.db.query(FingerprintMachineModel).filter(FingerprintMachineModel.id == machine_id).one()
            return FingerprintMachine.from_orm(machine)
        except NoResultFound:
            return None

    def get_fingerprint_machines(self, skip: int = 0, limit: int = 100) -> List[FingerprintMachine]:
        machines = self.db.query(FingerprintMachineModel).offset(skip).limit(limit).all()
        return [FingerprintMachine.from_orm(machine) for machine in machines]
