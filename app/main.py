from fastapi import FastAPI
from app.routers import user  # importa el router de usuarios

app = FastAPI()

# Registro del router de usuarios
app.include_router(user.router)
