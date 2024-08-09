from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.timekeepings import Timekeeping as TimekeepingModel
from app.infrastructure.schemas.timekeepings import TimekeepingCreate
from sqlalchemy.exc import SQLAlchemyError

class TimekeepingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_timekeeping(self, timekeeping_create: TimekeepingCreate) -> TimekeepingModel:
        timekeeping = TimekeepingModel(**timekeeping_create.dict())
        try:
            self.db.add(timekeeping)
            self.db.commit()
            self.db.refresh(timekeeping)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return timekeeping

    def get_timekeeping(self, timekeeping_id: int) -> Optional[TimekeepingModel]:
        return self.db.query(TimekeepingModel).filter(TimekeepingModel.id == timekeeping_id).first()

    def update_timekeeping(self, timekeeping_id: int, timekeeping_update: TimekeepingCreate) -> Optional[TimekeepingModel]:
        timekeeping = self.db.query(TimekeepingModel).filter(TimekeepingModel.id == timekeeping_id).first()
        if timekeeping:
            for key, value in timekeeping_update.dict().items():
                setattr(timekeeping, key, value)
            self.db.commit()
            self.db.refresh(timekeeping)
            return timekeeping
        return None
