import json
import streamlit as st
from database.database import obtener_receta, guardar_receta, obtener_ingrediente


class RecetaPage:

    def mostrar(self):
        st.subheader("Recetas Industriales")
        opcion = st.radio("Que quieres hacer?",["Generar receta","Cargar receta"])

        if opcion == "Generar receta":
            self.generar()
        
        elif opcion == "Cargar receta":
            self.cargar()

    def generar(self):
        if st.session_state.get("guardar_receta"):
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

            guardar_receta(st.session_state.nombre_receta, ingredientes, proceso)
            st.success("✅ Receta guardada correctamente")

            # limpiar todo
            st.session_state.ingredientes = []
            st.session_state.procesos = []
            st.session_state.nombre_receta = ""
            st.session_state.guardar_receta = False

            st.rerun()  # 🔁 reiniciar ejecución sin errores

        # ✅ Paso 2: construir el formulario
        st.subheader("🧪 Generar nueva receta")

        #  INICIALIZAR PRIMERO
        if "ingredientes" not in st.session_state:
            st.session_state.ingredientes = []
        if "procesos" not in st.session_state:
            st.session_state.procesos = []

        ingredientes_disponibles = obtener_ingrediente()
        opciones_ingredientes = [i["nombre"] for i in ingredientes_disponibles]

        st.markdown("### Ingredientes")

        nombre = st.text_input("Nombre de la nueva receta", key="nombre_receta")

        for i,item in enumerate(st.session_state.ingredientes):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                nombre = st.selectbox(f"Ingrediente {i+1}",opciones_ingredientes,index=opciones_ingredientes.index(item["nombre"])if item["nombre"] in opciones_ingredientes else 0, key=f"ing_nombre_{i}")
            with col2:
                cantidad = st.number_input("Cantidad (kg)", min_value=0.0, step=0.01, value=item["cantidad"], key=f"ing_cant_{i}")
            with col3:
                if st.button("🗑️", key=f"eliminar_{i}"):
                    st.session_state.ingredientes.pop(i)
                    st.rerun()
            item["nombre"] = nombre
            item["cantidad"]=cantidad      

        if st.button("Agregar Ingrediente"):
            st.session_state.ingredientes.append({"nombre": "", "cantidad": 0.0})

        st.markdown("### Proceso de Producción")
        if "procesos" not in st.session_state:
            st.session_state.procesos = []

        if st.button("Agregar Proceso"):
            st.session_state.procesos.append({"nombre": "", "tiempo": 0})

        for i, item in enumerate(st.session_state.procesos):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                nombre = st.text_input(f"Proceso {i+1}", value=item["nombre"], key=f"proc_nombre_{i}")
            with col2:
                tiempo = st.number_input("Tiempo (segundos)", min_value=0, step=1, value=item["tiempo"], key=f"proc_tiempo_{i}")
            with col3:
                if st.button("🗑️", key=f"eliminar_proc_{i}"):
                    st.session_state.procesos.pop(i)
                    st.rerun()
            item["nombre"] = nombre
            item["tiempo"] = tiempo

        # ✅ Botón final que solo activa la bandera
        if st.button("Guardar receta"):
            st.session_state.guardar_receta = True

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


