from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from config.db import Base
import enum
from datetime import datetime


class TypeUser(str, enum.Enum):
    Student = "Student"
    Teacher = "Teacher"
    Secretary = "Secretary"
    Laboratory = "Laboratory"
    Executive = "Executive"
    Administrative = "Administrative"

class Status(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Blocked = "Blocked"
    Suspended = "Suspended"

class User(Base):
    __tablename__="tbb_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    last_name = Column(String(60))
    type_user = Column(Enum(TypeUser))
    user_name = Column(String(60))
    email = Column(String(100))
    password = Column(String(60))
    phone_number = Column(String(20))
    status = Column(String(10), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    loans = relationship("Loan", back_populates="user")
