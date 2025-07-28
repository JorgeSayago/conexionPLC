import streamlit as st
from database.usuarios import verificarLogin

def mostrarLogin():
    st.title("Inicion de Sesión")

    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña",type="password")
        login_btn = st.form_submit_button("Iniciar Sesión")
    
    if login_btn:
        if verificarLogin(usuario,contrasena):
            st.session_state['logueado'] = True
            st.session_state['usuario'] = usuario
            st.rerun()
        else:
            st.error("usuario o contraseña incorrecta")
