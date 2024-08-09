from pydantic import BaseModel

class FingerprintMachineBase(BaseModel):
    name: str
    location: str

class FingerprintMachineCreate(FingerprintMachineBase):
    pass

class FingerprintMachine(FingerprintMachineBase):
    id: int

    class Config:
        orm_mode = True