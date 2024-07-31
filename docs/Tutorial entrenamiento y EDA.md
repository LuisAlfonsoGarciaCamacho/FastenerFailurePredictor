# Tutorial de Uso

#### Requisitos Previos

* **Python** : Asegúrate de tener Python 3.8 o superior instalado en tu sistema.
* **Librerías** : Instala las librerías necesarias ejecutando el siguiente comando en tu terminal:

```
pip install -r requirements.txt
```

#### Archivos y Carpetas

**Carpeta de Datos** :

* Ubicada en `src\data`.
* Contiene subcarpetas con archivos `.xlsx` que serán procesados.

**Carpeta de Modelos** :

* Ubicada en `modelos`.
* Aquí se guardarán los modelos entrenados y los escaladores.

**Carpeta de Salida** :

* Se creará automáticamente como `output`.
* Aquí se guardarán los gráficos generados.

#### Descripción de los Scripts

1. **Script de Entrenamiento de Modelos** (`Entrenamiento_modelos.ipynb`):
   * Procesa archivos `.xlsx` en las subcarpetas de `src\data`.
   * Prepara los datos, entrena modelos con XGBoost y LightGBM, y guarda los modelos y los escaladores.
   * Genera métricas de rendimiento y las guarda en un archivo CSV.
2. **Script de Creación de Gráficos** (`EDA_con_fechas.ipynb`):
   * Procesa archivos `.xlsx` en `src\data` y genera gráficos de dispersión y histogramas.
   * Guarda los gráficos en la carpeta `output`.

#### Modificaciones Necesarias

* **train_models.py** :
* Verificar y ajustar la ruta de la carpeta principal `main_folder_path` si es necesario.
* **create_graphs.py** :
* Verificar y ajustar la ruta de la carpeta base de datos `data_base_dir` si es necesario.

#### Iniciar los Scripts

**Entrenamiento de Modelos** :

* Ejecutar las celdas del notebook.
* El script procesará cada archivo `.xlsx` en las subcarpetas de `src\data`, entrenará los modelos y guardará los resultados en la carpeta `modelos`.

**Creación de Gráficos** :

* Ejecutar las celdas del notebook.
* El script generará gráficos de dispersión y histogramas a partir de los archivos `.xlsx` en `src\data` y guardará los gráficos en la carpeta `output`.
