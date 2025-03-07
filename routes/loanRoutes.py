from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
import crud.loan
import config.db
import schemas.loans
import models.loan
from typing import List

loan = APIRouter()

models.loan.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Instancia de seguridad para proteger las rutas
security = HTTPBearer()

# RUTA ABIERTA: Crear préstamo
@loan.post("/loan/", response_model=schemas.loans.Loan, tags=["Loans"])
async def create_loan(loan_data: schemas.loans.LoanCreate, db: Session = Depends(get_db)):
    return crud.loan.create_loan(db=db, loan=loan_data)

# RUTAS PROTEGIDAS
@loan.get("/loan/", response_model=List[schemas.loans.Loan], tags=["Loans"], dependencies=[Depends(security)])
async def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.loan.get_loans(db=db, skip=skip, limit=limit)

@loan.put("/loan/{id}", response_model=schemas.loans.Loan, tags=["Loans"], dependencies=[Depends(security)])
async def update_loan(id: int, loan_data: schemas.loans.LoanUpdate, db: Session = Depends(get_db)):
    db_loan = crud.loan.update_loan(db=db, loan_id=id, loan=loan_data)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@loan.delete("/loan/{id}", response_model=schemas.loans.Loan, tags=["Loans"], dependencies=[Depends(security)])
async def delete_loan(id: int, db: Session = Depends(get_db)):
    db_loan = crud.loan.delete_loan(db=db, loan_id=id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan
