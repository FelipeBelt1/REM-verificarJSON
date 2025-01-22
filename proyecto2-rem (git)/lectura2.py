import pandas as pd
import traductor as td
from tqdm import tqdm  # Importar tqdm para la barra de progreso

# Prueba 

def procesar_csv(ruta_csv):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(ruta_csv)

        # Verificar si existen las columnas clave
        columnas_clave = ["Ano", "CodigoPrestacion"]
        for columna in columnas_clave:
            if columna not in df.columns:
                raise KeyError(f"Columna requerida '{columna}' no encontrada en el archivo CSV.")

        # Procesar el archivo con barra de progreso
        resultados = []
        for _, fila in tqdm(df.iterrows(), total=df.shape[0], desc="Procesando CSV"):
            # Filtrar columnas que empiezan con "Col" y tienen valores no vacíos o no nulos
            valores_col = {
                col: fila[col]
                for col in fila.index
                if col.startswith("Col") and fila[col] not in [0, None, '', float('nan')] and not pd.isna(fila[col])
            }

            if valores_col:
                # Convertir el Año a entero
                año = int(fila["Ano"])

                # Manejo de CodigoPrestacion (si es alfanumérico)
                codigo_prestacion = fila["CodigoPrestacion"]
                if isinstance(codigo_prestacion, str) and codigo_prestacion.isdigit():  # Si es un valor numérico en forma de string
                    codigo_prestacion = f"{int(codigo_prestacion):08d}"  # Asegura que tenga ceros a la izquierda
                # Si el código tiene letras (alfanumérico), lo dejamos como está
                elif isinstance(codigo_prestacion, str):
                    # Dejamos el código tal como está, sin cambios
                    codigo_prestacion = codigo_prestacion.strip()  # Eliminar espacios innecesarios si los hay

                resultados.append({
                    "Año": año,
                    "CódigoPrestación": codigo_prestacion,
                    "ValoresCol": valores_col
                })

        return resultados

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_csv}.")
        return []
    except pd.errors.EmptyDataError:
        print("Error: El archivo CSV está vacío.")
        return []
    except KeyError as e:
        print(f"Error: Falta una columna clave en el archivo CSV. {e}")
        return []

# Crear un DataFrame para registrar los errores
errores = pd.DataFrame(columns=["Codigo", "Año"])

# Ruta del archivo CSV
ruta_csv = "Files/data_rem_lebu.csv"

try:
    # Procesar el CSV y obtener los resultados
    resultados_csv = procesar_csv(ruta_csv)

    # Guardar el progreso en un archivo CSV si Ctrl + C se presiona
    for resultado in tqdm(resultados_csv, desc="Procesando resultados", unit="registro"):
        año = resultado["Año"]
        codigo = resultado["CódigoPrestación"]
        
        # Llamar a obtener_descriptores con los datos
        descriptores = td.obtener_descriptores('Files/Data_serie_A_normalizado_con_identificadores.json', codigo, año)
        
        if not descriptores:
            print(f"No se encontraron descriptores para el código {codigo} y año {año}.")
            # Crear un DataFrame temporal para concatenar
            nuevo_error = pd.DataFrame({"Codigo": [codigo], "Año": [año]})
            # Usar concat para agregar el nuevo error al DataFrame de errores
            errores = pd.concat([errores, nuevo_error], ignore_index=True)
            # Guardar los errores en un archivo CSV después de cada iteración
            errores.to_csv("resultados_procesados.csv", index=False)

except KeyboardInterrupt:
    # Capturar Ctrl + C y guardar el progreso en un archivo CSV
    print("\nProceso interrumpido. Guardando resultados hasta el momento...")
    errores.to_csv("resultados_procesados.csv", index=False)
    print("Resultados guardados en 'resultados_procesados.csv'.")
