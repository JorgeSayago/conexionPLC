from database.database import getConnection

def verificarLogin(nombre, clave):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT clave FROM usuarios WHERE nombre = %s",(nombre,))
    resultado = cursor.fetchone()

    cursor.close()

    if resultado:
        clave_guardada = resultado[0]
        return clave == clave_guardada
    return False