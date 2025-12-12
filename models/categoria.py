from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Categoria(Base):
    __tablename__ = "categoria"
    idcategoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(255))

    productos = relationship("Producto", back_populates="categoria_rel")
