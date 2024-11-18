from sqlalchemy import String, Integer, Column
from database import Base

class Ingreso(Base):
    __tablename__="jugadores"
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50))
    correo = Column(String(100))
    contra = Column(String(25))
    puntaje = Column(Integer)