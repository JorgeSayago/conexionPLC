from database import getConnection
import psycopg2.extras

def insertar_receta_defecto():
    conn = getConnection()
    cur = conn.cursor()

    receta = {
        "nombre": "Leche sabor fresa",
        "ingredientes": {
            "leche": 1.0,
            "azúcar": 0.12,
            "agua": 0.12,
            "sal": 0.01,
            "colorante": 0.01,
            "fresas": 0.2
        },
        "proceso": [
            {"etapa": "mezclar", "tiempo": 10},
            {"etapa": "homogeneizar", "tiempo": 30},
            {"etapa": "calentar", "tiempo": 60},
            {"etapa": "mezcla_2", "tiempo": 20},
            {"etapa": "enfriar", "tiempo": 30},
            {"etapa": "sellar", "tiempo": 5}
        ]
    }

    cur.execute("""
        INSERT INTO recetas (nombre, ingredientes, proceso)
        VALUES (%s, %s, %s)
    """, (
        receta["nombre"],
        psycopg2.extras.Json(receta["ingredientes"]),
        psycopg2.extras.Json(receta["proceso"])
    ))

    conn.commit()
    cur.close()
    conn.close()