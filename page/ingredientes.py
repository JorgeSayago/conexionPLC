import streamlit as st
from database.database import getConnection
import psycopg2.extras

def mostrar_ingredientes():
    st.subheader("registro de Ingredientes")

    conn = getConnection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, nombre FROM categorias_ingredientes ORDER BY nombre")
    categorias = cur.fetchall()

    codigo = st.text_input("Codigo del ingrediente (ej: ING001)")
    nombre = st.text_input("Nombre del ingrediente (ej: leche)")
    categoria_opciones = [c["nombre"] for c in categorias]
    categoria_seleccionada = st.selectbox("Categoria", categoria_opciones)

    if st.button("Registrar ingrediente"):
        categoria_id = next(c["id"] for c in categorias if c["nombre"])

        try:
            cur.execute(""" 
                INSERT INTO ingredientes (codigo, nombre, categoria_id)
                VALUES (%s, %s, %s)
                """,(codigo.strip(), nombre.strip(),categoria_id()))
        except Exception as e:
            st.error(f"Error al registrar: {e}")
        finally:
            cur.close()
            conn.close()
    
    st.markdown("---")
    st.subheader("ingrediente existente")
    conn = getConnection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT i.codigo, i.nombre, c.nombre AS categoria
        FROM ingredientes i
        JOIN categorias_ingredientes c ON i.categoria_id = c.id
        ORDER BY i.nombre
    """)
    datos = cur.fetchall()
    cur.close()
    conn.close()

    if datos:
        st.dataframe(datos)
    else:
        st.info("no hay ingredientes registrados aun")
