from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    descripcion = Column(String(500))
    precio = Column(Float, nullable=False)
    imagen = Column(String(255))
    categoria_id = Column(Integer, ForeignKey("categoria.idcategoria"))
    stock = Column(Integer, default=0)
    creado_en = Column(DateTime)
    actualizado_en = Column(DateTime)

    categoria_rel = relationship("Categoria", back_populates="productos")
    comentarios = relationship("Comentario", back_populates="producto")
    detalle_pedidos = relationship("DetallePedido", back_populates="producto")
