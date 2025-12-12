from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Comentario(Base):
    __tablename__ = "comentario"
    idcomentario = Column(Integer, primary_key=True, index=True)
    idusuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    idproducto = Column(Integer, ForeignKey("producto.id"), nullable=False)
    comentario = Column(Text, nullable=False)
    calificacion = Column(Integer)
    fecha = Column(DateTime)

    usuario = relationship("Usuario", back_populates="comentarios")
    producto = relationship("Producto", back_populates="comentarios")
