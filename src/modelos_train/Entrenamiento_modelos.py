import pandas as pd
import numpy as np
import os
import joblib
import gc
from glob import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import lightgbm as lgb
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import VotingClassifier
from collections import Counter

# Carpeta principal que contiene las subcarpetas con archivos .xlsx
main_folder_path = r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\src\data'

# Obtener lista de subcarpetas en la carpeta principal
subfolders = [f.path for f in os.scandir(main_folder_path) if f.is_dir()]

# Lista de tamaños de ventanas
window_sizes = [50, 100, 500]

# Inicializar lista para almacenar métricas
metrics = []

def prepare_data(df, window_size):
    X = []
    y = []
    for i in range(0, df.shape[1], 2):
        if i + 1 >= df.shape[1]:
            break
        angulo = df.iloc[1:, i].dropna().astype(float).values
        par = df.iloc[1:, i+1].dropna().astype(float).values
        label = df.iloc[0, i]
        min_len = min(len(angulo), len(par))
        if min_len > window_size:
            for j in range(0, min_len - window_size + 1, window_size):
                X.append([angulo[j:j + window_size], par[j:j + window_size]])
                y.append(label)
    X = np.array(X).reshape(-1, 2 * window_size)  # Aplanar las ventanas
    return X, np.array(y)

def process_folder(folder_path, window_size):
    # Obtener lista de archivos .xlsx en la carpeta
    file_paths = glob(os.path.join(folder_path, '*.xlsx'))

    # Inicializar listas para almacenar datos combinados
    X_combined = []
    y_combined = []

    for file_path in file_paths:
        # Cargar y preparar los datos
        df = pd.read_excel(file_path, sheet_name='Sheet1', header=None)
        df.columns = [f'Col_{i}' for i in range(len(df.columns))]
        print(f"Procesando archivo: {file_path}")
        print("Forma inicial del DataFrame:", df.shape)
        print("Primeras 5 filas del DataFrame original:")
        print(df.head())
        
        # Eliminar la primera y tercera columna
        df = df.drop(df.columns[[0, 2]], axis=1)

        df = df.dropna(axis=1, how='all').dropna(how='all')

        print("\nForma del DataFrame después de eliminar filas y columnas vacías:", df.shape)

        df_transposed = df.transpose().reset_index(drop=True)
        df_transposed.columns = [f'Col_{i}' for i in range(len(df_transposed.columns))]

        print("\nPrimeras 5 filas del DataFrame transpuesto:")
        print(df_transposed.head())

        # Convertir a numérico y limpiar
        for col in df_transposed.columns:
            df_transposed[col] = pd.to_numeric(df_transposed[col], errors='coerce')
        df_transposed = df_transposed.dropna(how='all')

        print("Valores únicos en la primera fila:", df_transposed.iloc[0].unique())

        # Preparar los datos
        X, y = prepare_data(df_transposed, window_size)

        # Verificar si tenemos datos suficientes
        if len(X) == 0:
            print("No hay suficientes datos para procesar este archivo.")
            continue

        # Agregar datos combinados
        X_combined.append(X)
        y_combined.append(y)

    # Concatenar todos los datos
    if not X_combined or not y_combined:
        print(f"No hay datos suficientes en la carpeta {folder_path}")
        return

    X_combined = np.vstack(X_combined)
    y_combined = np.hstack(y_combined)

    # Convertir etiquetas 2 a 1 para binarizar el problema
    y_combined = np.where(y_combined == 2, 1, y_combined)

    # Dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42)

    # Escalar los datos
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Verificar la cantidad de muestras por clase
    counter = Counter(y_train)
    print(f"Distribución de clases antes de SMOTE: {counter}")

    # Manejo del desbalance de clases con SMOTE
    try:
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
    except ValueError as e:
        print(f"Error con SMOTE en la carpeta {folder_path} con ventana de tamaño {window_size}: {e}")
        return

    # Entrenamiento de XGBoost (CPU)
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        booster='gbtree',
        tree_method='hist',  # Cambiado para usar la CPU
        random_state=42
    )
    xgb_model.fit(X_train_balanced, y_train_balanced)

    # Entrenamiento de LightGBM (CPU)
    lgb_model = lgb.LGBMClassifier(
        n_estimators=200,
        max_depth=20,
        learning_rate=0.1,
        num_leaves=50,
        device='cpu',  # Cambiado para usar la CPU
        random_state=42
    )
    lgb_model.fit(X_train_balanced, y_train_balanced)

    # Crear el modelo de ensamblado
    ensemble_model = VotingClassifier(
        estimators=[('xgb', xgb_model), ('lgb', lgb_model)],
        voting='soft'
    )
    ensemble_model.fit(X_train_balanced, y_train_balanced)

    # Ensemble
    ensemble_probs = ensemble_model.predict_proba(X_test_scaled)[:, 1]

    # Evaluar modelo ensemble
    roc_auc = roc_auc_score(y_test, ensemble_probs)
    print("\nEnsemble Model Performance para ventana de tamaño {}:".format(window_size))
    print(classification_report(y_test, ensemble_model.predict(X_test_scaled)))
    print("ROC AUC:", roc_auc)

    # Guardar métrica
    metrics.append({
        'Modelos': f"{os.path.basename(folder_path)}/ensemble_{window_size}",
        'ROC AUC': roc_auc
    })

    # Obtener la ruta para guardar el modelo ensemble
    model_save_path = os.path.join(r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\modelos', os.path.basename(folder_path))

    # Crear la carpeta si no existe
    os.makedirs(model_save_path, exist_ok=True)

    # Guardar el modelo ensemble y el scaler
    joblib.dump(ensemble_model, os.path.join(model_save_path, f'ensemble_{window_size}.pkl'))
    joblib.dump(scaler, os.path.join(model_save_path, f'scaler_{window_size}.pkl'))

    print(f"\nModelos guardados en: {model_save_path}")

    # Liberar memoria
    del df, df_transposed, X_combined, y_combined, X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, X_train_balanced, y_train_balanced
    del xgb_model, lgb_model, ensemble_model, scaler, ensemble_probs
    gc.collect()

# Procesar cada subcarpeta para cada tamaño de ventana
for subfolder in subfolders:
    for window_size in window_sizes:
        print(f"\nProcesando carpeta: {subfolder} con ventana de tamaño {window_size}")
        process_folder(subfolder, window_size)

# Guardar métricas en un archivo CSV
metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv(r'C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\modelos/roc_auc_metrics.csv', index=False)
print("\nMétricas guardadas en: modelos/roc_auc_metrics.csv")
