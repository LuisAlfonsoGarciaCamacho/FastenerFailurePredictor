"""
Servicio de Predicción con FastAPI

Este script implementa un servicio de predicción utilizando FastAPI.
Se encarga de cargar modelos de predicción y escalar datos para realizar predicciones.

Imports:
    - fastapi: Framework para construir APIs.
    - pydantic: Librería para validación de datos.
    - numpy: Librería para manejo de matrices y operaciones numéricas.
    - joblib: Librería para cargar modelos serializados.
    - os: Librería para interactuar con el sistema operativo.

Funciones:
    - load_model_and_scaler: Carga el modelo de predicción y el scaler.
    - predict: Realiza una predicción utilizando el modelo y los datos proporcionados.
    - read_root: Ruta raíz de prueba.
    - start_service: Inicia el servidor de FastAPI.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import os

app = FastAPI()

class PredictionRequest(BaseModel):
    """
    Modelo de solicitud de predicción.

    Atributos:
        model_folder (str): Carpeta del modelo.
        model_name (str): Nombre del modelo.
        window_size (int): Tamaño de la ventana de datos.
        angulo (list): Lista de valores de ángulo.
        par (list): Lista de valores de par.
    """
    model_folder: str
    model_name: str
    window_size: int
    angulo: list
    par: list

    class Config:
        protected_namespaces = ()

def load_model_and_scaler(model_folder, model_name, window_size):
    """
    Carga el modelo de predicción y el scaler.

    Args:
        model_folder (str): Carpeta del modelo.
        model_name (str): Nombre del modelo.
        window_size (int): Tamaño de la ventana de datos.

    Returns:
        tuple: Modelo de predicción y scaler.

    Raises:
        FileNotFoundError: Si el modelo o el scaler no existen.
    """
    model_path = os.path.join(r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\modelos', model_folder, f'{model_name}.pkl')
    scaler_path = os.path.join(r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\modelos', model_folder, f'scaler_{window_size}.pkl')

    # Añadir logs para verificar las rutas
    print(f"Model path: {model_path}")
    print(f"Scaler path: {scaler_path}")

    if not os.path.exists(model_path):
        print(f"Model file not found at path: {model_path}")
        raise FileNotFoundError("El modelo especificado no existe.")

    if not os.path.exists(scaler_path):
        print(f"Scaler file not found at path: {scaler_path}")
        raise FileNotFoundError("El scaler especificado no existe.")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

@app.post("/predict")
def predict(request: PredictionRequest):
    """
    Realiza una predicción utilizando el modelo y los datos proporcionados.

    Args:
        request (PredictionRequest): Solicitud de predicción con los datos y configuración del modelo.

    Returns:
        dict: Resultado de la predicción.
    """
    try:
        model, scaler = load_model_and_scaler(request.model_folder, request.model_name, request.window_size)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Verificar que los datos tengan el tamaño correcto
    if len(request.angulo) != request.window_size or len(request.par) != request.window_size:
        raise HTTPException(status_code=400, detail=f"El tamaño de los datos de ángulo y par debe ser {request.window_size}.")

    # Convertir los datos en un numpy array y escalarlo
    data_array = np.array(request.angulo + request.par).reshape(1, -1)
    scaled_data = scaler.transform(data_array)

    # Realizar la predicción
    pred = model.predict(scaled_data)
    result = 'OK' if pred[0] == 0 else 'NOT OK'

    return {"prediction": result}

@app.get("/")
def read_root():
    """
    Ruta raíz de prueba.

    Returns:
        dict: Mensaje de bienvenida.
    """
    return {"message": "FastAPI Prediction Service is running"}

def start_service():
    """
    Inicia el servidor de FastAPI.
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
