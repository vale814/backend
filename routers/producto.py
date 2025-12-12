from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.producto import Producto
from models.categoria import Categoria
from schemas.producto import Producto as ProductoSchema, ProductoCreate as ProductoCreateSchema

router = APIRouter()

@router.post("/", response_model=ProductoSchema)
def create_producto(payload: ProductoCreateSchema, db: Session = Depends(get_db)):
    data = payload.dict()
    categoria_val = data.pop("categoria", None)
    # resolver categoria: puede ser id (int/str digits) o nombre (str)
    if categoria_val is not None:
        try:
            cat_id = int(categoria_val)
            categoria = db.query(Categoria).filter(Categoria.idcategoria == cat_id).first()
            if categoria:
                data["categoria_id"] = categoria.idcategoria
        except (ValueError, TypeError):
            # buscar por nombre
            categoria = db.query(Categoria).filter(Categoria.nombre == categoria_val).first()
            if not categoria:
                # crear nueva categoria mínima
                categoria = Categoria(nombre=categoria_val, descripcion=None)
                db.add(categoria)
                db.commit()
                db.refresh(categoria)
            data["categoria_id"] = categoria.idcategoria

    db_item = Producto(**data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[ProductoSchema])
def list_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Producto).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ProductoSchema)
def get_producto(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Producto).filter(Producto.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Producto not found")
    return item

@router.put("/{item_id}", response_model=ProductoSchema)
def update_producto(item_id: int, payload: ProductoCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Producto).filter(Producto.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Producto not found")
    for k, v in payload.dict().items():
        if k == "categoria":
            if v is None:
                setattr(item, "categoria_id", None)
                continue
            try:
                cat_id = int(v)
                categoria = db.query(Categoria).filter(Categoria.idcategoria == cat_id).first()
                if categoria:
                    setattr(item, "categoria_id", categoria.idcategoria)
                    continue
            except (ValueError, TypeError):
                pass
            # buscar o crear por nombre
            categoria = db.query(Categoria).filter(Categoria.nombre == v).first()
            if not categoria:
                categoria = Categoria(nombre=v, descripcion=None)
                db.add(categoria)
                db.commit()
                db.refresh(categoria)
            setattr(item, "categoria_id", categoria.idcategoria)
        else:
            setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_producto(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Producto).filter(Producto.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Producto not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
