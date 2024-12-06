from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cancha(Base):
    __tablename__ = "canchas"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    nombre = Column(String, nullable=False, index=True) 

    reservas = relationship("Reserva", back_populates="cancha")  

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Date, nullable=False, index=True)  
    hora = Column(Time, nullable=False)  
    nombre_contacto = Column(String, nullable=False)  
    telefono = Column(String, nullable=False)  
    cancha_id = Column(Integer, ForeignKey("canchas.id"), nullable=False, index=True)  

    cancha = relationship("Cancha", back_populates="reservas")
    duracion = Column(Integer, default=60) 
