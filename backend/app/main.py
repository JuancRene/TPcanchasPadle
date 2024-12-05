from fastapi import FastAPI
from app.api import canchas, reservas
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Dirección de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite cualquier método HTTP
    allow_headers=["*"],  # Permite cualquier encabezado
)

app.include_router(canchas.router, prefix="/api/canchas", tags=["Canchas"])
app.include_router(reservas.router, prefix="/api/reservas", tags=["Reservas"])

