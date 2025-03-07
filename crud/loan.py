"""
Módulo CRUD de la API para el área de préstamos.

Este módulo contiene la funcionalidad para gestionar los préstamos,
incluyendo operaciones de consulta, creación, actualización y eliminación.
"""

from sqlalchemy.orm import Session
from models import loan as loan_model
from schemas import loans as loan_schema

def get_loans(db: Session, skip: int = 0, limit: int = 0):
    """Obtiene una lista de préstamos con paginación opcional."""
    return db.query(loan_model.Loan).offset(skip).limit(limit).all()

def get_loan(db: Session, loan_id: int):
    """Obtiene un préstamo por su ID."""
    return db.query(loan_model.Loan).filter(loan_model.Loan.id_loan == loan_id).first()

def create_loan(db: Session, loan: loan_schema.LoanCreate):
    """Crea un nuevo préstamo en la base de datos."""
    db_loan = loan_model.Loan(
        id_user=loan.id_user,
        id_material=loan.id_material,
        loan_date=loan.loan_date,
        return_date=loan.return_date,
        status=loan.status
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def update_loan(db: Session, loan_id: int, loan: loan_schema.LoanUpdate):
    """Actualiza un préstamo existente."""
    db_loan = db.query(loan_model.Loan).filter(loan_model.Loan.ID_Loan == loan_id).first()  # Cambio aquí
    if db_loan:
        for var, value in vars(loan).items():
            if value is not None:
                setattr(db_loan, var, value)
        db.commit()
        db.refresh(db_loan)
        return db_loan
    return None

def delete_loan(db: Session, loan_id: int):
    """Elimina un préstamo de la base de datos."""
    db_loan = db.query(loan_model.Loan).filter(loan_model.Loan.ID_Loan == loan_id).first()
    if db_loan:
        db.delete(db_loan)
        db.commit()
    return db_loan
