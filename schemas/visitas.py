from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VisitasBase(BaseModel):
    ip: Optional[str] = None
    user_agent: Optional[str] = None

class VisitasCreate(VisitasBase):
    pass

class Visitas(VisitasBase):
    id: int
    fecha: Optional[datetime] = None
    model_config = {"from_attributes": True}
