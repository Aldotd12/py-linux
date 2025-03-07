from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
import crud.users
import config.db
from jwt_config import solicita_token  # Importa create_access_token
import schemas.users
import models.user
from typing import List
from passlib.context import CryptContext  # Importa Passlib para la verificación de contraseñas



user = APIRouter()
auth_router = APIRouter()

models.user.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Instancia de seguridad
security = HTTPBearer()

# Función para verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

# RUTA ABIERTA: Crear usuario (Registro)
@user.post("/user/", response_model=schemas.users.user, tags=["Usuarios"])
async def create_user(user_data: schemas.users.userCreate, db: Session = Depends(get_db)):
    db_user = crud.users.create_user(db=db, user=user_data)
    return db_user

# RUTAS PROTEGIDAS
@user.get("/user/", response_model=List[schemas.users.user], tags=["Users"], dependencies=[Depends(security)])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.users.get_users(db=db, skip=skip, limit=limit)

@user.put("/user/{id}", response_model=schemas.users.user, tags=["Usuarios"], dependencies=[Depends(security)])
async def update_user(id: int, user_data: schemas.users.userUpdate, db: Session = Depends(get_db)):
    db_user = crud.users.update_user(db=db, user_id=id, user=user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user.delete("/user/{id}", response_model=schemas.users.user, tags=["Usuarios"], dependencies=[Depends(security)])
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.users.delete_user(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@auth_router.post("/auth/login")
async def login(user_data: schemas.users.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.users.get_user_by_email(db, user_data.email)
    
    if not db_user or user_data.password != db_user.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # deberia de generar elntoken 
    token = solicita_token({"sub": db_user.email})
    return {"token": token}
