#models\user.py
from pydantic import BaseModel, EmailStr, Optional

from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    correo: EmailStr
    password: str


class User(BaseModel):
    correo: EmailStr
    p_nombre: str
    s_nombre: Optional[str] = None
    a_paterno: str
    a_materno: Optional[str] = None
    comuna: int
    direccion: str
    telefono: Optional[str] = None

class UserCreate(BaseModel):
    correo: EmailStr
    password: str
    p_nombre: str
    s_nombre: Optional[str] = None
    a_paterno: str
    a_materno: Optional[str] = None
    comuna: int
    direccion: str
    telefono: Optional[str] = None

class UserUpdate(BaseModel):
    correo: EmailStr
    password: Optional[str] = None
    p_nombre: str
    s_nombre: Optional[str] = None
    a_paterno: str
    a_materno: Optional[str] = None
    comuna: int
    direccion: str
    telefono: Optional[str] = None

class TemporaryUser(BaseModel):
    correo: EmailStr
    p_nombre: str
    a_paterno: str
    comuna: int
    direccion: str

class AdminUserCreate(BaseModel):
    correo: EmailStr
    p_nombre: str
    s_nombre: Optional[str] = None
    a_paterno: str
    a_materno: Optional[str] = None
    comuna: int
    direccion: str
    telefono: Optional[str] = None
    tipo_usuario: int
    sucursal_id: int
    rut_usuario: str

class AdmUser(BaseModel):
    id_usuario: int
    correo: EmailStr
    p_nombre: str
    s_nombre: Optional[str] = None
    a_paterno: str
    a_materno: Optional[str] = None
    comuna: int
    direccion: str
    telefono: Optional[str] = None