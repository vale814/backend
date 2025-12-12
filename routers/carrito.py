from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.carrito import Carrito
from schemas.carrito import Carrito as CarritoSchema, CarritoCreate as CarritoCreateSchema

router = APIRouter()

@router.post("/", response_model=CarritoSchema)
def create_carrito(payload: CarritoCreateSchema, db: Session = Depends(get_db)):
    db_item = Carrito(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[CarritoSchema])
def list_carritos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Carrito).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=CarritoSchema)
def get_carrito(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Carrito).filter(Carrito.idcarrito == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Carrito not found")
    return item

@router.put("/{item_id}", response_model=CarritoSchema)
def update_carrito(item_id: int, payload: CarritoCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Carrito).filter(Carrito.idcarrito == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Carrito not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_carrito(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Carrito).filter(Carrito.idcarrito == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Carrito not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
