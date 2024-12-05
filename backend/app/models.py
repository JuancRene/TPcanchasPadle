from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cancha(Base):
    __tablename__ = "canchas"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)  # Añadido autoincrement
    nombre = Column(String, nullable=False, index=True)  # Nombre de la cancha, añadido índice

    reservas = relationship("Reserva", back_populates="cancha")  # Relación inversa con las reservas

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Date, nullable=False, index=True)  # Fecha de la reserva, añadido índice
    hora = Column(Time, nullable=False)  # Hora de inicio de la reserva
    nombre_contacto = Column(String, nullable=False)  # Nombre del contacto
    telefono = Column(String, nullable=False)  # Teléfono del contacto
    cancha_id = Column(Integer, ForeignKey("canchas.id"), nullable=False, index=True)  # Relación con Cancha

    cancha = relationship("Cancha", back_populates="reservas")
    duracion = Column(Integer, default=60)  # Duración en minutos, por defecto 60 minutos

