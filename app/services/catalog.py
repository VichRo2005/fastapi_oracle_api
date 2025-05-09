import oracledb
from app.db.db_connection import get_connection
from app.models.catalog import Product

def get_products_by_sucursal(sucursal_id: int, search: str = None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT p.nombre_producto, p.desc_producto, p.precio, p.imagen
        FROM producto_sucursal ps
        JOIN producto p ON ps.producto_id = p.id_producto
        WHERE ps.sucursal_id = :sucursal_id AND p.estado_producto = 1
        """
        if search:
            query += " AND (LOWER(p.nombre_producto) LIKE :search OR LOWER(p.desc_producto) LIKE :search)"

        params = {'sucursal_id': sucursal_id}
        if search:
            params['search'] = f"%{search.lower()}%"

        cursor.execute(query, params)
        products = [Product(nombre_producto=row[0], desc_producto=row[1], precio=row[2], imagen=row[3]) for row in cursor]

        return products
    except Exception as e:
        print("Error al obtener productos:", e)
        return []
    finally:
        cursor.close()
        conn.close()
