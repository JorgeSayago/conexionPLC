import streamlit as st
from PIL import Image
import pandas as pd
import snap7
from conecction.lectura import leer_datos
from database.database import guardar_dato, obtener_registro

# Mostrar logo arriba solo si existe
try:
    img = Image.open("./assets/logo.jpeg")
    st.image(img, width=400)
except FileNotFoundError:
    pass

st.set_page_config(page_title="Dashboard PLC")

# Parametros de conexion
IP = "192.168.1.10"
RACK = 0
SLOT = 1

# CREAR CONEXION SOLO UNA VEZ
@st.cache_resource
def conectarPLC():
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    return plc 

def main():
    st.title("Recoleccion de datos PLC")

    plc = conectarPLC()

    if st.button("Leer datos del PLC"):
        nuevo = leer_datos(plc)
        guardar_dato(nuevo["Producto"],nuevo["Valor"],nuevo["Estado"])
        st.success("datos guardados en la base")
    
    st.subheader("datos almacenados")
    registros = obtener_registro()
    if registros:
        df = pd.DataFrame(registros)
        st.dataframe(df)
    else:
        st.info("no hay datos registrados aun")


if __name__ == "__main__":
    main()