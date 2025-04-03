import os
import cv2
from PIL import Image
import numpy as np

# Funció per binaritzar una imatge aplicant un llindar
def binarize_image(image, threshold=0.4, target_size=(28, 28)):
    # Convertir a escala de grisos
    image = image.convert('L')
    
    # Redimensionar la imatge
    image = image.resize(target_size)

    # Convertir la imatge a un array de numpy
    image_array = np.array(image)
    
    # Aplicar el filtre binari de cv2
    _, binary_image = cv2.threshold(image_array, int(threshold * 255), 255, cv2.THRESH_BINARY)
    
    return binary_image

# Funció per aplicar erosió i dilatació
def apply_erosion_dilation(binary_image, kernel_size=3):
    # Crear un nucli per a la morfologia (matriu de 3x3)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    # Aplicar erosió
    eroded_image = cv2.erode(binary_image, kernel, iterations=1)
    
    # Aplicar dilatació
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
    
    return dilated_image

# Funció per crear el directori de destinació si no existeix
def create_output_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Bloc principal per executar el codi
if __name__ == '__main__':
    # Obtenir el camí absolut de la imatge
    folder_path = os.path.join(os.path.dirname(__file__), 'dataset_digit', 'train_images', 'filter')  # Modifica segons sigui necessari
    output_folder = os.path.join(os.path.dirname(__file__), 'dataset_digit', 'train_images', 'processed')  # Ruta de la carpeta de sortida
    
    # Crear la carpeta de sortida si no existeix
    create_output_folder(output_folder)
    
    # Recórrer totes les imatges del directori
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        
        if not image_path.endswith('.png'):
            continue

        # Carregar la imatge
        image = Image.open(image_path)

        for i in range(1, 10):
            # Aplicar la binarització amb un llindar
            binarized_image = binarize_image(image, threshold=i/10)       
            save_path_binarized = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_binarized_{i}.png")
            cv2.imwrite(save_path_binarized, binarized_image)

            # Aplicar erosió i dilatació
            final_image = apply_erosion_dilation(binarized_image, kernel_size=2)        
            save_path_binarized_with_erosion_dilation = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_binarized_{i}_erosion_dilation.png")
            cv2.imwrite(save_path_binarized_with_erosion_dilation, final_image)

            print(f"Imatge processada: {save_path_binarized_with_erosion_dilation}")
