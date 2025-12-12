from sqlalchemy import Column, Integer, String
from database import Base

class Carrito(Base):
    __tablename__ = "carrito"
    idcarrito = Column(Integer, primary_key=True, index=True)
    nombreproducto = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
