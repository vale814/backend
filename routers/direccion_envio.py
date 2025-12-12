from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.direccion_envio import DireccionEnvio
from schemas.direccion_envio import DireccionEnvio as DireccionEnvioSchema, DireccionEnvioCreate as DireccionEnvioCreateSchema

router = APIRouter()

@router.post("/", response_model=DireccionEnvioSchema)
def create_direccion(payload: DireccionEnvioCreateSchema, db: Session = Depends(get_db)):
    db_item = DireccionEnvio(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[DireccionEnvioSchema])
def list_direcciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(DireccionEnvio).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=DireccionEnvioSchema)
def get_direccion(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DireccionEnvio).filter(DireccionEnvio.iddireccion == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Direccion not found")
    return item

@router.put("/{item_id}", response_model=DireccionEnvioSchema)
def update_direccion(item_id: int, payload: DireccionEnvioCreateSchema, db: Session = Depends(get_db)):
    item = db.query(DireccionEnvio).filter(DireccionEnvio.iddireccion == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Direccion not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_direccion(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DireccionEnvio).filter(DireccionEnvio.iddireccion == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Direccion not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
