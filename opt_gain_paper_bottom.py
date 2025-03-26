
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.ndimage import gaussian_filter1d
import pandas as pd

# Definir la ruta base para los resultados
base_path = r"limpio/sif-tiff/analisis/implementing simulation/paper work"

# Eliminar carpetas de resultados si existen
resultados_path = os.path.join(base_path, "resultados")
if os.path.exists(resultados_path):
    shutil.rmtree(resultados_path)

# Crear las carpetas de resultados
os.makedirs(os.path.join(resultados_path, "info"), exist_ok=True)
os.makedirs(os.path.join(resultados_path, "bottom plots"), exist_ok=True)
os.makedirs(os.path.join(resultados_path, "bottom plots", "irregular"), exist_ok=True)

# Archivos para guardar ganancias, anchuras y pendientes
ganancias_file = os.path.join(resultados_path, "info", "bottom ganancias.txt")
width_file = os.path.join(resultados_path, "info", "bottom width.txt")
slope_file = os.path.join(resultados_path, "info", "bottom slope.txt")
x2_file = os.path.join(resultados_path, "info", "bottom x2.txt")
ix2_file = os.path.join(resultados_path, "info", "bottom x2 irregular.txt")
r2_file = os.path.join(resultados_path, "info", "bottom R2.txt")
ir2_file = os.path.join(resultados_path, "info", "bottom R2 irregular.txt")
snr_file = os.path.join(resultados_path, "info", "bottom SNR.txt")
isnr_file = os.path.join(resultados_path, "info", "bottom SNR irregular.txt")
phw_file = os.path.join(resultados_path, "info", "bottom integral diff.txt")
iphw_file = os.path.join(resultados_path, "info", "bottom integral diff irregular.txt")

# Crear los archivos de texto y escribir encabezados
with open(ganancias_file, "w") as gf, open(isnr_file, "w") as isnrf, open(iphw_file, "w") as iphwf, open(phw_file, "w") as phwf, open(snr_file, "w") as snrf, open(width_file, "w") as wf, open(ir2_file, "w") as irf, open(r2_file, "w") as rf, open(slope_file, "w") as sf, open(x2_file, "w") as xf, open(ix2_file, "w") as ixf:
    gf.write("Archivo\tGanancia Óptica\n")
    wf.write("Archivo\tAnchura del Ajuste\n")
    sf.write("Archivo\tPendiente del Ajuste\n")
    xf.write("Archivo\tChi Cuadrado\n")
    ixf.write("Archivo\tChi Cuadrado Irregular\n")
    rf.write("Archivo\tR Cuadrado\n")
    irf.write("Archivo\tR Cuadrado Irregular\n")
    snrf.write("Archivo\tSignal to Noise Relation\n")
    isnrf.write("Archivo\t Irregular Signal to Noise Relation\n")
    phwf.write("Archivo\tDiferencia Integral\n")
    iphwf.write("Archivo\t Irregular Diferencia Integral\n")

# Lista de archivos específicos que deben ser considerados irregulares
archivos_irregulares = [
    "1p5Bot_5msexp_17 Plot Data.csv", "1p5Bot_5msexp_30 Plot Data.csv", "1p5Bot_5msexp_62 Plot Data.csv",
    "1p5Bot_5msexp_72 Plot Data.csv", "1p5Bot_5msexp_76 Plot Data.csv", "1p5Bot_5msexp_94 Plot Data.csv",
    "1p5Bot_5msexp_99 Plot Data.csv", "1p6Bot_5msexp_38 Plot Data.csv", "1p6Bot_5msexp_49 Plot Data.csv",
    "1p6Bot_5msexp_66 Plot Data.csv"
]

# Función para procesar cada archivo CSV
def procesar_archivo(filepath):
    # Leer los datos
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
    plot_x = np.linspace(0, len(data), len(data))

    # Identificar inicio y final de la señal
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
        y = [0] * len(x)
        for i in range(len(x)):
            if offset <= x[i] < d:
                y[i] = slope * (x[i] + offset) + intercept
            else:
                y[i] = 0
        return gaussian_filter1d(y, sigma=sigma)

    # Señal ajustada
    s = fit(start, end, 1, plot_x)
    r = data - s

    # Asignar la carpeta para guardar los datos de ajuste
    fit_data_folder = os.path.join(resultados_path, "fit_data")
    os.makedirs(fit_data_folder, exist_ok=True)

    # Guardar los datos (x, y) de la función fit
    fit_data_file = os.path.join(fit_data_folder, f"{os.path.basename(filepath).replace('.csv', '_fit_data.csv')}")
    fit_data = pd.DataFrame({'X': plot_x, 'Y': s})
    fit_data.to_csv(fit_data_file, index=False)


    # Relación señal-ruido
    P_s = np.sum(s[start:end]**2)
    P_r = np.sum(r[start:end]**2)
    SNR = P_s / P_r

    # Cálculo de ganancia óptica
    n_ph = np.sum(data)
    W_i = 26.7
    GE = 5.09 * 10**-4
    QE = 0.95
    Ea = 5.5 * 10**6
    fa = 200
    t_exp = 5 * 10**-3
    opt_g = (n_ph * W_i) / (GE * QE * Ea * fa * t_exp)


    # R^2 
    ss_res = np.sum((data[start:end] - s[start:end]) ** 2)
    ss_tot = np.sum((data[start:end] - np.mean(data[start:end])) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    mask = s[start:end] > 0  # Considerar solo valores positivos

    # Diferencia integral

    I1 = np.sum(data[start:end][mask])
    I2 = np.sum(s[start:end][mask])
    
    DI = np.abs(I2 - I1) / ((I1 + I2) / 2)

    # Chi2 normalizado
    dof = len(data[start:end][mask]) - 2
    phw2 = np.sum(s[start:end][mask]) / (len(s[start:end][mask]))
    chi2 = (1/dof) * np.sum((data[start:end][mask] - s[start:end][mask])**2 / phw2)

    # Determinar si es "irregular"
    base_filename = os.path.basename(filepath)

    # Considerar como irregular si el archivo está en la lista o si el slope es positivo
    is_irregular = (base_filename in archivos_irregulares) or (slope > 0)

    # Si es irregular, no agregar al archivo de ganancias
    if not is_irregular:
        with open(ganancias_file, "a") as gf, open(phw_file, "a") as phwf, open(snr_file, "a") as snrf, open(r2_file, "a") as rf, open(width_file, "a") as wf, open(slope_file, "a") as sf, open(x2_file, "a") as xf:
            gf.write(f"{os.path.basename(filepath)}\t{opt_g:.2f}\n")
            wf.write(f"{os.path.basename(filepath)}\t{end - start}\n")
            sf.write(f"{os.path.basename(filepath)}\t{slope:.4f}\n")
            xf.write(f"{os.path.basename(filepath)}\t{chi2:.4f}\n")
            rf.write(f"{os.path.basename(filepath)}\t{r2:.4f}\n")
            snrf.write(f"{os.path.basename(filepath)}\t{SNR:.4f}\n")
            phwf.write(f"{os.path.basename(filepath)}\t{DI:.4f}\n")
            
    # Crear y guardar el plot en la carpeta correspondiente
    plt.figure()
    plt.plot(plot_x, s, label='Fitting function')
    plt.plot(data, label='Datos experimentales')
    plt.legend()
    plt.title(f"Ajuste de datos: {os.path.basename(filepath)}")

    # Asignar la carpeta para guardar el gráfico dependiendo de si es irregular
    if is_irregular:
        with open(ix2_file, "a") as ixf, open(ir2_file, "a") as irf, open(iphw_file, "a") as iphwf, open(isnr_file, "a") as isnrf:
            ixf.write(f"{os.path.basename(filepath)}\t{chi2:.4f}\n")
            irf.write(f"{os.path.basename(filepath)}\t{r2:.4f}\n")
            iphwf.write(f"{os.path.basename(filepath)}\t{DI:.4f}\n")
        plot_folder = os.path.join(resultados_path, "bottom plots", "irregular")
    else:
        plot_folder = os.path.join(resultados_path, "bottom plots")

    # Asegurarse de que la carpeta exista
    os.makedirs(plot_folder, exist_ok=True)

    # Guardar el gráfico
    plt.savefig(os.path.join(plot_folder, f"{os.path.basename(filepath).replace('.csv', '.png')}"))
    plt.close()

    return {
        "Archivo": os.path.basename(filepath),
        "Coeficiente de correlación lineal": slope**2,
        "Señal a ruido (SNR)": SNR,
        "Ganancia óptica": opt_g,
        "Anchura de la señal (en píxels)": end - start,
        "Amplitud de pico de la señal (fit)": np.max(s),
        "Amplitud de pico de la señal (data)": np.max(data),
        "Coeficiente Chi^2": chi2,
        "Diferencia Integral": DI,
        "Irregular": is_irregular
    }

# Iterar sobre las carpetas y procesar archivos
resultados = []
carpeta_base = "limpio/sif-tiff/analisis/implementing simulation/paper work/alpha tracks/bottom THGEM"

for root, dirs, files in os.walk(carpeta_base):
    if "bckg" in root:
        continue
    for file in files:
        if file.endswith(".csv"):
            filepath = os.path.join(root, file)
            try:
                # Intentar procesar cada archivo CSV
                resultados.append(procesar_archivo(filepath))
            except Exception as e:
                # Si ocurre un error, imprimir el mensaje y continuar con el siguiente archivo
                print(f"Error al procesar {file}: {e}. Omitiendo archivo.")


# Guardar los resultados en un CSV
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(os.path.join(resultados_path, "resultados_completos.csv"), index=False)
