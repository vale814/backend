from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.admin import Admin
from schemas.admin import Admin as AdminSchema, AdminCreate as AdminCreateSchema
from schemas.login import LoginRequest, LoginResponse

router = APIRouter()

@router.post("/", response_model=AdminSchema)
def create_admin(payload: AdminCreateSchema, db: Session = Depends(get_db)):
    data = payload.dict()
    data.pop('id', None)
    db_item = Admin(**data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[AdminSchema])
def list_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Admin).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=AdminSchema)
def get_admin(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Admin).filter(Admin.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Admin not found")
    return item

@router.put("/{item_id}", response_model=AdminSchema)
def update_admin(item_id: int, payload: AdminCreateSchema, db: Session = Depends(get_db)):
    item = db.query(Admin).filter(Admin.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Admin not found")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_admin(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Admin).filter(Admin.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Admin not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.post("/login", response_model=LoginResponse)
def login_admin(payload: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == payload.email).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    if admin.password != payload.password:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return {
        "id": admin.id,
        "email": admin.email,
        "nombre": admin.nombre,
        "message": "Login exitoso"
    }

