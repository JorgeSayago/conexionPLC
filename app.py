import streamlit as st
from PIL import Image
import pandas as pd
import snap7
from conecction.lectura import leer_datos
from conecction.manager import PLCManager
from database.database import guardar_dato, obtener_registro
from page.login import mostrarLogin
from page.receta import RecetaPage

# Mostrar logo arriba solo si existe
try:
    img = Image.open("./assets/logo.jpeg")
    st.image(img, width=400)
except FileNotFoundError:
    pass

st.set_page_config(page_title="Dashboard PLC")

def main():
    if "paso_vida" not in st.session_state:
        st.session_state.paso_vida = 0


    if "usuario" not in st.session_state:
        mostrarLogin()
        return
    
    st.sidebar.success(f"Bienvenido, {st.session_state['usuario']}")
    st.title("Recoleccion de datos PLC")

    plc = PLCManager()

    recetaPage = RecetaPage()
    recetaPage.mostrar()

#    st.subheader("Estado del PLC (bit de vida)")
#    estado = plc.leer_bit_vida()
#    st.info(estado)

    if st.button("Leer datos del PLC"):
        nuevo = plc.leer_y_guardar()
#        st.success("datos guardados en la base")
        plc.enviar_bit_vida(st.session_state.paso_vida)
        st.session_state.paso_vida = (st.session_state.paso_vida + 1) % 4
        st.success("✅ Datos guardados y bit de vida enviado")

    st.subheader("datos almacenados")
    registros = obtener_registro()
    if registros:
        df = pd.DataFrame(registros)
        st.dataframe(df)
    else:
        st.info("no hay datos registrados aun")


if __name__ == "__main__":
    main()