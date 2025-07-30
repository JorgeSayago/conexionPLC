import json
import streamlit as st
from database.database import obtener_receta, guardar_receta

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

        st.markdown("### Ingredientes")
        leche = st.number_input("leche (kg)", step=0.001)
        azucar = st.number_input("Azucar (kg)",step=0.01)
        agua = st.number_input("Agua (L)",step=0.01)
        sal = st.number_input("Sal (kg)",step=0.01)
        colorante = st.number_input("Colorante (kg)",step=0.01)
        fresas = st.number_input("Fresas (kg)",step=0.01)

        st.markdown("Proceso de Produccion")
        tiempo_mezcla = st.number_input("Mezcla inicial (segundos)",step=1)
        tiempo_homogenizado = st.number_input("Homogenizacion (segundos)",step=1)
        tiempo_calentado = st.number_input("Calentamiento (segundos)",step=1)
        tiempo_mezcla2 = st.number_input("Segunda mezcla (segundos)",step=1)
        tiempo_enfriado = st.number_input("Enfriamiento (segundos)", step=1)
        tiempo_sello = st.number_input("Sellado (segundos)",step=1)

        if st.button("Guardar receta"):
            ingredientes = {
                "leche":leche,
                "azucar": azucar,
                "agua":agua,
                "sal":sal,
                "colorante":colorante,
                "fresas": fresas
            }
            proceso =[
                {"etapa": "mezclar","tiempo":tiempo_mezcla},
                {"etapa":"homogenizar","tiempo":tiempo_homogenizado},
                {"etapa":"calentar","tiempo":tiempo_calentado},
                {"etapa":"mezcla 2","tiempo":tiempo_mezcla2},
                {"etapa":"enfriar","tiempo":tiempo_enfriado},
                {"etapa":"sellar","tiempo":tiempo_sello}
            ]

            guardar_receta(nombre,ingredientes,proceso)
            st.success("receta guardada correctamente")

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


