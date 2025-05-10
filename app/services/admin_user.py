# app/services/admin_user.py
import bcrypt
import smtplib
from email.message import EmailMessage
from app.db.db_connection import get_connection
from app.models.user import AdminUserCreate, AdmUser
from app.core.config import settings

def get_next_user_id():
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT COALESCE(MAX(id_usuario), 0) + 1 FROM usuario"
    cursor.execute(sql)
    next_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return next_id

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def generar_password(p_nombre: str, rut: str) -> str:
    return f"{p_nombre.strip().lower()}{rut.strip().replace('-', '').replace('.', '')}"

def enviar_credenciales_por_correo(destinatario: str, password: str):
    msg = EmailMessage()
    msg['Subject'] = 'Credenciales de acceso a Ferremas'
    msg['From'] = settings.MAIL_USER
    msg['To'] = destinatario
    msg.set_content(f"""
    Estimado/a,

    Un administrador de Ferremas ha creado una cuenta de empleado en la plataforma. A continuación se presentan sus credenciales:

    Usuario: {destinatario}
    Contraseña: {password}

    Por favor, cambie su contraseña en cuanto inicie sesión.

    Saludos,
    Equipo Ferremas
    """)

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_USER, settings.MAIL_PASSWORD)
        server.send_message(msg)

def crear_cuenta_trabajador(data: AdminUserCreate):
    user_id = get_next_user_id()
    raw_password = generar_password(data.p_nombre, data.rut_usuario)
    hashed = hash_password(raw_password)

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO usuario (id_usuario, correo, contrasena, p_nombre, s_nombre, a_paterno, a_materno,
                             comuna, direccion, telefono, tipo_usuario, sucursal_id,
                             rut_usuario, estado_usuario)
        VALUES (:user_id, :correo, :password, :p_nombre, :s_nombre, :a_paterno, :a_materno,
                :comuna, :direccion, :telefono, :tipo_usuario, :sucursal_id,
                :rut_usuario, 1)
    """

    cursor.execute(sql, {
        'id_usuario': user_id,
        'correo': data.correo,
        'password': hashed,
        'p_nombre': data.p_nombre,
        's_nombre': data.s_nombre,
        'a_paterno': data.a_paterno,
        'a_materno': data.a_materno,
        'comuna': data.comuna,
        'direccion': data.direccion,
        'telefono': data.telefono,
        'tipo_usuario': data.tipo_usuario,
        'sucursal_id': data.sucursal_id,
        'rut_usuario': data.rut_usuario
    })

    conn.commit()
    cursor.close()
    conn.close()

    enviar_credenciales_por_correo(data.correo, raw_password)

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT id_usuario, correo, p_nombre, s_nombre, a_paterno, a_materno, comuna_id_comuna, direccion, telefono
        FROM usuario
        WHERE estado_usuario = 1
    """
    cursor.execute(sql)
    results = cursor.fetchall()

    usuarios = []
    for row in results:
        usuarios.append(AdmUser(
            id_usuario=row[0], correo=row[1], p_nombre=row[2], s_nombre=row[3],
            a_paterno=row[4], a_materno=row[5], comuna=row[6], direccion=row[7], telefono=row[8]
        ))

    cursor.close()
    conn.close()
    return usuarios


def eliminar_usuario(id_usuario: int, id_actual: int):
    if id_usuario == id_actual:
        raise ValueError("No puedes eliminar tu propia cuenta")

    if id_usuario == 8:
        raise ValueError("No se puede eliminar el administrador principal")

    conn = get_connection()
    cursor = conn.cursor()

    # Obtener tipo de usuario a eliminar
    cursor.execute("""
        SELECT tipo_usuario_id_tip_user 
        FROM usuario 
        WHERE id_usuario = :id AND estado_usuario = 1 
    """, {'id': id_usuario})  #revisar bien logica al momento de testear esta funcion esta query principalemnte
    
    row = cursor.fetchone()
    if not row:
        raise ValueError("Usuario no encontrado o ya desactivado")
    
    tipo_usuario_objetivo = row[0]
    
    # Validar si es administrador
    if tipo_usuario_objetivo == 3:
        raise ValueError("No se permite eliminar a otros administradores")

    # Soft delete
    cursor.execute("""
        UPDATE usuario 
        SET estado_usuario = 0 
        WHERE id_usuario = :id
    """, {'id': id_usuario})

    conn.commit()
    cursor.close()
    conn.close()
