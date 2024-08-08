from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SalaryBase(BaseModel):
    employee_id: int
    date_of_decision: datetime
    salary: int

class SalaryCreate(SalaryBase):
    pass

class Salary(SalaryBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True