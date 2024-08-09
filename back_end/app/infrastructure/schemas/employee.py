from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# Schemas for Employee
class EmployeeBase(BaseModel):
    name: str
    date_of_birth: datetime

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True