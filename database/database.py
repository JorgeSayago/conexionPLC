import json
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extras import Json

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

def obtener_receta():
    conn = getConnection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM recetas ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def guardar_receta(nombre, ingredientes, proceso):
    conn = getConnection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO recetas (nombre, ingredientes, proceso)
        VALUES (%s, %s, %s)
    """,(nombre,Json(ingredientes),Json(proceso)) )
    conn.commit()
    cur.close()
    conn.close()