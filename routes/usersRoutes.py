from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from typing import List

import crud.users
import config.db
import schemas.users
import models.user
from jwt_config import solicita_token  # Función para generar el token JWT

user = APIRouter()
auth_router = APIRouter()

# Crear las tablas si no existen
models.user.Base.metadata.create_all(bind=config.db.engine)

# Instancia de seguridad para rutas protegidas
security = HTTPBearer()

# Contexto para verificar contraseñas (aunque por ahora se comparan directamente)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ RUTA ABIERTA - CREAR USUARIO
@user.post("/user/", response_model=schemas.users.user, tags=["Usuarios"])
async def create_user(user_data: schemas.users.userCreate, db: Session = Depends(get_db)):
    existing_user = crud.users.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return crud.users.create_user(db=db, user=user_data)

# 🔒 RUTA PROTEGIDA - OBTENER USUARIOS
@user.get("/user/", response_model=List[schemas.users.user], tags=["Usuarios"], dependencies=[Depends(security)])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.users.get_users(db=db, skip=skip, limit=limit)

# 🔒 RUTA PROTEGIDA - ACTUALIZAR USUARIO
@user.put("/user/{id}", response_model=schemas.users.user, tags=["Usuarios"], dependencies=[Depends(security)])
async def update_user(id: int, user_data: schemas.users.userUpdate, db: Session = Depends(get_db)):
    db_user = crud.users.update_user(db=db, user_id=id, user=user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# 🔒 RUTA PROTEGIDA - ELIMINAR USUARIO
@user.delete("/user/{id}", response_model=schemas.users.user, tags=["Usuarios"], dependencies=[Depends(security)])
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.users.delete_user(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# ✅ RUTA ABIERTA - LOGIN
@auth_router.post("/auth/login")
async def login(user_data: schemas.users.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.users.get_user_by_email(db, user_data.email)
    
    if not db_user or user_data.password != db_user.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = solicita_token({"sub": db_user.email})
    return {"token": token}
