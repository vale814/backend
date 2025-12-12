from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DireccionEnvio(Base):
    __tablename__ = "direccion_envio"
    iddireccion = Column(Integer, primary_key=True, index=True)
    idusuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    direccion = Column(String(100), nullable=False)
    ciudad = Column(String(100))
    telefono = Column(String(20))

    usuario = relationship("Usuario", back_populates="direcciones")
