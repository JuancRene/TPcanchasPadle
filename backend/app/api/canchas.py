from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CanchaCreate, CanchaResponse  
from app.crud import create_cancha,delete_cancha,delete_all_canchas  
from app.models import Cancha  

router = APIRouter()

@router.post("/", response_model=CanchaResponse)  
def crear_cancha(cancha: CanchaCreate, db: Session = Depends(get_db)):
    return create_cancha(db, cancha)

@router.get("/", response_model=list[CanchaResponse]) 
def obtener_canchas(db: Session = Depends(get_db)):
    canchas = db.query(Cancha).all()  
    return canchas

@router.delete("/cancha/{cancha_id}")
def eliminar_cancha(cancha_id: int, db: Session = Depends(get_db)):
    return delete_cancha(db, cancha_id)

@router.delete("/all")
def eliminar_todas_las_canchas(db: Session = Depends(get_db)):
    delete_all_canchas(db)  
    return {"message": "Todas las canchas han sido eliminadas y el contador reiniciado"}
