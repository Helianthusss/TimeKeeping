from typing import List, Optional
from app.core.domain.timekeepings import Timekeeping as TimekeepingModel
from app.infrastructure.schemas.timekeepings import Timekeeping as TimekeepingSchema, TimekeepingCreate
from app.infrastructure.repository.timekeepings_repository import TimekeepingRepository

class TimekeepingUseCase:
    def __init__(self, timekeeping_repository: TimekeepingRepository):
        self.timekeeping_repository = timekeeping_repository

    def create_timekeeping(self, timekeeping_create: TimekeepingCreate) -> TimekeepingSchema:
        # Tạo thời gian công việc mới và trả về schema
        timekeeping_model = self.timekeeping_repository.create_timekeeping(timekeeping_create)
        return TimekeepingSchema.from_orm(timekeeping_model)

    def get_timekeeping(self, timekeeping_id: int) -> Optional[TimekeepingSchema]:
        # Lấy thông tin thời gian công việc và trả về schema
        timekeeping_model = self.timekeeping_repository.get_timekeeping(timekeeping_id)
        if timekeeping_model:
            return TimekeepingSchema.from_orm(timekeeping_model)
        return None

    def update_timekeeping(self, timekeeping_id: int, timekeeping_update: TimekeepingCreate) -> Optional[TimekeepingSchema]:
        # Cập nhật thời gian công việc và trả về schema
        updated_timekeeping_model = self.timekeeping_repository.update_timekeeping(timekeeping_id, timekeeping_update)
        if updated_timekeeping_model:
            return TimekeepingSchema.from_orm(updated_timekeeping_model)
        return None
