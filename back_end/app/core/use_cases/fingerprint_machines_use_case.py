from typing import List, Optional
from app.core.domain.fingerprint_machines import FingerprintMachine
from app.infrastructure.schemas.fingerprint_machines import FingerprintMachineCreate
from app.infrastructure.repository.fingerprint_machines_repository import FingerprintMachineRepository

class FingerprintMachineUseCase:
    def __init__(self, machine_repository: FingerprintMachineRepository):
        self.machine_repository = machine_repository

    def create_fingerprint_machine(self, machine_create: FingerprintMachineCreate) -> FingerprintMachine:
        return self.machine_repository.create_fingerprint_machine(machine_create)

    def get_fingerprint_machine(self, machine_id: int) -> Optional[FingerprintMachine]:
        return self.machine_repository.get_fingerprint_machine(machine_id)

    def get_fingerprint_machines(self, skip: int = 0, limit: int = 100) -> List[FingerprintMachine]:
        return self.machine_repository.get_fingerprint_machines(skip, limit)
