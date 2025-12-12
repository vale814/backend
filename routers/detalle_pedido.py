from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.detalle_pedido import DetallePedido
from schemas.detalle_pedido import DetallePedido as DetallePedidoSchema, DetallePedidoCreate as DetallePedidoCreateSchema

router = APIRouter()

@router.post("/", response_model=DetallePedidoSchema)
def create_detalle(payload: DetallePedidoCreateSchema, db: Session = Depends(get_db)):
    db_item = DetallePedido(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[DetallePedidoSchema])
def list_detalles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(DetallePedido).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=DetallePedidoSchema)
def get_detalle(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DetallePedido).filter(DetallePedido.iddetalle == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Detalle not found")
    return item

@router.put("/{item_id}", response_model=DetallePedidoSchema)
def update_detalle(item_id: int, payload: DetallePedidoCreateSchema, db: Session = Depends(get_db)):
    item = db.query(DetallePedido).filter(DetallePedido.iddetalle == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Detalle not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_detalle(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DetallePedido).filter(DetallePedido.iddetalle == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Detalle not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
