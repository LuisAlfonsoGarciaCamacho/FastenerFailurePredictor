# despachador_datos module

Despachador de Datos

Este script procesa un archivo Excel y envía los datos al servicio de datos
para su predicción.

Imports:
: - pandas: Librería para manipulación de datos.

- requests: Librería para realizar solicitudes HTTP.
- time: Librería para manejo de tiempo.

Funciones:
: - check_server_status: Verifica el estado del servidor de datos.

- prepare_data_for_prediction: Prepara los datos para la predicción.
- process_excel_and_send_data: Procesa el archivo Excel y envía los datos.

### test_model.check_server_status()

Verifica el estado del servidor de datos.

Returns:
: bool: True si el servidor está activo, False en caso contrario.

### test_model.prepare_data_for_prediction(df, window_size)

Prepara los datos para la predicción.

Args:
: df (DataFrame): DataFrame con los datos.
  window_size (int): Tamaño de la ventana de datos.

Returns:
: list: Lista de ventanas de datos y sus índices.

### test_model.process_excel_and_send_data(file_path, window_size)

Procesa el archivo Excel y envía los datos al servidor.

Args:
: file_path (str): Ruta del archivo Excel.
  window_size (int): Tamaño de la ventana de datos.
