from app.db.db_connection import get_connection

def get_usuario_por_correo(correo: str):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT correo, p_nombre, a_paterno
        FROM usuario
        WHERE correo = :correo AND estado_usuario = 1
    """
    cursor.execute(sql, [correo])
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result
