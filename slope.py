import matplotlib.pyplot as plt
import numpy as np

# Ruta del archivo de texto
archivo_path = "limpio/sif-tiff/analisis/implementing simulation/paper work/resultados/info/bottom slope.txt"

# Crear un diccionario para almacenar las sumas, los conteos y las pendientes individuales por los primeros 3 caracteres del nombre
sumas_y_conteos = {}

# Abrir y leer el archivo
with open(archivo_path, 'r') as file:
    # Leer las líneas del archivo
    lineas = file.readlines()

    # Iterar sobre las líneas, saltando la primera (encabezado)
    for linea in lineas[1:]:
        # Separar la línea en columnas usando tabuladores
        columnas = linea.strip().split('\t')
        
        # Verificar si hay al menos 2 columnas (Archivo, Pendiente)
        if len(columnas) >= 2:
            try:
                # Convertir el valor de la pendiente a flotante y tomar el valor absoluto
                pendiente = abs(float(columnas[1]))
                
                # Obtener los primeros 3 caracteres del nombre del archivo
                archivo_nombre = columnas[0]
                primer_codigo = archivo_nombre[:3]  # Los primeros 3 caracteres
                
                # Sumar la pendiente y llevar el conteo de los archivos
                if primer_codigo in sumas_y_conteos:
                    sumas_y_conteos[primer_codigo]['pendientes'].append(pendiente)
                else:
                    sumas_y_conteos[primer_codigo] = {'pendientes': [pendiente]}
            except ValueError:
                # Si hay un error al convertir a flotante, lo ignoramos
                continue

# Calcular la media y el error estándar (desviación típica / sqrt(n)) para cada grupo
medias = []
errores = []
nombres = []

for clave, datos in sumas_y_conteos.items():
    pendientes = datos['pendientes']
    media = np.mean(pendientes)
    error_estadistico = np.std(pendientes, ddof=1) / np.sqrt(len(pendientes))  # Error estándar
    medias.append(media)
    errores.append(error_estadistico)
    nombres.append(clave)

# Graficar las medias con barras de error
plt.figure(figsize=(10, 6))

# Crear el plot (línea con puntos) con las barras de error
plt.errorbar(nombres, medias, yerr=errores, fmt='-o', color='skyblue', ecolor='black', capsize=5, label="Bottom THGEM slope (absolute values)")

# Etiquetas y título del gráfico
plt.xlabel('Voltage', fontsize=12)
plt.ylabel('Pendiente Media (Absoluta)', fontsize=12)
plt.title('Pendiente Media Absoluta por Voltage', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()


# Establecer la escala logarítmica en el eje Y
plt.yscale('log')

# Mostrar la gráfica
plt.legend()
plt.show()



# Ruta del archivo de texto
archivo_path_top = "limpio/sif-tiff/analisis/implementing simulation/paper work/resultados/info/top slope.txt"

# Crear un diccionario para almacenar las sumas, los conteos y las pendientes individuales por bloques de 20
pendientes_por_bloque = {}

# Abrir y leer el archivo
with open(archivo_path_top, 'r') as file:
    lineas = file.readlines()
    pendientes_temporales = []
    bloque_contador = 1

    # Iterar sobre las líneas, saltando la primera (encabezado)
    for linea in lineas[1:]:
        columnas = linea.strip().split('\t')
        if len(columnas) >= 2:
            try:
                pendiente = abs(float(columnas[1]))
                pendientes_temporales.append(pendiente)
                
                # Cada 20 entradas, crear un nuevo bloque
                if len(pendientes_temporales) == 20:
                    pendientes_por_bloque[f'1p {bloque_contador+2}'] = pendientes_temporales[:]
                    bloque_contador += 1
                    pendientes_temporales.clear()
            except ValueError:
                continue

# Calcular la media y el error estándar para cada bloque
medias_top = []
errores_top = []
nombres_top = []

for bloque, pendientes in pendientes_por_bloque.items():
    media = np.mean(pendientes)
    error_estadistico = np.std(pendientes, ddof=1) / np.sqrt(len(pendientes))
    medias_top.append(media)
    errores_top.append(error_estadistico)
    nombres_top.append(bloque)

# Graficar las medias con barras de error
plt.figure(figsize=(10, 6))
plt.errorbar(nombres_top, medias_top, yerr=errores_top, fmt='-o', color='orange', ecolor='black', capsize=5, label="Top THGEM slope (absolute values)")

plt.xlabel('Voltage', fontsize=12)
plt.ylabel('Pendiente Media (Absoluta)', fontsize=12)
plt.title('Pendiente Media Absoluta por Voltage (Top)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.yscale('log')
plt.legend()
plt.show()
