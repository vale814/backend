from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    imagen: Optional[str] = None
    categoria: Optional[str] = None
    stock: int = 0

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    model_config = {"from_attributes": True}
