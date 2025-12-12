from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Visitas(Base):
    __tablename__ = "visitas"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    ip = Column(String(45))
    user_agent = Column(String(255))
