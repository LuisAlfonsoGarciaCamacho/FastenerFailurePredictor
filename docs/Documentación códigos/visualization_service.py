"""
Servicio de Visualización en Tiempo Real con Streamlit

Este script implementa una aplicación de visualización en tiempo real utilizando Streamlit.
Se conecta a servicios de predicción y datos para mostrar resultados en vivo.

Imports:
    - streamlit: Framework para aplicaciones web interactivas.
    - pandas: Librería para manipulación de datos.
    - requests: Librería para realizar solicitudes HTTP.
    - os: Librería para interactuar con el sistema operativo.
    - pygame: Librería para reproducción de sonido.
    - datetime: Librería para manejar fechas y horas.
    - matplotlib.pyplot: Librería para crear gráficas.
    - streamlit_autorefresh: Plugin de Streamlit para auto refrescar la página.

Funciones:
    - get_model_folders: Obtiene las carpetas de los modelos.
    - get_models: Obtiene los nombres de los modelos dentro de una carpeta.
    - update_prediction_service: Actualiza el modelo en el servicio de predicción.
    - fetch_data: Obtiene datos del servicio de datos.
    - update_data: Actualiza el estado de los datos en la aplicación.
"""

import streamlit as st
import pandas as pd
import requests
import os
import pygame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

pygame.init()

st.title("Visualización en Tiempo Real")

count = st_autorefresh(interval=5000, limit=None, key="autorefresh")

# Inicializar los datos
if 'data' not in st.session_state:
    st.session_state.data = {"angulo": [], "par": [], "prediction": "", "process_count": 0, "identificador": ""}
    st.session_state.last_update_time = datetime.now()
    st.session_state.is_active = True
    st.session_state.save_graphs = True  # Nuevo: inicializar la opción de guardar gráficas

alert_sound = pygame.mixer.Sound(r"C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\docs\Documentación códigos\alert_sound.mp3")

def get_model_folders():
    """
    Obtiene las carpetas que contienen los modelos.

    Returns:
        list: Lista de nombres de carpetas de modelos.
    """
    models_dir = r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\modelos'
    return [f for f in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, f))]

def get_models(folder):
    """
    Obtiene los nombres de los modelos dentro de una carpeta.

    Args:
        folder (str): Nombre de la carpeta que contiene los modelos.

    Returns:
        list: Lista de nombres de modelos (sin extensión .pkl).
    """
    models_dir = os.path.join(r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\modelos', folder)
    return [f.split('.')[0] for f in os.listdir(models_dir) if f.endswith('.pkl') and not f.startswith('scaler')]

model_folders = get_model_folders()
selected_folder = st.selectbox("Seleccione la carpeta del modelo", model_folders)
models = get_models(selected_folder)
selected_model = st.selectbox("Seleccione el modelo", models)
window_size = int(selected_model.split('_')[-1])

# Nuevo: Menú desplegable para decidir si guardar gráficas
st.session_state.save_graphs = st.selectbox("¿Guardar gráficas?", ["Sí", "No"]) == "Sí"

def update_prediction_service():
    """
    Actualiza el modelo en el servicio de predicción.

    Envía una solicitud POST al servicio de predicción para actualizar el modelo.
    """
    try:
        response = requests.post("http://localhost:8001/update_model", json={
            "model_folder": selected_folder,
            "model_name": selected_model,
            "window_size": window_size
        })
        if response.status_code == 200:
            st.success("Modelo actualizado con éxito en el servicio de predicción.")
        else:
            st.error(f"Error al actualizar el modelo: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")

if st.button('Actualizar modelo'):
    update_prediction_service()

def fetch_data():
    """
    Obtiene datos del servicio de datos.

    Returns:
        dict: Diccionario con los datos obtenidos del servicio de datos.
    """
    try:
        response = requests.get("http://localhost:8001/get_data")
        if response.status_code == 200:
            return response.json()
        else:
            return {"angulo": [], "par": [], "prediction": "Error", "reset": False, "identificador": ""}
    except requests.requests.RequestException as e:
        return {"angulo": [], "par": [], "prediction": "Error", "reset": False, "identificador": ""}

def update_data(new_data):
    """
    Actualiza el estado de los datos en la aplicación.

    Args:
        new_data (dict): Diccionario con los nuevos datos obtenidos.
    """
    if new_data["reset"] or new_data["angulo"] or new_data["par"]:
        st.session_state.last_update_time = datetime.now()
        st.session_state.is_active = True
        if new_data["reset"]:
            st.session_state.data["process_count"] += 1
            st.session_state.data["angulo"] = new_data["angulo"]
            st.session_state.data["par"] = new_data["par"]
            st.session_state.data["identificador"] = new_data["identificador"]
        else:
            st.session_state.data["angulo"].extend(new_data["angulo"])
            st.session_state.data["par"].extend(new_data["par"])
        st.session_state.data["prediction"] = new_data["prediction"]
        
        # Reproducir sonido si la predicción es "NOT OK"
        if new_data["prediction"] == "NOT OK":
            alert_sound.play()
    else:
        # Si no hay nuevos datos, verificar si han pasado 10 segundos
        if datetime.now() - st.session_state.last_update_time > timedelta(seconds=10):
            st.session_state.is_active = False

new_data = fetch_data()
update_data(new_data)

st.subheader("Identificador de coche", anchor="identificador")
st.write(f"{st.session_state.data['identificador']}", unsafe_allow_html=True)

st.subheader(f"Proceso de atornillado #{st.session_state.data['process_count']}")

st.subheader("Valores de Ángulo y Par")
st.text_area("Ángulo", value=str(st.session_state.data["angulo"]), height=100, key="angulo_text_area")
st.text_area("Par", value=str(st.session_state.data["par"]), height=100, key="par_text_area")

st.subheader("Gráfica de Ángulo y Par")
if len(st.session_state.data["angulo"]) > 0 and len(st.session_state.data["par"]) > 0:
    df = pd.DataFrame({"Ángulo": st.session_state.data["angulo"], "Par": st.session_state.data["par"]})

    # Crear gráfica con Matplotlib
    fig, ax = plt.subplots()
    ax.scatter(df['Ángulo'], df['Par'])
    ax.set_xlabel('Ángulo')
    ax.set_ylabel('Par')
    ax.set_title('Gráfica de Ángulo y Par')

    st.pyplot(fig)

    # Guardar la gráfica solo si el sistema está activo, la predicción es "NOT OK" y se ha seleccionado guardar gráficas
    if st.session_state.is_active and st.session_state.data["prediction"] == "NOT OK" and st.session_state.save_graphs:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{current_time}_{selected_folder}_{st.session_state.data['identificador']}_{st.session_state.data['prediction']}.png"
        
        os.makedirs('graficas', exist_ok=True)
        
        plt.savefig(os.path.join('graficas', filename))
        st.success(f"Gráfica guardada como {filename}")
    elif not st.session_state.is_active:
        st.warning("No se han recibido nuevos datos en los últimos 10 segundos. No se guardará la gráfica.")
    elif not st.session_state.save_graphs:
        st.info("No se guardará la gráfica porque la opción está desactivada.")

    plt.close(fig)

st.subheader("Predicción")
st.write(st.session_state.data["prediction"])

st.subheader("Modelo seleccionado")
st.write(f"Carpeta: {selected_folder}")
st.write(f"Modelo: {selected_model}")
st.write(f"Tamaño de ventana: {window_size}")
