#services\user.py 
import bcrypt
from app.db.db_connection import get_connection
from app.models.user import User, UserCreate, UserUpdate, TemporaryUser

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_usuario_por_correo(correo: str) -> bool:  #esto para el envio de correos para la recuperacion de contraseña
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT COUNT(*) FROM usuario WHERE correo = :correo and estado_usuario = 1 and tipo_usuario_id_tip_user != 2"
    cursor.execute(sql, [correo])
    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result > 0


def existe_correo(correo: str, excluir_correo: str = None) -> bool: #este es para el caso del login, crear cuenta o modificar cuenta, es distindo al get usuario por correo, se maneja el caso donde esta en el form de modificar pero no modifica en si el correo
    conn = get_connection()
    cursor = conn.cursor()

    if excluir_correo:
        sql = "SELECT COUNT(*) FROM usuario WHERE correo = :correo AND correo != :excluir"
        cursor.execute(sql, {'correo': correo, 'excluir': excluir_correo})
    else:
        sql = "SELECT COUNT(*) FROM usuario WHERE correo = :correo"
        cursor.execute(sql, {'correo': correo})

    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result > 0


def login_usuario(correo: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT contrasena
        FROM usuario
        WHERE correo = :correo AND estado_usuario = 1 and tipo_usuario_id_tip_user != 2
    """  #el tipo de usuario 2 seria el temporal, lo cual no es valido para el login en sí por eso se pone distinto
    cursor.execute(sql, [correo])
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result and verify_password(password, result[0]):
        return True
    return False

def crear_usuario(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(user.password)

    sql = """
        INSERT INTO usuario (correo, contrasena, p_nombre, s_nombre, a_paterno, a_materno, comuna_id_comuna, direccion, fono, tipo_usuario_id_tip_user, estado_usuario)
        VALUES (:correo, :password, :p_nombre, :s_nombre, :a_paterno, :a_materno, :comuna, :direccion, :telefono, 1, 1)
    """
    cursor.execute(sql, {
        'correo': user.correo,
        'password': hashed_password,
        'p_nombre': user.p_nombre,
        's_nombre': user.s_nombre,
        'a_paterno': user.a_paterno,
        'a_materno': user.a_materno,
        'comuna': user.comuna,
        'direccion': user.direccion,
        'telefono': user.telefono
    })

    conn.commit()
    cursor.close()
    conn.close()

def actualizar_usuario(correo: str, user_update: UserUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el correo ya existe (exceptuando el propio)
    if existe_correo(user_update.correo, excluir_correo=correo):
        cursor.close()
        conn.close()
        raise ValueError("El correo ya está registrado por otro usuario")

    update_fields = [
        "p_nombre = :p_nombre",
        "s_nombre = :s_nombre",
        "a_paterno = :a_paterno",
        "a_materno = :a_materno",
        "comuna = :comuna",
        "direccion = :direccion",
        "telefono = :telefono"
    ]

    # Actualizar correo y contraseña si están presentes
    if user_update.password:
        update_fields.append("contrasena = :password")
    if user_update.correo:
        update_fields.append("correo = :correo")

    sql = f"UPDATE usuario SET {', '.join(update_fields)} WHERE correo = :correo_actual AND estado_usuario = 1"
    
    params = user_update.dict()
    if user_update.password:
        params['password'] = hash_password(user_update.password)
    params['correo_actual'] = correo

    cursor.execute(sql, params)
    conn.commit()
    cursor.close()
    conn.close()

def ver_info_usuario(correo: str): #esto es para los uusarios que no son de caracter temporal
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT correo, p_nombre, s_nombre, a_paterno, a_materno, comuna, direccion, telefono
        FROM usuario
        WHERE correo = :correo and estado_usuario = 1 and tipo_usuario_id_tip_user != 2
    """
    cursor.execute(sql, [correo])
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return User(correo=result[0], p_nombre=result[1], s_nombre=result[2], a_paterno=result[3],
                    a_materno=result[4], comuna=result[5], direccion=result[6], telefono=result[7])
    return None


def get_next_user_id():
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT COALESCE(MAX(id_usuario), 0) + 1 FROM usuario"
    cursor.execute(sql)
    next_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return next_id


def crear_usuario_temporal():
    conn = get_connection()
    cursor = conn.cursor()

    user_id = get_next_user_id()

    sql = """
        INSERT INTO usuario (id_usuario, tipo_usuario, estado_usuario)
        VALUES (:id_usuario, 3, 1)
    """
    cursor.execute(sql, {'id_usuario': user_id})
    conn.commit()

    cursor.close()
    conn.close()
    return user_id

def actualizar_usuario_temporal(user_id: int, user_data: TemporaryUser):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE usuario
        SET correo = :correo, p_nombre = :p_nombre, a_paterno = :a_paterno, 
            comuna = :comuna, direccion = :direccion
        WHERE id_usuario = :id_usuario 
    """
    cursor.execute(sql, {
        'correo': user_data.correo,
        'p_nombre': user_data.p_nombre,
        'a_paterno': user_data.a_paterno,
        'comuna': user_data.comuna,
        'direccion': user_data.direccion,
        'id_usuario': user_id
    })
    conn.commit()

    cursor.close()
    conn.close()

def get_usuario_temporal(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT correo, p_nombre, a_paterno, comuna_id_comuna, direccion
        FROM usuario
        WHERE id_usuario = :id_usuario AND tipo_usuario_id_tip_user = 2
    """
    cursor.execute(sql, {'id_usuario': user_id})
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return TemporaryUser(correo=result[0], p_nombre=result[1], a_paterno=result[2], comuna=result[3], direccion=result[4])
    return None


def desactivar_usuario_temporal(user_id: int): #se desactiva ya al finalizar el proceso de compra
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE usuario SET estado_usuario = 0 WHERE id_usuario = :id AND tipo_usuario_id_tip_user = 2"
    cursor.execute(sql, {'id': user_id})
    conn.commit()
    cursor.close()
    conn.close()


