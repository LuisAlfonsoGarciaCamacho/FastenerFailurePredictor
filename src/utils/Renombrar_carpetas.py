import os

# Directorio base
base_dir = r"C:\Users\luisg\OneDrive\Documentos\Proyecto_Fiverr\estaciones"

# Iterar sobre todas las carpetas en el directorio base
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    
    # Verificar si es un directorio
    if os.path.isdir(folder_path):
        # Crear el nuevo nombre de la carpeta reemplazando espacios por _
        new_folder_name = folder_name.replace(" ", "_")
        new_folder_path = os.path.join(base_dir, new_folder_name)
        
        # Renombrar la carpeta
        os.rename(folder_path, new_folder_path)
        print(f"Renamed: {folder_name} -> {new_folder_name}")

print("Renaming completed.")
