from typing import List, Optional
from app.core.domain.fingerprint_machines import FingerprintMachine as FingerprintMachineModel
from app.infrastructure.schemas.fingerprint_machines import FingerprintMachine as FingerprintMachineSchema, FingerprintMachineCreate
from app.infrastructure.repository.fingerprint_machines_repository import FingerprintMachineRepository

class FingerprintMachineUseCase:
    def __init__(self, machine_repository: FingerprintMachineRepository):
        self.machine_repository = machine_repository

    def create_fingerprint_machine(self, machine_create: FingerprintMachineCreate) -> FingerprintMachineSchema:
        # Tạo máy quét dấu vân tay mới và trả về schema
        created_machine = self.machine_repository.create_fingerprint_machine(machine_create)
        return FingerprintMachineSchema.from_orm(created_machine)

    def get_fingerprint_machine(self, machine_id: int) -> Optional[FingerprintMachineSchema]:
        # Lấy thông tin máy quét dấu vân tay và trả về schema
        machine_model = self.machine_repository.get_fingerprint_machine(machine_id)
        if machine_model:
            return FingerprintMachineSchema.from_orm(machine_model)
        return None

    def get_fingerprint_machines(self, skip: int = 0, limit: int = 100) -> List[FingerprintMachineSchema]:
        # Lấy danh sách máy quét dấu vân tay và trả về danh sách schema
        machines = self.machine_repository.get_fingerprint_machines(skip, limit)
        return [FingerprintMachineSchema.from_orm(machine) for machine in machines]
