#  # import random as rm
# from random import sample

# # num = rm.sample(range(1,100), 10)
# num = sample(range(1,100), 10)
# print(num)

import streamlit as st
import groq

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def configurar_pagina():
    st.set_page_config(page_title="Mi Primer ChatBot con Python")
    st.title("Bienvenidos a mi Chatbot")

def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

def mostrar_sidebar():
    st.sidebar.title("Configuración del Modelo")
    modelo = st.sidebar.selectbox('Selecciona un modelo', MODELOS, index=0)
    st.sidebar.info(f"Modelo seleccionado: {modelo}")
    return modelo

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def obtener_mensaje_usuario():
    return st.chat_input("Escribe tu mensaje aquí...")

def agregar_mensaje(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content

def ejecutar_chat():
    configurar_pagina()
    
    cliente = crear_cliente_groq()
        
    modelo = mostrar_sidebar()
    inicializar_estado_chat()
    obtener_mensajes_previos()
    
    mensaje_usuario = obtener_mensaje_usuario()
    if mensaje_usuario:
        # Mostrar mensaje usuario en UI
        agregar_mensaje("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)
        
        # Obtener respuesta del modelo
        respuesta = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        
        # Imprimir respuesta en terminal (requerimiento del desafío)
        print("=" * 50)
        print(f"Modelo: {modelo}")
        print(f"Usuario: {mensaje_usuario}")
        print(f"Assistant: {respuesta}")
        print("=" * 50)
        
        # Mostrar respuesta en UI
        agregar_mensaje("assistant", respuesta)
        mostrar_mensaje("assistant", respuesta)

if __name__ == '__main__':
    ejecutar_chat()

# Comando para ejecutar archivo: python -m streamlit run main.py