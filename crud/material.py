"""
Módulo CRUD para la gestión de materiales en la base de datos.
"""

from sqlalchemy.orm import Session
from models import material as material_model
from schemas import materials as material_schema

def get_materials(db: Session, skip: int = 0, limit: int = 0):
    """Obtiene una lista de materiales con paginación opcional."""
    return db.query(material_model.Material).offset(skip).limit(limit).all()

def get_material(db: Session, material_id: int):
    """Obtiene un material por su ID."""
    return db.query(material_model.Material).filter(
        material_model.Material.id_material == material_id).first()

def create_material(db: Session, material: material_schema.MaterialCreate):
    """Crea un nuevo material en la base de datos."""
    db_material = material_model.Material(
        material_type=material.material_type,
        brand=material.brand,
        model=material.model,
        state=material.state
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def update_material(db: Session, material_id: int, material: material_schema.MaterialUpdate):
    """Actualiza los datos de un material existente."""
    db_material = db.query(material_model.Material).filter(
        material_model.Material.ID_Material == material_id).first()
    if db_material:
        for var, value in vars(material).items():
            if value is not None:
                setattr(db_material, var, value)
        db.commit()
        db.refresh(db_material)
        return db_material
    return None

def delete_material(db: Session, material_id: int):
    """Elimina un material de la base de datos."""
    db_material = db.query(material_model.Material).filter(
        material_model.Material.ID_Material == material_id).first()
    if db_material:
        db.delete(db_material)
        db.commit()
    return db_material
