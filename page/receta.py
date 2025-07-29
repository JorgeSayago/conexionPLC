import streamlit as st

class RecetaPage:

    def motrar(self):
        st.subheader("Recetas Industriales")
        opcion = st.radio("Que quieres hacer?",["Generar receta","Cargar receta"])

        if opcion == "Generar receta":
            self.generar()
        
        elif opcion == "Cargar Receta":
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
        st.info("cargar recetas")