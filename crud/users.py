"""
Módulo CRUD para la gestión de usuarios en la base de datos.
"""

from sqlalchemy.orm import Session
from models import user as user_model
import models 
from schemas import users as user_schema


def get_users(db: Session, skip: int = 0, limit: int = 0):
    """Obtiene una lista de usuarios con paginación opcional."""
    return db.query(user_model.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    """Obtiene un usuario por su ID."""
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, user_email: int):
    """Obtiene un usuario por su email."""
    return db.query(user_model.User).filter(user_model.User.email == user_email).first()

def create_user(db: Session, user: user_schema.userCreate):
    """Crea un nuevo usuario en la base de datos."""
    db_user = user_model.User(
        name=user.name,
        last_name=user.last_name,
        type_user=user.type_user,
        user_name=user.user_name,
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        status=user.status,
        registration_date=user.registration_date,
        update_date=user.update_date
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id, user: user_schema.userUpdate):
    """Actualiza los datos de un usuario existente."""
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        for var, value in vars(user).items():
            if value is not None:
                setattr(db_user, var, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    """Elimina un usuario de la base de datos."""
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def get_user_by_credentials(db: Session, user_name: str = None, email: str = None, phone_number: str = None, password: str = None):
    return db.query(models.user.User).filter(
        (models.user.User.user_name == user_name) |
        (models.user.User.email == email) |
        (models.user.User.phone_number == phone_number)
    ).filter(models.user.User.password == password).first()
