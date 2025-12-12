from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from database import get_db
from models.categoria import Categoria
from schemas.categoria import Categoria as CategoriaSchema, CategoriaCreate as CategoriaCreateSchema

router = APIRouter()

@router.post("/", response_model=CategoriaSchema)
def create_categoria(payload: CategoriaCreateSchema, db: Session = Depends(get_db)):
    db_item = Categoria(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[CategoriaSchema])
def list_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Categoria).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=CategoriaSchema)
def get_categoria(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Categoria).filter(Categoria.idcategoria == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return item

@router.put("/{item_id}", response_model=CategoriaSchema)
def update_categoria(item_id: int, payload: CategoriaCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Categoria).filter(Categoria.idcategoria == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Categoria not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_categoria(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Categoria).filter(Categoria.idcategoria == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Categoria not found")
    # Asegurarse de que la columna producto.categoria_id existe; si no, crearla.
    try:
        productos = db.execute(text("SELECT id FROM producto WHERE categoria_id = :cid"), {"cid": item_id}).fetchall()
    except OperationalError:
        # Añadir la columna si no existe y continuar
        db.execute(text("ALTER TABLE producto ADD COLUMN categoria_id INTEGER"))
        db.commit()
        productos = []

    # Opcional: desvincular productos asociados antes de borrar la categoría
    if productos:
        try:
            db.execute(text("UPDATE producto SET categoria_id = NULL WHERE categoria_id = :cid"), {"cid": item_id})
        except OperationalError:
            pass

    db.delete(item)
    db.commit()
    return {"ok": True}
