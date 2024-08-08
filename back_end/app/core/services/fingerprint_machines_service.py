from typing import List, Optional
from app.core.use_cases.fingerprint_machines_use_case import FingerprintMachineUseCase
from app.infrastructure.schemas.fingerprint_machines import FingerprintMachine as FingerprintMachineSchema, FingerprintMachineCreate

class FingerprintMachineService:
    def __init__(self, machine_use_case: FingerprintMachineUseCase):
        self.machine_use_case = machine_use_case

    def create_fingerprint_machine(self, machine_create: FingerprintMachineCreate) -> FingerprintMachineSchema:
        # Gọi phương thức từ FingerprintMachineUseCase và trả về schema
        return self.machine_use_case.create_fingerprint_machine(machine_create)

    def get_fingerprint_machine(self, machine_id: int) -> Optional[FingerprintMachineSchema]:
        # Gọi phương thức từ FingerprintMachineUseCase và trả về schema
        return self.machine_use_case.get_fingerprint_machine(machine_id)

    def get_fingerprint_machines(self, skip: int = 0, limit: int = 100) -> List[FingerprintMachineSchema]:
        # Gọi phương thức từ FingerprintMachineUseCase và trả về danh sách schema
        return self.machine_use_case.get_fingerprint_machines(skip, limit)
