import os
import time

from selenium_test import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

num_captches = 20 # Número 

# Inicialitzar Selenium (necessites tenir el ChromeDriver instal·lat)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Opcional, per executar sense obrir el navegador
driver = webdriver.Chrome(options=options)

try:
    # Anar a la pàgina dels cursos
    url = "https://cefire.edu.gva.es/sfp/index.php?seccion=ediciones&filtro_titulo=&filtro_ambito=009&filtro_familia=32&filtro_nivel=&filtro_estado=inscripcion"
    driver.get(url)
    
    # Esperar que carregui la pàgina
    # time.sleep(3)  # Millor substituir per WebDriverWait si la pàgina tarda més
    
    # Esperar fins que carreguin els enllaços dels cursos
    cursos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td a.titulo"))
    )
    
    # Trobar tots els enllaços dels cursos
    cursos = driver.find_elements(By.CSS_SELECTOR, "td a.titulo")

    if cursos:
        # Seleccionar un curs aleatori (o el primer, per exemple)
        curs = cursos[0]
        
        # Obtenir l'enllaç del curs
        url_curs = curs.get_attribute("href")

        # Extreure l'ID del curs
        id_curs = url_curs.split("id=")[-1]
        
        print(f"URL del curs: {url_curs}")
        print(f"ID del curs: {id_curs}")

        # Fer clic en el curs per obtindre captches
        curs.click()

        WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(span/text(), 'Inscribirse')]"))  # Exemple per a un CAPTCHA que siga una imatge
            )

        boto_inscripcio = driver.find_element(By.XPATH, "//button[contains(span/text(), 'Inscribirse')]")
        boto_inscripcio.click()

        
        for i in range(num_captches):
            # driver.get(url_curs)
            # Esperar que carregui el captcha
            captcha_img = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'antispam.php')]"))  # Exemple per a un CAPTCHA que siga una imatge
            )
            captcha_src = captcha_img.screenshot_as_png  # Fa una captura de la imatge
            timestamp = time.time_ns()
            captcha_img.screenshot(os.path.join(os.path.dirname(__file__), "captches", f"captcha_{timestamp}.png"))  # Desa el CAPTCHA en un fitxer
            driver.refresh()
except Exception as e:
    print(e.__traceback__)

finally:
    # Tancar el navegador
    driver.quit()
