from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.domain.timekeepings import Timekeeping as TimekeepingModel
from app.infrastructure.schemas.timekeepings import TimekeepingCreate, Timekeeping
from sqlalchemy.exc import NoResultFound

class TimekeepingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_timekeeping(self, timekeeping_create: TimekeepingCreate) -> Timekeeping:
        timekeeping = TimekeepingModel(**timekeeping_create.dict())
        self.db.add(timekeeping)
        self.db.commit()
        self.db.refresh(timekeeping)
        return Timekeeping.from_orm(timekeeping)

    def get_timekeeping(self, timekeeping_id: int) -> Optional[Timekeeping]:
        try:
            timekeeping = self.db.query(TimekeepingModel).filter(TimekeepingModel.id == timekeeping_id).one()
            return Timekeeping.from_orm(timekeeping)
        except NoResultFound:
            return None

    def update_timekeeping(self, timekeeping_id: int, timekeeping_update: TimekeepingCreate) -> Optional[Timekeeping]:
        timekeeping = self.db.query(TimekeepingModel).filter(TimekeepingModel.id == timekeeping_id).first()
        if timekeeping:
            for key, value in timekeeping_update.dict().items():
                setattr(timekeeping, key, value)
            self.db.commit()
            self.db.refresh(timekeeping)
            return Timekeeping.from_orm(timekeeping)
        return None
