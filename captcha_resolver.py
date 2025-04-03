import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import Counter
from io import BytesIO
from PIL import Image

# Carregar el model entrenat
model_path = os.path.join(os.path.dirname(__file__), 'digit_ocr_model.keras')
model = load_model(model_path)

# Funció per a processar i segmentar la imatge del CAPTCHA
def process_captcha(captcha_image_bytes):
    # Convertir els bytes de la imatge en una imatge de OpenCV
    img = Image.open(BytesIO(captcha_image_bytes))
    img = np.array(img.convert('L'))  # Convertim a escala de grisos (L)

    # Eliminar el marc de 3 píxels (redueix la mida de la imatge)
    img = img[3:-3, 3:-3]
    
    # Obtenir les dimensions de la imatge
    h, w = img.shape
    
    # Segmentació basada en el vector digit_widths
    digits = []
    start_x = 0
    # Vector amb les amplades dels dígits
    digit_widths = [17, 17, 18, 18, 17, 18, 17, 20, 18]
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
            prediction = model.predict(digit_img, verbose=0)
            
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

# Funció per capturar el CAPTCHA directament des de Selenium i passar-lo al model
def capture_and_process_captcha(driver):
    # Captura la imatge del CAPTCHA com a bytes
    captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'antispam.php')]")
    captcha_image_bytes = captcha_img.screenshot_as_png  # Capturem la imatge en memòria (en format PNG)

    # Passar la imatge capturada a la funció per resoldre el CAPTCHA
    return process_captcha(captcha_image_bytes)

if __name__ == '__main__':
    correct = []
    incorrect = {}
    # Configurar Selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Accedir a la pàgina del curs
    captcha_directory = os.path.join(os.path.dirname(__file__), '..', 'captcha_images')  # Directori de CAPTCHA
    for filename in os.listdir(captcha_directory):
        if filename.endswith('.png'):
            # Obtenim la ruta del CAPTCHA
            captcha_path = os.path.join(captcha_directory, filename)
            
            # Capturar i processar el CAPTCHA utilitzant Selenium i el model
            captcha_text = capture_and_process_captcha(driver)
            
            if captcha_text == filename[:-4]:  # Comparar amb el nom del fitxer per verificar
                print(f"CAPTCHA {filename}: {captcha_text} (CORRECTE)")
                correct.append(captcha_text)
            else:
                print(f"CAPTCHA {filename}: {captcha_text} (INCORRECTE)")
                incorrect[filename] = captcha_text

    print(f"Resultats:")
    print(f"\tCorrectes: {correct}")
    print(f"\tIncorrectes: {incorrect}")

    # Tancar el navegador després de la prova
    driver.quit()
