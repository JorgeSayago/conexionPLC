import streamlit as st
from PIL import Image
import pandas as pd
import snap7
from conecction.lectura import leer_datos
from conecction.manager import PLCManager
from database.database import guardar_dato, obtener_registro
from page.login import mostrarLogin
from page.receta import RecetaPage
from page.ingredientes import mostrar_ingredientes
from page.reporteReceta import mostrarReceta

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

    # Navegación
    pagina = st.sidebar.radio("Menú", ["Dashboard", "Recetas", "Ingredientes","Reporte Recetas"])

    if pagina == "Dashboard":
        st.title("Recoleccion de datos PLC")
        plc = PLCManager()

        registros = []  # ← Asignamos lista vacía por defecto

        if st.button("Leer datos del PLC"):
            nuevo = plc.leer_y_guardar()
            plc.enviar_bit_vida(st.session_state.paso_vida)
            st.session_state.paso_vida = (st.session_state.paso_vida + 1) % 4
            st.success("✅ Datos guardados y bit de vida enviado")
            registros = obtener_registro()  # ← solo si hace clic

        st.subheader("datos almacenados")
        if registros:
            df = pd.DataFrame(registros)
            st.dataframe(df)
        else:
            st.info("no hay datos registrados aun")
        

    elif pagina == "Recetas":
        recetaPage = RecetaPage()
        recetaPage.mostrar()

    elif pagina == "Ingredientes":
        mostrar_ingredientes()
    
    elif pagina == "Reporte Recetas":
        mostrarReceta()

    


#    recetaPage = RecetaPage()
#    recetaPage.mostrar()

#    st.subheader("Estado del PLC (bit de vida)")
#    estado = plc.leer_bit_vida()
#    st.info(estado)




if __name__ == "__main__":
    main()