from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.comentario import Comentario
from schemas.comentario import Comentario as ComentarioSchema, ComentarioCreate as ComentarioCreateSchema

router = APIRouter()

@router.post("/", response_model=ComentarioSchema)
def create_comentario(payload: ComentarioCreateSchema, db: Session = Depends(get_db)):
    db_item = Comentario(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[ComentarioSchema])
def list_comentarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Comentario).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ComentarioSchema)
def get_comentario(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Comentario).filter(Comentario.idcomentario == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Comentario not found")
    return item

@router.put("/{item_id}", response_model=ComentarioSchema)
def update_comentario(item_id: int, payload: ComentarioCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Comentario).filter(Comentario.idcomentario == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Comentario not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_comentario(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Comentario).filter(Comentario.idcomentario == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Comentario not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
