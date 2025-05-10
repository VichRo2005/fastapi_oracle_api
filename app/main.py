from fastapi import FastAPI
from app.routers import user, catalog, admin_user  # importa el router de usuarios
import multiprocessing

app = FastAPI()

# Registro del router de usuarios
app.include_router(user.router, prefix="/api")
app.include_router(catalog.router, prefix="/api")
app.include_router(admin_user.router, prefix="/api")

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Importante para Windows y PyInstaller
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
