import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.ndimage import gaussian_filter1d
import pandas as pd

# Definir la ruta base para los resultados
base_path = r"limpio/sif-tiff/analisis/implementing simulation/paper work"

# Crear o verificar la carpeta de resultados
resultados_path = os.path.join(base_path, "resultados")
os.makedirs(os.path.join(resultados_path, "info"), exist_ok=True)
os.makedirs(os.path.join(resultados_path, "top plots"), exist_ok=True)

# Archivos para guardar ganancias, anchuras y pendientes
ganancias_file = os.path.join(resultados_path, "info", "top ganancias.txt")
width_file = os.path.join(resultados_path, "info", "top width.txt")
slope_file = os.path.join(resultados_path, "info", "top slope.txt")
x2_file = os.path.join(resultados_path, "info", "top x2.txt")

# Crear los archivos de texto y escribir encabezados si no existen
def ensure_file(file, header):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write(header)

ensure_file(ganancias_file, "Archivo\tGanancia Óptica\n")
ensure_file(width_file, "Archivo\tAnchura del Ajuste\n")
ensure_file(slope_file, "Archivo\tPendiente del Ajuste\n")
ensure_file(x2_file, "Archivo\tChi Cuadrado\n")

# Función para procesar cada archivo CSV
def procesar_archivo(filepath):
    data = pd.read_csv(filepath)
    max_x = data['X'].max()
    max_y = data['Y'].max()
    array_2d = np.zeros((max_x + 1, max_y + 1))

    for _, row in data.iterrows():
        x_rect = row['X']
        y_rect = row['Y']
        value_rect = row['Value']
        array_2d[int(x_rect), int(y_rect)] = value_rect

    data = np.sum(array_2d, axis=1)
    plot_x = np.linspace(0, 200, len(data))

    start, end = 0, len(data)
    for i in range(len(data)):
        if data[i] > np.max(data) / 4:
            start = i
            break
    for i in range(np.argmax(data), len(data) - 2):
        if data[i] < np.max(data) / 4:
            end = i
            break

    y_signal = np.sum(array_2d, axis=1)[start:end]
    intervals = np.array_split(y_signal, 10)
    points_y = [np.mean(interval) for interval in intervals[:10]]
    points_x = [np.round(len(y_signal) / 10) * j + start for j in range(10)]

    if np.max(data) < 1000000:
        points_x.pop(0)
        points_y.pop(0)
        slope, intercept, *_ = linregress([x + start for x in points_x], points_y)
        pred_y = [slope * (x + start) + intercept for x in points_x]
        dev = np.array(points_y) - np.array(pred_y)
        thr = -(1) * np.mean(np.abs(dev))  # Distancia media
        indices_to_keep = dev >= thr
        points_x = np.array(points_x)[indices_to_keep].tolist()
        points_y = np.array(points_y)[indices_to_keep].tolist()
        slope, intercept, *_ = linregress([x + start for x in points_x], points_y)
    else:
        slope, intercept, *_ = linregress([x + start for x in points_x], points_y)

    def fit(offset, d, sigma, x):
        y = np.zeros(len(x))
        for i in range(len(x)):
            if offset <= x[i] < d:
                y[i] = slope * (x[i] + offset) + intercept
        return gaussian_filter1d(y, sigma=sigma)

    s = fit(start, end, 1, plot_x)
    r = data - s
    P_s = np.sum(s[start:end]**2)
    P_r = np.sum(r[start:end]**2)
    SNR = P_s / P_r

    n_ph_av_bot = 3305
    n_ph = np.sum(data) - n_ph_av_bot
    W_i = 26.7
    GE = 5.09 * 10**-4
    QE = 0.95
    Ea = 5.5 * 10**6
    fa = 200
    t_exp = 5 * 10**-3
    opt_g = (n_ph * W_i) / (GE * QE * Ea * fa * t_exp)

    # Chi2 normalizado
    mask = s[start:end] > 0  # Considerar solo valores positivos
    dof = len(data[start:end][mask]) - 2
    chi2 = (1/dof) * np.sum((data[start:end][mask] - s[start:end][mask])**2 / np.sqrt(s[start:end][mask]))

    with open(ganancias_file, "a") as gf, open(width_file, "a") as wf, open(slope_file, "a") as sf, open(x2_file, "a") as xf:
        gf.write(f"{os.path.basename(filepath)}\t{opt_g:.2f}\n")
        wf.write(f"{os.path.basename(filepath)}\t{end - start}\n")
        sf.write(f"{os.path.basename(filepath)}\t{slope:.4f}\n")
        xf.write(f"{os.path.basename(filepath)}\t{chi2:.4f}\n")


    plt.figure()
    plt.plot(plot_x, s, label='Fitting function')
    plt.plot(data, label='Datos experimentales')
    plt.legend()
    plt.title(f"Ajuste de datos: {os.path.basename(filepath)}")

    plot_folder = os.path.join(resultados_path, "top plots")
    plt.savefig(os.path.join(plot_folder, f"{os.path.basename(filepath).replace('.csv', '.png')}"))
    plt.close()

# Iterar sobre las carpetas y procesar archivos
carpeta_base = "limpio/sif-tiff/analisis/implementing simulation/paper work/alpha tracks/top THGEM"

for root, dirs, files in os.walk(carpeta_base):
    if "bckg" in root:
        continue
    for file in files:
        if file.endswith(".csv"):
            filepath = os.path.join(root, file)
            try:
                procesar_archivo(filepath)
            except Exception as e:
                print(f"Error al procesar {file}: {e}. Omitiendo archivo.")

# Guardar resultados en CSV
df_resultados = pd.DataFrame({"Archivo": os.listdir(carpeta_base)})
df_resultados.to_csv(os.path.join(resultados_path, "resultados_completos.csv"), index=False)