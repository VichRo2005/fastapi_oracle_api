#routers\admin_user.py
from fastapi import APIRouter, HTTPException
from app.models.user import AdminUserCreate
from app.services.admin_user import crear_cuenta_trabajador, listar_usuarios, eliminar_usuario

router = APIRouter()

@router.post("/admin/crear_cuenta")
async def crear_cuenta(user: AdminUserCreate):
    try:
        crear_cuenta_trabajador(user)
        return {"message": "Cuenta creada y correo enviado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear la cuenta")

@router.get("/admin/listar_usuarios")
async def obtener_usuarios():
    return listar_usuarios()

@router.delete("/admin/eliminar_usuario/{correo}")
async def eliminar_cuenta(correo: str):
    try:
        eliminar_usuario(correo)
        return {"message": "Usuario desactivado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al eliminar el usuario")
