import json

def obtener_descriptores(json_file, codigo, año):
    """
    Obtiene los descriptores de un código específico para un año dado desde un archivo JSON con estructura de lista.
    
    Args:
        json_file (str): Ruta al archivo JSON.
        codigo (str): Código a buscar.
        año (int): Año asociado al código.
    
    Returns:
        dict: Los descriptores asociados al código y año.
              Si no se encuentra el código o el año, devuelve None.
    """
    try:
        # Leer el archivo JSON
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Recorrer la lista para buscar el código
        for item in data:
            if codigo in item:  # Verificar si el código está en el diccionario actual
                entry = item[codigo]
                # Verificar que el año coincida
                if entry.get("año") == año:
                    return entry.get("descriptores")
        
        # Si no se encuentra el código o el año
        return None
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {json_file}.")
        return None
    except json.JSONDecodeError:
        print("Error: El archivo no es un JSON válido.")
        return None

# # Ejemplo de uso
# descriptores = obtener_descriptores("Files/Data_serie_A_normalizado_con_identificadores.json", "01010101", 2009)

# if descriptores:
#     print("Descriptores encontrados:")
#     print(json.dumps(descriptores, indent=4, ensure_ascii=False))
# else:
#     print("No se encontraron descriptores para el código y año especificados.")
