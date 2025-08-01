import streamlit as st
from database.database import getConnection , guardar_ingrediente , obtener_ingrediente
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
        if not codigo or not nombre:
            st.warning(" Por favor complete todos los campos")
        else:
            try:
                categoria_id = next(c["id"] for c in categorias if c["nombre"] == categoria_seleccionada)
                guardar_ingrediente(codigo,nombre,categoria_id)
                st.success("ingrediente guardado correctamente")
                st.session_state.clear()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

    st.markdown("---")
    st.subheader("ingrediente existente")
    datos = obtener_ingrediente()
    if datos:
        st.dataframe(datos)
    else:
        st.info("no hay ingredientes registrados aun")
