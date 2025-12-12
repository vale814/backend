from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Pedido(Base):
    __tablename__ = "pedido"
    idpedido = Column(Integer, primary_key=True, index=True)
    idusuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha = Column(DateTime)
    total = Column(Float)
    estado = Column(String(30), default="pendiente")

    usuario = relationship("Usuario", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido")
