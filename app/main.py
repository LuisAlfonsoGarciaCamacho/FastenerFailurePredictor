"""
Iniciador de Servicios

Este script inicia los servicios de predicción, datos y la aplicación de visualización.

Imports:
    - multiprocessing: Librería para manejar procesos en paralelo.
    - subprocess: Librería para ejecutar comandos del sistema.
    - time: Librería para manejo de tiempo.
    - start_service: Función para iniciar el servicio de predicción (de model_service.py).
    - start_service: Función para iniciar el servicio de datos (de data_service.py).

Funciones:
    - start_streamlit_service: Inicia el servicio de Streamlit.
"""

import multiprocessing
from model_service import start_service as start_prediction_service
from prediction_service import start_service as start_data_service
import subprocess
import time

def start_streamlit_service():
    """
    Inicia el servicio de Streamlit.
    """
    subprocess.run(["streamlit", "run", "visualization_service.py"])

if __name__ == "__main__":
    # Iniciar el servicio de predicción
    p1 = multiprocessing.Process(target=start_prediction_service)
    p1.start()
    print("Servicio de Predicción iniciado en http://localhost:8000")

    # Iniciar el servicio de datos
    p2 = multiprocessing.Process(target=start_data_service)
    p2.start()
    print("Servicio de Datos iniciado en http://localhost:8001")

    # Esperar un momento para asegurarse de que los servicios estén corriendo
    time.sleep(5)

    # Iniciar el servicio de Streamlit
    p3 = multiprocessing.Process(target=start_streamlit_service)
    p3.start()
    print("Servicio de Streamlit iniciado")

    # Mantener el script principal activo
    p1.join()
    p2.join()
    p3.join()
