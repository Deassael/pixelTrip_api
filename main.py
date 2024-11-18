from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

class IngresoBase(BaseModel):
    nombre_usuario:str
    correo:str
    contra:str
    puntaje:int

class IngresoBase2(BaseModel):
    id: int
    nombre_usuario:str
    contra:str

class IngresoBasePuntaje(BaseModel):
    id: int
    puntaje: int

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/crearjugador/", status_code=status.HTTP_201_CREATED)
async def crear_jugador(jugador:IngresoBase, db:db_dependency):
    db_jugador = models.Ingreso(**jugador.dict())
    db.add(db_jugador)
    db.commit()
    return "El jugador se ha creado correctamente"

@app.get("/listajugadores/", status_code=status.HTTP_200_OK)
async def obtener_jugadores(db:db_dependency):
    jugadores = db.query(models.Ingreso).all()
    return jugadores

@app.get("/obtenerjugador/{nombreusuario},{contrajugador}", status_code=status.HTTP_200_OK)
async def obtener_jugador(nombreusuario, contrajugador, db:db_dependency):
    jugadores = db.query(models.Ingreso).filter(models.Ingreso.nombre_usuario==nombreusuario, models.Ingreso.contra==contrajugador).first()
    if jugadores is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugadores

@app.delete("/eliminarjugador/{idjugador}", status_code=status.HTTP_200_OK)
async def eliminar_jugador(idjugador, db:db_dependency):
    jugador = db.query(models.Ingreso).filter(models.Ingreso.id==idjugador).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="No se puede eliminar al jugador porque no existe")
    db.delete(jugador)
    db.commit()
    return "El jugador se ha eliminado correctamente"

@app.post("/actualizarjugador", status_code=status.HTTP_200_OK)
async def actualizar_jugador(jugador:IngresoBase2, db:db_dependency):
    jugadoractualizar = db.query(models.Ingreso).filter(models.Ingreso.id==jugador.id).first()
    if jugadoractualizar is None:
        raise HTTPException(status_code=404, detail="El jugador que intenta actualizar no existe")
    jugadoractualizar.nombre_usuario = jugador.nombre_usuario
    jugadoractualizar.contra = jugador.contra
    db.commit()
    return "Los datos del jugador han sido actualizados"

@app.post("/actualizarpuntaje", status_code=status.HTTP_200_OK)
async def actualizar_puntaje(jugador:IngresoBasePuntaje, db:db_dependency):
    jugadoractualizar = db.query(models.Ingreso).filter(models.Ingreso.id==jugador.id).first()
    if jugadoractualizar is None:
        raise HTTPException(status_code=404, detail="El jugador que intenta actualizar no existe")
    jugadoractualizar.puntaje = jugador.puntaje
    db.commit()
    return "Los datos del jugador han sido actualizados"
