import matplotlib.pyplot as plt
import numpy as np

# Ruta del archivo de texto
archivo_path = "limpio/sif-tiff/analisis/implementing simulation/paper work/resultados/info/bottom width.txt"

# Crear un diccionario para almacenar las anchuras individuales por los primeros 3 caracteres del nombre
anchuras_por_voltaje = {}

# Abrir y leer el archivo
with open(archivo_path, 'r') as file:
    # Leer las líneas del archivo
    lineas = file.readlines()

    # Iterar sobre las líneas, saltando la primera (encabezado)
    for linea in lineas[1:]:
        # Separar la línea en columnas usando tabuladores
        columnas = linea.strip().split('\t')
        
        # Verificar si hay al menos 2 columnas (Archivo, Anchura)
        if len(columnas) >= 2:
            try:
                # Convertir el valor de la anchura a flotante
                anchura = float(columnas[1])
                
                # Obtener los primeros 3 caracteres del nombre del archivo
                archivo_nombre = columnas[0]
                primer_codigo = archivo_nombre[:3]  # Los primeros 3 caracteres
                
                # Agregar la anchura al diccionario
                if primer_codigo in anchuras_por_voltaje:
                    anchuras_por_voltaje[primer_codigo].append(anchura)
                else:
                    anchuras_por_voltaje[primer_codigo] = [anchura]
            except ValueError:
                # Si hay un error al convertir a flotante, lo ignoramos
                continue

# Calcular la media y el error estándar de las anchuras para cada voltaje
medias = []
errores = []
nombres = []

for voltaje, anchuras in anchuras_por_voltaje.items():
    media = np.mean(anchuras)
    error_estadistico = np.std(anchuras, ddof=1) / np.sqrt(len(anchuras))  # Error estándar
    medias.append(media)
    errores.append(error_estadistico)
    nombres.append(voltaje)

# Configurar subplots
num_voltajes = len(anchuras_por_voltaje)
cols = 3  # Número de columnas
rows = (num_voltajes + cols - 1) // cols  # Número de filas necesarias

plt.figure(figsize=(15, 5 * rows))

# Generar un histograma para cada voltaje en subplots
for i, (voltaje, anchuras) in enumerate(anchuras_por_voltaje.items()):
    plt.subplot(rows, cols, i + 1)
    plt.hist(anchuras, bins=5, color='skyblue', edgecolor='black', alpha=0.7)  # Ajustado a 5 bins
    media = np.mean(anchuras)  # Media de las anchuras
    plt.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media = {media:.2f}')
    plt.xlabel('Anchura', fontsize=10)
    plt.ylabel('Frecuencia', fontsize=10)
    plt.title(f'Voltage {voltaje}', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

# Mostrar los histogramas
plt.tight_layout()
plt.show()

# Graficar la media con barra de error estadístico
plt.figure(figsize=(8, 6))
plt.errorbar(nombres, medias, yerr=errores, fmt='o-', color='skyblue', ecolor='black', capsize=5)
plt.xlabel('Voltage', fontsize=12)
plt.ylabel('Media de Anchura', fontsize=12)
plt.title('Media de Anchura con Barra de Error por Voltage', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()

# Ruta del archivo de texto
archivo_path_top = "limpio/sif-tiff/analisis/implementing simulation/paper work/resultados/info/top width.txt"

# Crear un diccionario para almacenar las anchuras individuales por bloques de 20
anchuras_por_bloque = {}

# Abrir y leer el archivo
with open(archivo_path_top, 'r') as file:
    # Leer las líneas del archivo
    lineas = file.readlines()
    
    # Lista temporal para almacenar las anchuras
    anchuras_temporales = []
    bloque_contador = 1

    # Iterar sobre las líneas, saltando la primera (encabezado)
    for linea in lineas[1:]:
        columnas = linea.strip().split('\t')
        if len(columnas) >= 2:
            try:
                anchura = float(columnas[1])
                anchuras_temporales.append(anchura)

                # Cada 20 entradas, crear un nuevo bloque
                if len(anchuras_temporales) == 20:
                    anchuras_por_bloque[f'1p {bloque_contador+2}'] = anchuras_temporales[:]
                    bloque_contador += 1
                    anchuras_temporales.clear()
            except ValueError:
                continue

# Calcular la media y el error estándar de las anchuras para cada bloque
medias_top = []
errores_top = []
nombres_top = []

for bloque, anchuras in anchuras_por_bloque.items():
    media = np.mean(anchuras)
    error_estadistico = np.std(anchuras, ddof=1) / np.sqrt(len(anchuras))
    medias_top.append(media)
    errores_top.append(error_estadistico)
    nombres_top.append(bloque)

# Configurar subplots
num_bloques = len(anchuras_por_bloque)
cols = 3
rows = (num_bloques + cols - 1) // cols

plt.figure(figsize=(15, 5 * rows))

# Generar histogramas para cada bloque
for i, (bloque, anchuras) in enumerate(anchuras_por_bloque.items()):
    plt.subplot(rows, cols, i + 1)
    plt.hist(anchuras, bins=5, color='orange', edgecolor='black', alpha=0.7)
    media = np.mean(anchuras)
    plt.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media = {media:.2f}')
    plt.xlabel('Anchura', fontsize=10)
    plt.ylabel('Frecuencia', fontsize=10)
    plt.title(f'Voltage {bloque}', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

plt.tight_layout()
plt.show()

# Graficar la media con barra de error estadístico
plt.figure(figsize=(8, 6))
plt.errorbar(nombres_top, medias_top, yerr=errores_top, fmt='o-', color='orange', ecolor='black', capsize=5)
plt.xlabel('Voltage', fontsize=12)
plt.ylabel('Media de Anchura', fontsize=12)
plt.title('Media de Anchura con Barra de Error por Voltage (Top)', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()