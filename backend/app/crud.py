
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Cancha, Reserva
from app.schemas import CanchaCreate, ReservaCreate
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.database import engine

def reset_autoincrement(db: Session):
    db.execute(text('ALTER SEQUENCE canchas_id_seq RESTART WITH 1'))
    db.commit()

def delete_all_canchas(db: Session):
    db.query(Cancha).delete()  
    db.commit()
    reset_autoincrement(db) 


def create_cancha(db: Session, cancha: CanchaCreate):
    db_cancha = Cancha(nombre=cancha.nombre)  
    db.add(db_cancha)
    db.commit()
    db.refresh(db_cancha)
    return db_cancha


def create_reserva(db: Session, reserva: ReservaCreate):
    nueva_reserva = Reserva(**reserva.dict())
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva


def validar_reserva(db: Session, reserva: ReservaCreate):
    inicio = datetime.combine(reserva.dia, reserva.hora)
    fin = inicio + timedelta(minutes=reserva.duracion)
    reservas_existentes = db.query(Reserva).filter(
        Reserva.cancha_id == reserva.cancha_id,
        Reserva.dia == reserva.dia
    ).all()
    for reserva_existente in reservas_existentes:
        inicio_existente = datetime.combine(reserva_existente.dia, reserva_existente.hora)
        fin_existente = inicio_existente + timedelta(minutes=reserva_existente.duracion)
        if inicio < fin_existente and fin > inicio_existente:
            raise HTTPException(
                status_code=400,
                detail="La reserva se solapa con otra reserva existente."
            )
    return True


def delete_cancha(db: Session, cancha_id: int):
    cancha = db.query(Cancha).filter(Cancha.id == cancha_id).first()
    if not cancha:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
     
    db.delete(cancha)
    db.commit()
    
    return {"message": "Cancha eliminada correctamente"}