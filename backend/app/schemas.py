from pydantic import BaseModel
from datetime import date, time

class CanchaBase(BaseModel):
    nombre: str

class CanchaCreate(CanchaBase):
    pass

class CanchaResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True  

class ReservaCreate(BaseModel):
    dia: date
    hora: time
    nombre_contacto: str
    telefono: str
    cancha_id: int
    duracion: int = 60  

    class Config:
        orm_mode = True

class ReservaUpdate(BaseModel):
    cancha_id: int
    dia: date
    hora: time
    duracion: int
    