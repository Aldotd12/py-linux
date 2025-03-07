from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jwt_config import valida_token
import crud.users, config.db, models.user

models.user.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Portador(HTTPBearer):
    async def __call__(self, request, db: Session = Depends(get_db)):
        autorizacion = await super().__call__(request)
        dato = valida_token(autorizacion.credentials)
        db_userlogin = crud.users.get_user_by_credentials(
            db,
            username=dato["user_name"],
            correo=dato["email"],
            telefono=dato["phone_number"], 
            password=dato["password"]
        )
        if db_userlogin is None:
            raise HTTPException(status_code=404, detail="login error")
        return db_userlogin
