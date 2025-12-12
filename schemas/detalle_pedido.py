from pydantic import BaseModel

class DetallePedidoBase(BaseModel):
    idpedido: int
    idproducto: int
    cantidad: int
    precio_unitario: float

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedido(DetallePedidoBase):
    iddetalle: int
    model_config = {"from_attributes": True}
