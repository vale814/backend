from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.pedido import Pedido
from schemas.pedido import Pedido as PedidoSchema, PedidoCreate as PedidoCreateSchema

router = APIRouter()

@router.post("/", response_model=PedidoSchema)
def create_pedido(payload: PedidoCreateSchema, db: Session = Depends(get_db)):
    db_item = Pedido(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[PedidoSchema])
def list_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Pedido).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=PedidoSchema)
def get_pedido(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Pedido).filter(Pedido.idpedido == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Pedido not found")
    return item

@router.put("/{item_id}", response_model=PedidoSchema)
def update_pedido(item_id: int, payload: PedidoCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Pedido).filter(Pedido.idpedido == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Pedido not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_pedido(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Pedido).filter(Pedido.idpedido == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Pedido not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
