#routers\user.py
from fastapi import APIRouter, HTTPException
from app.services.user import crear_usuario, get_usuario_por_correo, login_usuario, actualizar_usuario, ver_info_usuario, crear_usuario_temporal, actualizar_usuario_temporal, get_usuario_temporal, existe_correo, desactivar_usuario_temporal
from app.models.user import UserCreate, UserUpdate, TemporaryUser

from app.utils.code_cache import generar_codigo_verificacion, guardar_codigo, validar_codigo, eliminar_codigo
from app.utils.email import enviar_codigo_verificacion


router = APIRouter()

@router.post("/user/register")
async def register(user: UserCreate):
    if existe_correo(user.correo):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    crear_usuario(user)
    return {"message": "Usuario registrado con éxito"}


@router.post("/user/login")
async def login(user: UserCreate):
    if not login_usuario(user.correo, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"message": "Inicio de sesión exitoso"}


@router.put("/user/update")
async def update_user(correo: str, user_update: UserUpdate):
    try:
        actualizar_usuario(correo, user_update)
        return {"message": "Información del usuario actualizada"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/user/info")
async def get_user_info(correo: str):
    user = ver_info_usuario(correo)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/user/temporary")
async def create_temporary_user():
    user_id = crear_usuario_temporal()
    return {"message": "Usuario temporal creado", "user_id": user_id}

@router.put("/user/temporary/{user_id}")
async def update_temporary_user(user_id: int, user_data: TemporaryUser):
    temp_user = get_usuario_temporal(user_id)
    if not temp_user:
        raise HTTPException(status_code=404, detail="Usuario temporal no encontrado")
    actualizar_usuario_temporal(user_id, user_data)
    return {"message": "Usuario temporal actualizado"}

@router.get("/user/temporary/{user_id}")
async def get_temporary_user(user_id: int):
    temp_user = get_usuario_temporal(user_id)
    if not temp_user:
        raise HTTPException(status_code=404, detail="Usuario temporal no encontrado")
    return temp_user

@router.post("/user/temporary/deactivate/{user_id}")
async def deactivate_temporary_user(user_id: int):
    desactivar_usuario_temporal(user_id)
    return {"message": "Usuario temporal desactivado correctamente"}

@router.post("/user/send-recovery-code")
async def enviar_codigo(correo: str):
    # Verifica que el correo esté registrado
    if not get_usuario_por_correo(correo):
        raise HTTPException(status_code=404, detail="Correo no encontrado")

    codigo = generar_codigo_verificacion()
    guardar_codigo(correo, codigo)
    enviar_codigo_verificacion(correo, codigo)
    return {"message": "Código enviado al correo"}

@router.post("/user/verify-recovery-code")
async def verificar_codigo(correo: str, codigo: str):
    if validar_codigo(correo, codigo):
        eliminar_codigo(correo)
        return {"message": "Código verificado correctamente"}
    raise HTTPException(status_code=400, detail="Código inválido o expirado")