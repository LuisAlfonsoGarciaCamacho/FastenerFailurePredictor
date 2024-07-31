"""
Despachador de Datos

Este script procesa un archivo Excel y envía los datos al servicio de datos
para su predicción.

Imports:
    - pandas: Librería para manipulación de datos.
    - requests: Librería para realizar solicitudes HTTP.
    - time: Librería para manejo de tiempo.

Funciones:
    - check_server_status: Verifica el estado del servidor de datos.
    - prepare_data_for_prediction: Prepara los datos para la predicción.
    - process_excel_and_send_data: Procesa el archivo Excel y envía los datos.
"""

import pandas as pd
import requests
import time

def check_server_status():
    """
    Verifica el estado del servidor de datos.

    Returns:
        bool: True si el servidor está activo, False en caso contrario.
    """
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al verificar el estado del servidor: {e}")
        return False

def prepare_data_for_prediction(df, window_size):
    """
    Prepara los datos para la predicción.

    Args:
        df (DataFrame): DataFrame con los datos.
        window_size (int): Tamaño de la ventana de datos.

    Returns:
        list: Lista de ventanas de datos y sus índices.
    """
    X = []
    for i in range(0, df.shape[1], 2):
        if i + 1 >= df.shape[1]:
            break
        angulo = df.iloc[:, i].dropna().astype(float).values
        par = df.iloc[:, i + 1].dropna().astype(float).values
        min_len = min(len(angulo), len(par))
        if min_len > window_size:
            for j in range(0, min_len - window_size + 1, window_size):
                X.append(([angulo[j:j+window_size], par[j:j+window_size]], i))
    return X

def process_excel_and_send_data(file_path, window_size):
    """
    Procesa el archivo Excel y envía los datos al servidor.

    Args:
        file_path (str): Ruta del archivo Excel.
        window_size (int): Tamaño de la ventana de datos.
    """
    print(f"Leyendo archivo Excel: {file_path}")
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1', header=None)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return

    print(f"Dimensiones originales del DataFrame: {df.shape}")

    # Obtener identificadores de la cuarta columna
    identificadores = df.iloc[:, 3].dropna().astype(str).tolist()

    # Eliminar columnas 1, 3 y 4
    df = df.drop(df.columns[[1, 3, 4]], axis=1)
    df = df.dropna(axis=1, how='all').dropna(how='all')
    print(f"Dimensiones del DataFrame después de limpieza: {df.shape}")
    
    df_transposed = df.transpose().reset_index(drop=True)
    
    for col in df_transposed.columns:
        df_transposed[col] = pd.to_numeric(df_transposed[col], errors='coerce')
    df_transposed = df_transposed.dropna(how='all')
    print(f"Dimensiones del DataFrame transpuesto: {df_transposed.shape}")

    X = prepare_data_for_prediction(df_transposed, window_size)
    print(f"Número de ventanas preparadas: {len(X)}")
    if len(X) == 0:
        print("No hay suficientes datos para procesar este archivo.")
        return

    if not check_server_status():
        print("El servidor no está respondiendo. Por favor, verifica que esté en ejecución.")
        return

    current_process = -1
    samples_sent = 0

    for index, (window, process_index) in enumerate(X):
        if process_index != current_process:
            current_process = process_index
            reset = True
            print(f"Preparando datos del atornillado {current_process // 2 + 1}")
        else:
            reset = False

        angulo, par = window

        # Usar el identificador correspondiente para cada fila del dataset original
        identificador = identificadores[process_index // 2]

        json_data = {
            "angulo": angulo.tolist(),
            "par": par.tolist(),
            "reset": reset,
            "identificador": identificador
        }

        print(f"Enviando datos: reset={reset}, longitud angulo={len(angulo)}, longitud par={len(par)}, identificador={json_data['identificador']}")
        try:
            start_time = time.time()
            response = requests.post("http://localhost:8001/data", json=json_data, timeout=60)
            end_time = time.time()
            print(f"Tiempo de respuesta del servidor: {end_time - start_time:.2f} segundos")
            response.raise_for_status()
            print(f"Respuesta del servidor: {response.text}")
            samples_sent += 1
        except requests.exceptions.Timeout:
            print("Tiempo de espera agotado al enviar datos al servidor.")
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar datos: {e}")
            print(f"Contenido de la respuesta: {e.response.text if e.response else 'No hay respuesta'}")
        
        time.sleep(1)  # Aumentamos la pausa entre envíos a 1 segundo

    print(f"Proceso completado. Se enviaron {samples_sent} muestras.")

if __name__ == "__main__":
    window_size = 500  # Este valor debe coincidir con el tamaño de ventana del modelo seleccionado en Streamlit
    excel_file_path = r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\src\new_data\4146_PF4_A218izq_T12\Prueba_new.xlsx'
    
    print("Iniciando proceso de envío de datos...")
    process_excel_and_send_data(excel_file_path, window_size)
    print("Proceso finalizado.")
