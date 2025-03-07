"""
Módulo de modelos para usuarios.

Define las clases Pydantic para la validación de datos de usuarios en la API.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    """Modelo base para los usuarios."""

    name: str
    last_name: str
    type_user: str
    user_name: str
    email: str
    password: str
    phone_number: str
    status: str
    registration_date: Optional[datetime] = datetime.utcnow()
    update_date: Optional[datetime] = datetime.utcnow()

class userCreate(UserBase):
    """Modelo para la creación de usuarios."""
    pass

class userUpdate(UserBase):
    """Modelo para la actualización de usuarios."""
    name: str
    last_name: str
    type_user: str
    user_name: str
    email: str
    phone_number: str

class user(UserBase):
    """Modelo que representa un usuario con ID incluido."""

    id: int

    class Config:
        """Configuración para permitir el uso con ORM."""
        orm_mode = True

class UserLogin(BaseModel):
    user_name: Optional [str] = None
    email: Optional [str] = None
    password: str
    phone_number: Optional [str] = None 