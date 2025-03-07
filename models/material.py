from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from config.db import Base
import enum

class TypeState(str, enum.Enum):
    Available = "Available"
    Unavailable = "Unavailable"
    Loaned = "Loaned"
    Maintenance = "Maintenance"

class Material(Base):
    __tablename__="tbb_materials"

    ID_Material = Column(Integer, primary_key=True, autoincrement=True)
    material_type = Column(String(60))
    brand = Column(String(60))
    model = Column(String(60))
    state = Column(String(60))

    loans = relationship("Loan", back_populates="material")
    