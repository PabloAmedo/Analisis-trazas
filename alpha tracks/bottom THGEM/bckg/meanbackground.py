import numpy as np
import os
from PIL import Image

# Ruta de la carpeta que contiene los archivos TIFF
path = "projects/helloworld/igfae/limpio/sif-tiff/analisis/implementing simulation/background"

# Ruta de destino donde guardarás la imagen final
output_path = "projects/helloworld/igfae/limpio/sif-tiff/analisis/implementing simulation/background"

# Asegúrate de que la carpeta de salida existe
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Obtener lista de archivos TIFF
tiff = [f for f in os.listdir(path) if f.endswith('.tiff')]

# Inicializar la variable para la suma de las imágenes
sum_image = None

# Inicializar la variable de dimensiones
image_shape = None

# Sumar las imágenes
for archivo in tiff:
    ruta_completa = os.path.join(path, archivo)
    
    with Image.open(ruta_completa) as img:
        img_array = np.array(img, dtype=np.float64)
        
        # Comprobar las dimensiones de cada imagen
        if image_shape is None:
            image_shape = img_array.shape
        elif img_array.shape != image_shape:
            print(f"Error: La imagen {archivo} tiene dimensiones diferentes: {img_array.shape}")
            continue  # Ignorar imágenes con dimensiones diferentes
        
        # Inicializar la suma si es la primera imagen
        if sum_image is None:
            sum_image = img_array
        else:
            sum_image += img_array

# Asegurarse de que la suma no es nula
if sum_image is not None:
    # Calcular el promedio de la suma (si es necesario)
    mean_sum = sum_image / len(tiff)

    # Guardar la imagen en formato float32 sin reescalar
    final_image = mean_sum.astype(np.float32)

    # Convertir el array final a una imagen
    imagen_suma = Image.fromarray(final_image)

    # Guardar la imagen en la carpeta especificada
    output_file = os.path.join(output_path, "mean_backg.tiff")
    imagen_suma.save(output_file, format="TIFF")

    # Mostrar un mensaje de éxito
    print(f"Imagen guardada exitosamente en {output_file}")
else:
    print("No se procesaron imágenes correctamente.")
