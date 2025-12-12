from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    iddetalle = Column(Integer, primary_key=True, index=True)
    idpedido = Column(Integer, ForeignKey("pedido.idpedido"), nullable=False)
    idproducto = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalle_pedidos")
