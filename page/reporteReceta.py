import streamlit as st
from database.database import obtener_receta
from utils.pdf import _crear_pdf_tabla
import json

def generar_pdf_recetas():
    recetas = obtener_receta()

    # Convertimos los campos JSON a texto legible para incluir en el PDF
    for receta in recetas:
        receta["ingredientes"] = json.dumps(receta["ingredientes"], ensure_ascii=False)
        receta["proceso"] = json.dumps(receta["proceso"], ensure_ascii=False)

    return _crear_pdf_tabla(recetas, titulo="Reporte de Recetas Industriales")

def mostrarReceta():
    st.markdown("Reporte Recetas")
    datos = obtener_receta()
    if datos:
        st.dataframe(datos)

        if st.button("Generar PDF"):
            pdf = generar_pdf_recetas()
            st.download_button(
                label="Descargar PDF",
                data=pdf,
                file_name="reporte_receta.pdf",
                mime="application/pdf"
            )
    else:
        st.info("no se encontraron datos")