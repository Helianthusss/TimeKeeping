from typing import List, Optional
from app.core.domain.timekeepings import Timekeeping
from app.infrastructure.schemas.timekeepings import TimekeepingCreate
from app.infrastructure.repository.timekeepings_repository import TimekeepingRepository

class TimekeepingUseCase:
    def __init__(self, timekeeping_repository: TimekeepingRepository):
        self.timekeeping_repository = timekeeping_repository

    def create_timekeeping(self, timekeeping_create: TimekeepingCreate) -> Timekeeping:
        return self.timekeeping_repository.create_timekeeping(timekeeping_create)

    def get_timekeeping(self, timekeeping_id: int) -> Optional[Timekeeping]:
        return self.timekeeping_repository.get_timekeeping(timekeeping_id)

    def update_timekeeping(self, timekeeping_id: int, timekeeping_update: TimekeepingCreate) -> Optional[Timekeeping]:
        return self.timekeeping_repository.update_timekeeping(timekeeping_id, timekeeping_update)
