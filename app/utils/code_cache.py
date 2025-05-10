from datetime import datetime, timedelta
import random

# Diccionario para guardar los códigos
codigo_cache = {}

def generar_codigo_verificacion():
    return str(random.randint(100000, 999999))  # Código de 6 dígitos

def guardar_codigo(correo: str, codigo: str):
    expira = datetime.now() + timedelta(minutes=5)
    codigo_cache[correo] = {'codigo': codigo, 'expira': expira}

def validar_codigo(correo: str, codigo: str) -> bool:
    datos = codigo_cache.get(correo)
    if not datos:
        return False
    if datetime.now() > datos['expira']:
        del codigo_cache[correo]
        return False
    return datos['codigo'] == codigo

def eliminar_codigo(correo: str):
    if correo in codigo_cache:
        del codigo_cache[correo]
