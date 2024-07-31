# main module

Iniciador de Servicios

Este script inicia los servicios de predicción, datos y la aplicación de visualización.

Imports:
: - multiprocessing: Librería para manejar procesos en paralelo.
  - subprocess: Librería para ejecutar comandos del sistema.
  - time: Librería para manejo de tiempo.
  - start_service: Función para iniciar el servicio de predicción (de model_service.py).
  - start_service: Función para iniciar el servicio de datos (de prediction_service.py).

Funciones:
: - start_streamlit_service: Inicia el servicio de Streamlit.

### main.start_streamlit_service()

Inicia el servicio de Streamlit.
