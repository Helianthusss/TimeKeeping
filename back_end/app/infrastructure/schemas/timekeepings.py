from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TimekeepingBase(BaseModel):
    employee_id: int
    time_in: datetime
    time_out: datetime | None
    in_FM_id: int
    out_FM_id: int | None
    note: str | None

class TimekeepingCreate(TimekeepingBase):
    pass

class Timekeeping(TimekeepingBase):
    pass

    class Config:
        orm_mode = True

class Employee(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class TimekeepingWithEmployee(BaseModel):
    employee_id: int
    employee_name: str
    time_in: datetime
    time_out: Optional[datetime]
    in_FM_id: int
    out_FM_id: Optional[int]
    note: Optional[str]

    class Config:
        orm_mode = True