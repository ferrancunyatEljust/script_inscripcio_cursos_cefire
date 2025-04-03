import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical
import os


# Funció per a binaritzar la imatge
def preprocess_image(img_path, threshold=128, erode_dilate=True, kernel_size=(3, 3),resize=(28, 28)):
    # Carreguem la imatge en escala de grisos
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Aplica thresholding (binarització)
    _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # Aplica erosió i dilatació per millorar la qualitat de la imatge
    if erode_dilate:
        kernel = np.ones(kernel_size, np.uint8)
        processed_img = cv2.erode(binary_img, kernel, iterations=1)
        processed_img = cv2.dilate(processed_img, kernel, iterations=1)
    else:
        processed_img = binary_img

    # Redimensionem la imatge a 28x28
    processed_img = cv2.resize(processed_img, resize)

    return processed_img

# Càrrega de les imatges i etiquetes
def load_data_from_directory(directory, threshold=80, erode_dilate=True, kernel_size=(3, 3), resize=(64, 64)):
    X = []
    y = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            # Extraïm l'etiqueta del nom del fitxer (primer caràcter)
            label = int(filename[0]) - 1  # Subtraiem 1 per obtenir un índex de 0 a 8 (9 classes)
            
            # Preprocessat de la imatge
            img_path = os.path.join(directory, filename)
            img = preprocess_image(img_path, threshold, erode_dilate, kernel_size, resize)
            
            # Afegim la imatge i la seva etiqueta a les llistes
            X.append(img)
            y.append(label)
    
    # Convertim les llistes a arrays de numpy
    X = np.array(X).reshape(-1, image_size[0], image_size[1], 1)  # Redimensionem per a Keras
    y = to_categorical(y, num_classes=9)  # Converteix les etiquetes a one-hot (per a 9 classes)
    
    return X, y