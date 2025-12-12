from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComentarioBase(BaseModel):
    idusuario: int
    idproducto: int
    comentario: str
    calificacion: Optional[int] = None

class ComentarioCreate(ComentarioBase):
    pass

class Comentario(ComentarioBase):
    idcomentario: int
    fecha: Optional[datetime] = None
    model_config = {"from_attributes": True}
