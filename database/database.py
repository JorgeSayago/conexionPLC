import psycopg2
from psycopg2.extras import RealDictCursor

# conexion
def getConnection():
    return psycopg2.connect(
        dbname="PLC",
        user = "postgres",
        password ="admin",
        host="localhost"

    )
# guardar registro
def guardar_dato(producto,valor,estado):
    conn = getConnection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO registros_plc (producto, valor, estado)
        VALUES (%s, %s, %s)
    """,(producto,valor,estado))   
    conn.commit()
    cur.close()
    conn.close()

# leer todos los registros
def obtener_registro():
    conn = getConnection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from registros_plc ORDER BY fecha DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows