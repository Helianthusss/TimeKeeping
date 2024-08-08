from typing import List, Optional
from app.core.domain.timekeepings import Timekeeping
from app.core.use_cases.timekeepings_use_case import TimekeepingUseCase
from app.infrastructure.schemas.timekeepings import TimekeepingCreate, Timekeeping

class TimekeepingService:
    def __init__(self, timekeeping_use_case: TimekeepingUseCase):
        self.timekeeping_use_case = timekeeping_use_case

    def create_timekeeping(self, timekeeping_create: TimekeepingCreate) -> Timekeeping:
        return self.timekeeping_use_case.create_timekeeping(timekeeping_create)

    def get_timekeeping(self, timekeeping_id: int) -> Optional[Timekeeping]:
        return self.timekeeping_use_case.get_timekeeping(timekeeping_id)

    def update_timekeeping(self, timekeeping_id: int, timekeeping_update: TimekeepingCreate) -> Optional[Timekeeping]:
        return self.timekeeping_use_case.update_timekeeping(timekeeping_id, timekeeping_update)
