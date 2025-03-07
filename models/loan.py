from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
import enum
from datetime import datetime

class TypeLoan(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Blocked = "Blocked"

class Loan(Base):
    __tablename__ = "tbb_loans"

    ID_Loan = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("tbb_users.id"))
    id_material = Column(Integer, ForeignKey("tbb_materials.ID_Material"))
    loan_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(TypeLoan))

    user = relationship("User", back_populates="loans")
    material = relationship("Material", back_populates="loans")
