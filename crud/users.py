"""
Módulo CRUD para la gestión de usuarios en la base de datos.
"""

from sqlalchemy.orm import Session
from models import user as user_model
from schemas import users as user_schema
from datetime import datetime

# 🔹 Obtener todos los usuarios
def get_users(db: Session, skip: int = 0, limit: int = 0):
    return db.query(user_model.User).offset(skip).limit(limit).all()

# 🔹 Obtener usuario por ID
def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

# 🔹 Obtener usuario por email
def get_user_by_email(db: Session, user_email: str):
    return db.query(user_model.User).filter(user_model.User.email == user_email).first()

# 🔹 Crear nuevo usuario
def create_user(db: Session, user: user_schema.userCreate):
    db_user = user_model.User(
        name=user.name,
        last_name=user.last_name,
        type_user=user.type_user,
        user_name=user.user_name,
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        status=user.status,
        registration_date=user.registration_date or datetime.utcnow(),
        update_date=user.update_date or datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 🔹 Actualizar usuario existente
def update_user(db: Session, user_id: int, user: user_schema.userUpdate):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        for var, value in vars(user).items():
            if value is not None:
                setattr(db_user, var, value)
        db_user.update_date = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

# 🔹 Eliminar usuario
def delete_user(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# 🔹 Obtener usuario por credenciales (para login)
def get_user_by_credentials(
    db: Session,
    user_name: str = None,
    email: str = None,
    phone_number: str = None,
    password: str = None
):
    return db.query(user_model.User).filter(
        (user_model.User.user_name == user_name) |
        (user_model.User.email == email) |
        (user_model.User.phone_number == phone_number)
    ).filter(user_model.User.password == password).first()
