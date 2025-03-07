from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from routes.usersRoutes import user, auth_router  # Asegúrate de importar auth_router
from routes.materialRoutes import material
from routes.loanRoutes import loan
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app = FastAPI(
    title="API ALDOTD12 ",
    description="API de pruebas con rutas protegidas "
)

# Configurar autenticación con HTTPBearer
security = HTTPBearer()

# Registrar rutas (agregar autenticación solo en rutas protegidas)
app.include_router(user, dependencies=[Depends(security)])
app.include_router(auth_router)  
app.include_router(material)
app.include_router(loan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

