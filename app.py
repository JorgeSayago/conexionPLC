import streamlit as st
from PIL import Image
import pandas as pd
import snap7
from conecction.lectura import leer_datos

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
        if "datos" not in st.session_state:
            st.session_state.datos = []

            st.session_state.datos.append(nuevo)
            st.success("Datos leidos")
    
    # mostrar en la tabla
    if "datos" in st.session_state and st.session_state.datos:
        df = pd.DataFrame(st.session_state.datos)
        st.dataframe(df)


if __name__ == "__main__":
    main()