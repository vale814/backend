from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PedidoBase(BaseModel):
    idusuario: int
    total: Optional[float] = None
    estado: Optional[str] = "pendiente"

class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    idpedido: int
    fecha: Optional[datetime] = None
    model_config = {"from_attributes": True}
