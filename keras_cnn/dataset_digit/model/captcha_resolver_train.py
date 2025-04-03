import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import Counter

# Carregar el model entrenat
model_path = os.path.join(os.path.dirname(__file__), 'digit_ocr_model.keras')
model = load_model(model_path)

# Funció per a processar i segmentar la imatge del CAPTCHA
def process_captcha(captcha_path, digit_widths):
    # Carreguem la imatge en escala de grisos
    img = cv2.imread(captcha_path, cv2.IMREAD_GRAYSCALE)
    
    # Eliminar el marc de 3 píxels (redueix la mida de la imatge)
    img = img[3:-3, 3:-3]
    
    # Obtenir les dimensions de la imatge
    h, w = img.shape
    
    # Segmentació basada en el vector digit_widths
    digits = []
    start_x = 0
    possible_widths = set(digit_widths)
    
    for i in range(5):
        predictions = []
        for digit_width in possible_widths:
            # Extreiem cada segment corresponent a un dígit
            digit_img = img[:, start_x:start_x + digit_width]
            
            # Redimensionem cada dígit a 28x28 píxels
            digit_img = cv2.resize(digit_img, (64, 64))
            
            # Normalitzem la imatge a l'interval [0, 1]
            digit_img = digit_img.astype("float32") / 255.0
            
            # Afegim una nova dimensió per que sigui compatible amb el model
            digit_img = np.expand_dims(digit_img, axis=-1)  # Convertir a (28, 28, 1)
            digit_img = np.expand_dims(digit_img, axis=0)  # Convertir a (1, 28, 28, 1)
            
            # Predir el dígit
            prediction = model.predict(digit_img, verbose = 0)
            
            # Obtenir el dígit amb la màxima probabilitat
            predicted_digit = np.argmax(prediction)
            
            # Afegir el dígit a la llista de resultats
            predictions.append(str(predicted_digit + 1))  # Afegim 1 ja que els dígits són de 1 a 9

        # Mirem en les prediccions el dígit més probable
        counter = Counter(predictions)
        most_common = counter.most_common(1)
        element, frequency = most_common[0]
        digits.append(str(element))
            
        # Actualitzar la posició inicial per al següent dígit
        start_x += digit_widths[int(element) - 1]
    
    # Unir els dígits per obtenir el número complet del CAPTCHA
    return ''.join(digits)

if __name__ == '__main__':
    # Vector amb les amplades dels dígits
    digit_widths = [17, 17, 18, 18, 17, 18, 17, 20, 18]

    correct = []
    incorrect = {}
    # Directori amb les imatges dels CAPTCHAs
    captcha_directory = os.path.join(os.path.dirname(__file__), '..', 'captcha_images')
    for filename in os.listdir(captcha_directory):
        if filename.endswith('.png'):
            captcha_path = os.path.join(captcha_directory, filename)
            # Exemple de com utilitzar la funció per resoldre un CAPTCHA
            captcha_text = process_captcha(captcha_path, digit_widths)
            if captcha_text == filename[:-4]:
                print(f"CAPTCHA {filename}: {captcha_text} (CORRECTE)")
                correct.append(captcha_text)
            else:
                print(f"CAPTCHA {filename}: {captcha_text} (INCORRECTE)")
                incorrect[filename] = captcha_text
    
    print(f"Resultats:")
    print(f"\tCorrectes: {correct}")
    print(f"\tIncorrectes: {incorrect}")