from pydantic import BaseModel

class AdminBase(BaseModel):
    nombre: str
    email: str

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int
    model_config = {"from_attributes": True}
