"""
Servicio de Datos con FastAPI

Este script implementa un servicio de datos utilizando FastAPI.
Se encarga de recibir, procesar y enviar datos para la predicción.

Imports:
    - fastapi: Framework para construir APIs.
    - pydantic: Librería para validación de datos.
    - requests: Librería para realizar solicitudes HTTP.

Funciones:
    - update_model: Actualiza la información del modelo.
    - receive_data: Recibe y procesa los datos.
    - get_data: Envía los datos almacenados.
    - health_check: Verifica el estado del servidor.
    - start_service: Inicia el servidor de FastAPI.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
import requests

app = FastAPI()

class DataRequest(BaseModel):
    """
    Modelo de solicitud de datos.

    Atributos:
        angulo (list): Lista de valores de ángulo.
        par (list): Lista de valores de par.
        reset (bool): Indicador de reinicio de datos.
        identificador (str): Identificador del coche.
    """
    angulo: list
    par: list
    reset: bool
    identificador: str  # Nuevo campo para el identificador

class ModelUpdateRequest(BaseModel):
    """
    Modelo de solicitud de actualización del modelo.

    Atributos:
        model_folder (str): Carpeta del modelo.
        model_name (str): Nombre del modelo.
        window_size (int): Tamaño de la ventana de datos.
    """
    model_config = ConfigDict(protected_namespaces=())
    model_folder: str
    model_name: str
    window_size: int

data = {"angulo": [], "par": [], "prediction": "", "reset": False, "identificador": ""}
model_info = {"model_folder": "", "model_name": "", "window_size": 0}

@app.post("/update_model")
async def update_model(request: ModelUpdateRequest):
    """
    Actualiza la información del modelo.

    Args:
        request (ModelUpdateRequest): Solicitud de actualización del modelo.

    Returns:
        dict: Mensaje de confirmación.
    """
    global model_info
    model_info = request.dict()
    return {"message": "Model information updated successfully"}

@app.post("/data")
async def receive_data(request: DataRequest):
    """
    Recibe y procesa los datos.

    Args:
        request (DataRequest): Solicitud de datos con los valores y configuración.

    Returns:
        dict: Mensaje de confirmación.
    """
    global data
    if request.reset:
        data = {"angulo": [], "par": [], "prediction": "", "reset": True, "identificador": request.identificador}
    data["angulo"].extend(request.angulo)
    data["par"].extend(request.par)
    data["reset"] = request.reset
    data["identificador"] = request.identificador  # Actualizar identificador

    json_data = {
        "model_folder": model_info["model_folder"],
        "model_name": model_info["model_name"],
        "window_size": model_info["window_size"],
        "angulo": request.angulo,
        "par": request.par
    }

    try:
        response = requests.post("http://localhost:8000/predict", json=json_data)
        if response.status_code == 200:
            data["prediction"] = response.json().get("prediction")
            print(f"Predicción recibida: {data['prediction']}")
        else:
            data["prediction"] = "Error"
            print(f"Error en la predicción: {response.status_code}")
    except requests.exceptions.RequestException as e:
        data["prediction"] = "Error"
        print(f"Error en la solicitud: {str(e)}")

    return {"message": "Data received"}

@app.get("/get_data")
async def get_data():
    """
    Envía los datos almacenados.

    Returns:
        dict: Datos almacenados.
    """
    global data
    return data

@app.get("/health")
async def health_check():
    """
    Verifica el estado del servidor.

    Returns:
        dict: Estado del servidor.
    """
    return {"status": "OK"}

def start_service():
    """
    Inicia el servidor de FastAPI.
    """
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
