"""
Módulo de modelos para préstamos.

Define las clases Pydantic para la validación de datos de préstamos en la API.
"""

from datetime import datetime
from pydantic import BaseModel

class LoanBase(BaseModel):
    """Modelo base para los préstamos."""   
    id_user: int
    id_material: int
    loan_date: datetime
    return_date: datetime
    status: str

class LoanCreate(LoanBase):
    """Modelo para la creación de préstamos."""
    id_user: int
    id_material: int
    loan_date: datetime
    return_date: datetime
    status: str
class LoanUpdate(LoanBase):
    """Modelo para la actualización de préstamos."""
    pass

class Loan(LoanBase):
    """Modelo que representa un préstamo con ID incluido."""

    ID_Loan: int

    class Config:
        """Configuración para permitir el uso con ORM."""
        orm_mode = True
