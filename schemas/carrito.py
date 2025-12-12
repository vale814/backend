from pydantic import BaseModel

class CarritoBase(BaseModel):
    nombreproducto: str
    nombre: str
    direccion: str
    email: str

class CarritoCreate(CarritoBase):
    pass

class Carrito(CarritoBase):
    idcarrito: int
    model_config = {"from_attributes": True}
