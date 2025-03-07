from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
import crud.material
import config.db
import schemas.materials
import models.material
from typing import List

material = APIRouter()

models.material.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Instancia de seguridad para proteger las rutas
security = HTTPBearer()

# RUTA ABIERTA: Crear material
@material.post("/material/", response_model=schemas.materials.Material, tags=["Materials"])
async def create_material(material_data: schemas.materials.MaterialCreate, db: Session = Depends(get_db)):
    return crud.material.create_material(db=db, material=material_data)

# RUTAS PROTEGIDAS
@material.get("/material/", response_model=List[schemas.materials.Material], tags=["Materials"], dependencies=[Depends(security)])
async def read_materials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.material.get_materials(db=db, skip=skip, limit=limit)

@material.put("/material/{id}", response_model=schemas.materials.Material, tags=["Materials"], dependencies=[Depends(security)])
async def update_material(id: int, material_data: schemas.materials.MaterialUpdate, db: Session = Depends(get_db)):
    db_material = crud.material.update_material(db=db, material_id=id, material=material_data)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

@material.delete("/material/{id}", response_model=schemas.materials.Material, tags=["Materials"], dependencies=[Depends(security)])
async def delete_material(id: int, db: Session = Depends(get_db)):
    db_material = crud.material.delete_material(db=db, material_id=id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material
