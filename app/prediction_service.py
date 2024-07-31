from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
import requests

app = FastAPI()

class DataRequest(BaseModel):
    """Modelo para los datos recibidos en el endpoint de datos.

    Attributes:
        angulo (list): Lista de valores de ángulo.
        par (list): Lista de valores de par.
        reset (bool): Indicador de reinicio del proceso.
        identificador (str): Identificador del proceso.
        fecha (str): Fecha asociada al proceso.
    """
    angulo: list
    par: list
    reset: bool
    identificador: str
    fecha: str  # Nuevo campo para la fecha

class ModelUpdateRequest(BaseModel):
    """Modelo para la solicitud de actualización de modelo.

    Attributes:
        model_folder (str): Carpeta donde se almacena el modelo.
        model_name (str): Nombre del modelo.
        window_size (int): Tamaño de la ventana utilizada por el modelo.
    """
    model_config = ConfigDict(protected_namespaces=())
    model_folder: str
    model_name: str
    window_size: int

data = {"angulo": [], "par": [], "prediction": "", "reset": False, "identificador": "", "fecha": ""}
model_info = {"model_folder": "", "model_name": "", "window_size": 0}

@app.post("/update_model")
async def update_model(request: ModelUpdateRequest):
    """Actualiza la información del modelo con los datos proporcionados.

    Args:
        request (ModelUpdateRequest): Datos de la solicitud de actualización del modelo.

    Returns:
        dict: Mensaje de confirmación de actualización.
    """
    global model_info
    model_info = request.dict()
    return {"message": "Model information updated successfully"}

@app.post("/data")
async def receive_data(request: DataRequest):
    """Recibe datos de ángulo y par, los procesa y solicita una predicción.

    Args:
        request (DataRequest): Datos de ángulo, par y otros detalles del proceso.

    Returns:
        dict: Mensaje de confirmación de recepción de datos.
    """
    global data
    if request.reset:
        data = {"angulo": [], "par": [], "prediction": "", "reset": True, "identificador": request.identificador, "fecha": request.fecha}
    data["angulo"].extend(request.angulo)
    data["par"].extend(request.par)
    data["reset"] = request.reset
    data["identificador"] = request.identificador
    data["fecha"] = request.fecha  # Actualizar fecha

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
    """Devuelve los datos actuales almacenados en el servidor.

    Returns:
        dict: Datos actuales de ángulo, par, predicción, identificador y fecha.
    """
    global data
    return data

@app.get("/health")
async def health_check():
    """Verifica el estado de salud del servidor.

    Returns:
        dict: Mensaje de estado de salud.
    """
    return {"status": "ok"}


def start_service():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)