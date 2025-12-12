from pydantic import BaseModel
from typing import Optional

class DireccionEnvioBase(BaseModel):
    idusuario: int
    direccion: str
    ciudad: Optional[str] = None
    telefono: Optional[str] = None

class DireccionEnvioCreate(DireccionEnvioBase):
    pass

class DireccionEnvio(DireccionEnvioBase):
    iddireccion: int
    model_config = {"from_attributes": True}
