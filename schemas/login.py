from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    id: int
    email: str
    nombre: str
    message: str
    
    model_config = {"from_attributes": True}
