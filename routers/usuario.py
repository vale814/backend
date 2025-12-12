from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.usuario import Usuario as UsuarioSchema, UsuarioCreate as UsuarioCreateSchema
from schemas.login import LoginRequest, LoginResponse

router = APIRouter()

@router.post("/", response_model=UsuarioSchema)
def create_usuario(payload: UsuarioCreateSchema, db: Session = Depends(get_db)):
    data = payload.dict()
    data.pop('id', None)
    db_item = Usuario(**data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[UsuarioSchema])
def list_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Usuario).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=UsuarioSchema)
def get_usuario(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Usuario).filter(Usuario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return item

@router.put("/{item_id}", response_model=UsuarioSchema)
def update_usuario(item_id: int, payload: UsuarioCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Usuario).filter(Usuario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Usuario not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_usuario(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Usuario).filter(Usuario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Usuario not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.post("/login", response_model=LoginResponse)
def login_usuario(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    if usuario.password != payload.password:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "message": "Login exitoso"
    }

