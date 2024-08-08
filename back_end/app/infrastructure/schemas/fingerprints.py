from pydantic import BaseModel
from typing import Optional

class FingerprintBase(BaseModel):
    employee_id: int
    finger_print: str

class FingerprintCreate(FingerprintBase):
    pass

class Fingerprint(FingerprintBase):
    id: int

    class Config:
        orm_mode = True