from fastapi import FastAPI
from app.routers import user, catalog  # importa el router de usuarios

app = FastAPI()

# Registro del router de usuarios
app.include_router(user.router, prefix="/api")
app.include_router(catalog.router, prefix="/api")
