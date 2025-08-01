import streamlit as st
from database.database import getConnection, guardar_ingrediente, obtener_ingrediente
import psycopg2.extras

def mostrar_ingredientes():
    st.subheader("Registro de Ingredientes")

    # Obtener categorías desde la base de datos
    conn = getConnection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, nombre FROM categorias_ingredientes ORDER BY nombre")
    categorias = cur.fetchall()
    cur.close()
    conn.close()

    # Asegurar claves únicas para poder limpiar después
    if "ingrediente_form_key" not in st.session_state:
        st.session_state.ingrediente_form_key = 0

    key = st.session_state.ingrediente_form_key

    # Campos del formulario con clave dinámica
    codigo = st.text_input("Código del ingrediente (ej: ING001)", key=f"codigo_ingrediente_{key}")
    nombre = st.text_input("Nombre del ingrediente (ej: leche)", key=f"nombre_ingrediente_{key}")
    categoria_opciones = [c["nombre"] for c in categorias]
    categoria_seleccionada = st.selectbox("Categoría", categoria_opciones, key=f"categoria_ingrediente_{key}")

    if st.button("Registrar ingrediente"):
        if not codigo or not nombre:
            st.warning("Por favor complete todos los campos")
        else:
            try:
                categoria_id = next(c["id"] for c in categorias if c["nombre"] == categoria_seleccionada)
                guardar_ingrediente(codigo.strip(), nombre.strip(), categoria_id)
                st.success("Ingrediente guardado correctamente")

                # Limpiar campos sin cerrar sesión
                st.session_state.ingrediente_form_key += 1

            except Exception as e:
                st.error(f"Error al guardar: {e}")

    st.markdown("---")
    st.subheader("Ingredientes existentes")

    datos = obtener_ingrediente()
    if datos:
        st.dataframe(datos)
    else:
        st.info("No hay ingredientes registrados aún")
