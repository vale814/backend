from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    rol: str
    model_config = {"from_attributes": True}
