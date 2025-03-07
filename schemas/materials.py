"""
Módulo de modelos para materiales.

Define las clases Pydantic para la validación de datos de materiales en la API.
"""

from pydantic import BaseModel

class MaterialBase(BaseModel):
    """Modelo base para los materiales."""

    material_type: str
    brand: str
    model: str
    state: str

class MaterialCreate(MaterialBase):
    """Modelo para la creación de materiales."""
    pass

class MaterialUpdate(MaterialBase):
    """Modelo para la actualización de materiales."""
    pass

class Material(MaterialBase):
    """Modelo que representa un material con ID incluido."""

    ID_Material: int

    class Config:
        """Configuración para permitir el uso con ORM."""
        orm_mode = True
