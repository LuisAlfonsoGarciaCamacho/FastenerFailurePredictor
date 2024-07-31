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

# Servicio de Visualización en Tiempo Real con Streamlit
# Este script implementa una aplicación de visualización en tiempo real utilizando Streamlit.
# Se conecta a servicios de predicción y datos para mostrar resultados en vivo.

import streamlit as st
import pandas as pd
import requests
import os
import pygame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

pygame.init()

# Título de la aplicación
st.title("Visualización de Datos en Tiempo Real")

# Auto refrescar la página cada 5 segundos
count = st_autorefresh(interval=5000, limit=None, key="autorefresh")

# Inicializar los datos en la sesión
if 'data' not in st.session_state:
    st.session_state.data = {"angulo": [], "par": [], "prediction": "", "process_count": 0, "identificador": "", "fecha": ""}
    st.session_state.last_update_time = datetime.now()
    st.session_state.is_active = True
    st.session_state.save_graphs = True  # Nuevo: inicializar la opción de guardar gráficas

# Cargar sonido de alerta
alert_sound_path = "alert_sound.mp3"
alert_sound = pygame.mixer.Sound(alert_sound_path)

# Funciones para obtener modelos
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

# Configuración de la aplicación
st.sidebar.title("Configuración")
model_folders = get_model_folders()
selected_folder = st.sidebar.selectbox("Seleccione la carpeta del modelo", model_folders)
models = get_models(selected_folder)
selected_model = st.sidebar.selectbox("Seleccione el modelo", models)

# Guardar gráficos: menú desplegable
st.session_state.save_graphs = st.sidebar.selectbox("¿Guardar gráficas?", ["Sí", "No"]) == "Sí"

# Función para actualizar el servicio de predicción
def update_prediction_service():
    """
    Actualiza el modelo en el servicio de predicción.
    Envía una solicitud POST al servicio de predicción para actualizar el modelo.
    """
    try:
        # Extraer tamaño de ventana del nombre del modelo
        window_size = int(selected_model.split('_')[-1])
        response = requests.post("http://localhost:8001/update_model", json={
            "model_folder": selected_folder,
            "model_name": selected_model,
            "window_size": window_size,
        })
        if response.status_code == 200:
            st.success("Modelo actualizado con éxito en el servicio de predicción.")
        else:
            st.error(f"Error al actualizar el modelo: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
    except ValueError as ve:
        st.error(f"Error al extraer tamaño de ventana: {str(ve)}")

# Botón para actualizar el modelo
if st.sidebar.button('Actualizar servicio de predicción'):
    update_prediction_service()

# Función para obtener datos del servicio
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
            return {"angulo": [], "par": [], "prediction": "Error", "reset": False, "identificador": "", "fecha": ""}
    except requests.RequestException as e:
        return {"angulo": [], "par": [], "prediction": "Error", "reset": False, "identificador": "", "fecha": ""}

# Función para actualizar los datos en la sesión
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
            st.session_state.data["fecha"] = new_data["fecha"]
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

# Obtener y actualizar los datos
new_data = fetch_data()
update_data(new_data)

# Mostrar información del proceso y datos
st.subheader(f"Proceso de atornillado #{st.session_state.data['process_count']}")
st.write(f"Identificador: {st.session_state.data['identificador']}")
st.write(f"Fecha: {st.session_state.data['fecha']}")

# Mostrar predicción
st.subheader("Predicción")
st.write(st.session_state.data["prediction"])

# Mostrar gráficos de Ángulo y Par
# Mostrar gráficos de Ángulo y Par
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

    # Guardar la gráfica solo si el sistema está activo, se ha seleccionado guardar gráficas, y la predicción es "NOT OK"
    if st.session_state.is_active and st.session_state.save_graphs and st.session_state.data["prediction"] == "NOT OK":
        # Reemplazar caracteres no válidos en la fecha y hora
        safe_date = st.session_state.data["fecha"].replace(":", "-").replace("/", "-")
        safe_identificador = st.session_state.data["identificador"]
        safe_folder = selected_folder
        safe_prediction = st.session_state.data["prediction"]

        # Crear directorio si no existe
        os.makedirs(f'graficas/{safe_identificador}', exist_ok=True)
        
        # Nombre del archivo de la gráfica
        filename = f"{safe_date}_{safe_folder}_{safe_identificador}_{safe_prediction}.png"
        save_path = os.path.join('graficas', safe_identificador, filename)
        
        # Guardar gráfica
        plt.savefig(save_path)
        st.success(f"Gráfica guardada como {save_path}")
    elif not st.session_state.is_active:
        st.warning("No se han recibido nuevos datos en los últimos 10 segundos. No se guardará la gráfica.")
    elif not st.session_state.save_graphs:
        st.info("No se guardará la gráfica porque la opción está desactivada.")
    elif st.session_state.data["prediction"] != "NOT OK":
        st.info("No se guardará la gráfica porque la predicción no es 'NOT OK'.")

    plt.close(fig)


# Mostrar información del modelo seleccionado
st.subheader("Modelo seleccionado")
st.write(f"Carpeta: {selected_folder}")
st.write(f"Modelo: {selected_model}")
