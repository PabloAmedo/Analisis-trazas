import pandas as pd
import matplotlib.pyplot as plt
import os

# Definir la ruta del archivo de resultados
resultados_path = r"limpio/sif-tiff/analisis/implementing simulation/paper work/resultados/resultados_completos.csv"

# Verificar si el archivo existe antes de leerlo
if not os.path.exists(resultados_path):
    raise FileNotFoundError(f"El archivo no se encontró: {resultados_path}")

# Leer los datos del archivo CSV con manejo de errores
try:
    df_resultados = pd.read_csv(resultados_path, encoding='utf-8')  # Ajusta encoding si es necesario
except Exception as e:
    raise RuntimeError(f"Error al leer el archivo CSV: {e}")

# Filtrar columnas relevantes
columnas_relevantes = ['Archivo', 'Coeficiente Chi^2', 'Diferencia Integral', 'Irregular']
if not all(col in df_resultados.columns for col in columnas_relevantes):
    raise ValueError("El archivo CSV no contiene todas las columnas necesarias.")

df_plot = df_resultados[columnas_relevantes]

# Definir el umbral de Chi² y Diferencia Integral
chi2_corte = 100  # Puedes cambiar este valor según lo necesites
dif_integral_corte = 0.5  # Cambia este valor según tus necesidades

# Filtrar puntos regulares e irregulares
df_regulares = df_plot[df_plot['Irregular'] == False]
df_irregulares = df_plot[df_plot['Irregular'] == True]

# Estilo del gráfico
plt.style.use('seaborn-v0_8-muted')

# Gráfico 1: Todos los puntos
plt.figure(figsize=(10, 6))
plt.scatter(df_regulares['Coeficiente Chi^2'], df_regulares['Diferencia Integral'], color='blue', s=12, alpha=0.6, label='Regulares')
plt.scatter(df_irregulares['Coeficiente Chi^2'], df_irregulares['Diferencia Integral'], color='orange', s=12, alpha=0.6, label='Irregulares')
plt.title('Comparación de Chi² con Diferencia Integral')
plt.xlabel('Coeficiente Chi²')
plt.ylabel('Diferencia Integral')
plt.grid(True, linestyle='--', alpha=0.5)
plt.axhline(dif_integral_corte, color='red', linestyle='--', linewidth=1.5, label=f'DI = {dif_integral_corte}')
plt.axvline(chi2_corte, color='red', linestyle='--', linewidth=1.5, label=f'Chi² = {chi2_corte}')
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.savefig('chi2_vs_DI.png', dpi=300, bbox_inches='tight')
plt.show()

# Contar el total de eventos antes del corte
total_eventos = len(df_plot)

# Filtrar los datos después del corte
df_filtrado = df_regulares[
    (df_regulares['Coeficiente Chi^2'] < chi2_corte) & 
    (df_regulares['Diferencia Integral'] < dif_integral_corte)
]

eventos_filtrados = len(df_filtrado)
porcentaje_eventos_quedan = (eventos_filtrados / total_eventos) * 100

# Mostrar el resultado
print(f"Total de eventos antes del corte: {total_eventos}")
print(f"Total de eventos después del corte: {eventos_filtrados}")
print(f"Porcentaje de eventos que quedan después del corte: {porcentaje_eventos_quedan:.2f}%")

# Filtrar archivos fuera del corte
df_fuera_corte = df_plot[
    (df_plot['Coeficiente Chi^2'] <= 0.5* chi2_corte) & 
    (df_plot['Diferencia Integral'] <= 0.5)
]

# Obtener nombres de archivos fuera del corte
archivos_fuera_corte = df_fuera_corte['Archivo'].tolist()

print("\nArchivos que quedan fuera de los cortes:")
for archivo in archivos_fuera_corte:
    print(archivo)
