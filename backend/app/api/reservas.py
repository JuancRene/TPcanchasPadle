from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ReservaCreate, ReservaUpdate
from app.models import Cancha, Reserva

router = APIRouter()

@router.post("/")
def create_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    cancha = db.query(Cancha).filter(Cancha.id == reserva.cancha_id).first()
    if not cancha:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    elif reserva.duracion < 30:
        raise HTTPException(status_code=400, detail="La duración mínima de una reserva es de minimo 30 minutos")
    from datetime import datetime, timedelta
    inicio_nueva = datetime.combine(reserva.dia, reserva.hora)
    fin_nueva = inicio_nueva + timedelta(minutes=reserva.duracion)
    reservas_existentes = db.query(Reserva).filter(Reserva.cancha_id == reserva.cancha_id).all()
    for reserva_existente in reservas_existentes:
        inicio_existente = datetime.combine(reserva_existente.dia, reserva_existente.hora)
        fin_existente = inicio_existente + timedelta(minutes=reserva_existente.duracion)
        if inicio_nueva < fin_existente and fin_nueva > inicio_existente:
            raise HTTPException(
                status_code=400,
                detail=f"La cancha ya está reservada de {inicio_existente.time()} a {fin_existente.time()}"
            )

    db_reserva = Reserva(
        dia=reserva.dia,
        hora=reserva.hora,
        nombre_contacto=reserva.nombre_contacto,
        telefono=reserva.telefono,
        cancha_id=reserva.cancha_id,
        duracion=reserva.duracion,
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    db.delete(reserva)
    db.commit()
    return {"mensaje": "Reserva eliminada exitosamente"}

@router.put("/{reserva_id}")
def actualizar_reserva(reserva_id: int, datos_actualizados: ReservaUpdate, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    from datetime import datetime, timedelta
    inicio_nueva = datetime.combine(datos_actualizados.dia, datos_actualizados.hora)
    fin_nueva = inicio_nueva + timedelta(minutes=datos_actualizados.duracion)
    reservas_existentes = db.query(Reserva).filter(
        Reserva.cancha_id == datos_actualizados.cancha_id,
        Reserva.id != reserva_id  
    ).all()

    for reserva_existente in reservas_existentes:
        inicio_existente = datetime.combine(reserva_existente.dia, reserva_existente.hora)
        fin_existente = inicio_existente + timedelta(minutes=reserva_existente.duracion)
        if inicio_nueva < fin_existente and fin_nueva > inicio_existente:
            raise HTTPException(
                status_code=400,
                detail=f"Conflicto de horario con otra reserva: {inicio_existente.time()} a {fin_existente.time()}"
            )
    reserva.dia = datos_actualizados.dia
    reserva.hora = datos_actualizados.hora
    reserva.duracion = datos_actualizados.duracion
    reserva.cancha_id = datos_actualizados.cancha_id

    db.commit()
    db.refresh(reserva)
    return reserva

@router.get("/")
def listar_reservas(dia: str, cancha_id: int, db: Session = Depends(get_db)):
    reservas = db.query(Reserva).filter(
        Reserva.dia == dia,
        Reserva.cancha_id == cancha_id
    ).all()
    return reservas
