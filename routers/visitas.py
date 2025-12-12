from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.visitas import Visitas
from schemas.visitas import Visitas as VisitasSchema, VisitasCreate as VisitasCreateSchema

router = APIRouter()

@router.post("/", response_model=VisitasSchema)
def create_visita(payload: VisitasCreateSchema, db: Session = Depends(get_db)):
    db_item = Visitas(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[VisitasSchema])
def list_visitas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Visitas).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=VisitasSchema)
def get_visita(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Visitas).filter(Visitas.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Visita not found")
    return item

@router.put("/{item_id}", response_model=VisitasSchema)
def update_visita(item_id: int, payload: VisitasCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Visitas).filter(Visitas.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Visita not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_visita(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Visitas).filter(Visitas.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Visita not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
