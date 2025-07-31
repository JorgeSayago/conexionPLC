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

        nombre = st.text_input("Nombre de la nueva receta", key="nombre_receta")

        st.markdown("### Ingredientes")
        # inicializamos una lista de ingredientes si no existe
        if "ingredientes" not in st.session_state:
            st.session_state.ingredientes = []

        # boton para agrear nuevo ingrediente
        if st.button(" Agregar Ingrediente"):
            st.session_state.ingredientes.append({"nombre": "","cantidad": 0.0})

        # Mostrar inputs para cada ingrediente
        for i, item in enumerate(st.session_state.ingredientes):
            col1, col2, col3 = st.columns([4,2,1])
            with col1:
                nombre = st.text_input(f"Ingrediente {i+1}",value=item["nombre"], key=f"ing_nombre_{i}")
            with col2:
                cantidad = st.number_input(f"Cantidad (kg)", min_value=0.0, step=0.01, value=item["cantidad"], key=f"ing_cant_{i}")
            with col3:
                if st.button("🗑️", key=f"eliminar_{i}"):
                    st.session_state.ingredientes.pop(i)
                    st.experimental_rerun()
            item["nombre"] = nombre
            item["cantidad"] = cantidad

        st.markdown("Proceso de Produccion")

        if "procesos" not in st.session_state:
            st.session_state.procesos = []

        if st.button("Agregar Procesos"):
            st.session_state.procesos.append({"nombre": "","tiempo": 0})

        # mostrar imputs para cada proceso
        for i, item in enumerate(st.session_state.procesos):
            col1, col2, col3 = st.columns([4,2,1])
            with col1:
                nombre = st.text_input(f"proceso {i+1}",value=item["nombre"],key=f"proc_nombre_{i}")
            with col2:
                tiempo = st.number_input(f"tiempo (segundos)",min_value=0, step=1, value=item["tiempo"],key=f"proc_tiempo_{i}") 
            with col3:   
                if st.button("🗑️", key=f"eliminar_Proc{i}"):
                    st.session_state.procesos.pop(i)
                    st.experimental_rerun()
            item["nombre"] = nombre
            item["tiempo"] = tiempo

        if st.button("Guardar receta"):
            ingredientes = {
                item["nombre"]: item["cantidad"]
                for item in st.session_state.ingredientes
                if item["nombre"]
            }
            proceso = [
                {"etapa": item["nombre"], "tiempo": item["tiempo"]}
                for item in st.session_state.procesos
                if item["nombre"]
            ]


            guardar_receta(nombre,ingredientes,proceso)
            st.success("receta guardada correctamente")
            # limpiar los formularios luego de guardarlos
            st.session_state.ingredientes = []  
            st.session_state.procesos = []  
            st.session_state.nombre_receta = ""

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


