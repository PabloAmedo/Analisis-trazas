import matplotlib.pyplot as plt
import numpy as np

# Cargar datos del primer archivo
archivo_path_1 = "limpio/sif-tiff/analisis/implementing simulation/paper work/resultados/info/bottom ganancias.txt"
sumas_y_conteos = {}

with open(archivo_path_1, 'r') as file:
    lineas = file.readlines()
    for linea in lineas[1:]:
        columnas = linea.strip().split('\t')
        if len(columnas) >= 2:
            try:
                ganancia = float(columnas[1])
                archivo_nombre = columnas[0]
                primer_codigo = archivo_nombre[:3]
                if primer_codigo in sumas_y_conteos:
                    sumas_y_conteos[primer_codigo]['ganancias'].append(ganancia)
                else:
                    sumas_y_conteos[primer_codigo] = {'ganancias': [ganancia]}
            except ValueError:
                continue

medias_1 = []
errores_1 = []
nombres_1 = []

for clave, datos in sumas_y_conteos.items():
    ganancias = datos['ganancias']
    media = np.mean(ganancias)
    error_estadistico = np.std(ganancias, ddof=1) / np.sqrt(len(ganancias))
    medias_1.append(media)
    errores_1.append(error_estadistico)
    nombres_1.append(clave)

filtro_indices = [i for i, nombre in enumerate(nombres_1) if nombre >= "1p5"]
nombres_filtrados_1 = [nombres_1[i] for i in filtro_indices]
medias_filtradas_1 = [medias_1[i] * (4/3) for i in filtro_indices]
errores_filtrados_1 = [errores_1[i] * (4/3) for i in filtro_indices]

# Cargar datos del segundo archivo
archivo_path_2 = "limpio/sif-tiff/analisis/implementing simulation/paper work/resultados/info/top ganancias.txt"
ganancias_2 = []

with open(archivo_path_2, 'r') as file:
    lineas = file.readlines()
    for linea in lineas[1:]:
        columnas = linea.strip().split('\t')
        if len(columnas) >= 2:
            try:
                ganancias_2.append(float(columnas[1]))
            except ValueError:
                continue

bloques = [ganancias_2[i:i + 20] for i in range(0, len(ganancias_2), 20)]
medias_2 = []
errores_2 = []
nombres_2 = [f'1p {i+3}' for i in range(len(bloques))]

for bloque in bloques:
    if len(bloque) > 0:
        media = np.mean(bloque)
        error_estadistico = np.std(bloque, ddof=1) / np.sqrt(len(bloque))
        medias_2.append(media)
        errores_2.append(error_estadistico)
medias_2_comp = medias_2[2:]
errores_2_comp = errores_2[2:]

optg_cl = [16.17,23.29,62.69,158.93,500.26]
optg_cl = [x * (4/3) for x in optg_cl]
err_cl = [1.98,0.46,1.2,5.97,18.27]
err_cl = [x * (4/3) for x in err_cl]

optg_2 = [31.7,50.1,132.1,322,656]
err_2 = [4.6,1.6,9.1,18,6.6]

# Graficar ambos conjuntos de datos
plt.figure(figsize=(10, 6))
#plt.errorbar(nombres_filtrados_1, optg_cl, yerr=err_cl, fmt='o-', label='Bottom THGEM', capsize=5, ecolor='black', elinewidth=1, markersize=4)
#plt.errorbar(nombres_filtrados_1, optg_2, yerr=err_2, fmt='o-', label='Top THGEM', capsize=5, ecolor='black', elinewidth=1, markersize=4)
plt.errorbar(nombres_filtrados_1, medias_filtradas_1, yerr=errores_filtrados_1, fmt='-o', color='skyblue', ecolor='black', capsize=5, label="Bottom THGEM new")
plt.errorbar(nombres_filtrados_1, medias_2_comp, yerr=errores_2_comp, fmt='-o', color='orange', ecolor='black', capsize=5, label="Top THGEM new")

plt.yscale('log')
plt.xlabel('Voltage', fontsize=12)
plt.ylabel('Ganancia Óptica Media (escala logarítmica)', fontsize=12)
plt.title('Comparación de Ganancia Óptica Media', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()

print(errores_2_comp[4])
print(errores_filtrados_1[4])