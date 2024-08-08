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
    pass

    class Config:
        orm_mode = True

class FingerprintMachineBase(BaseModel):
    name: str
    location: str

class FingerprintMachineCreate(FingerprintMachineBase):
    pass

class FingerprintMachine(FingerprintMachineBase):
    id: int

    class Config:
        orm_mode = True