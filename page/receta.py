import json
import streamlit as st
from database.database import obtener_receta

class RecetaPage:

    def mostrar(self):
        st.subheader("Recetas Industriales")
        opcion = st.radio("Que quieres hacer?",["Generar receta","Cargar receta"])

        if opcion == "Generar receta":
            self.generar()
        
        elif opcion == "Cargar receta":
            self.cargar()

    def generar(self):
        st.subheader("🧪 Generar nueva receta")

        nombre = st.text_input("Nombre del producto o receta")
        peso = st.number_input("Peso objetivo (g)", step=1)
        tolerancia = st.number_input("Tolerancia (+/- g)", step=1)
        velocidad = st.number_input("Velocidad de operación (RPM)", step=10)
        sello = st.checkbox("Activar sello")

        if st.button("Guardar receta"):
            st.info("📝 Aquí se guardará la receta más adelante.")

    def cargar(self):
        st.subheader("Cargar recetas existentes")

        recetas = obtener_receta()
        if recetas:
            opciones = [r["nombre"] for r in recetas]
            selection = st.selectbox("Seleccione una receta",opciones)
            receta = next(r for r in recetas if r["nombre"] == selection)

            st.markdown(" Ingredientes: ")
            for ing, val in receta["ingredientes"].items():
                st.write(f"- {ing.capitalize()}: {val} kg")
        
        else:
            st.warning("no hay recetas guardadas")
