from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    rol = Column(String(20), default="usuario")

    comentarios = relationship("Comentario", back_populates="usuario")
    pedidos = relationship("Pedido", back_populates="usuario")
    direcciones = relationship("DireccionEnvio", back_populates="usuario")
