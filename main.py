import time
import os
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
from date_parser import parse_data_catala
from io import BytesIO
from PIL import Image
from queue import Queue  # Importem Queue per passar resultats entre fils

# Carregar les variables d'entorn
load_dotenv()
id_curs = os.getenv("ID_CURS")
nif = os.getenv("NIF")
nom = os.getenv("NOM")
cognoms = os.getenv("COGNOMS")
telefon = os.getenv("TELEFON")
email = os.getenv("EMAIL")
centre = os.getenv("CENTRE")
localitat_centre = os.getenv("LOCALITAT_CENTRE")
especialitat = os.getenv("ESPECIALITAT")
carrec = os.getenv("CARREC")
situacio_laboral = os.getenv("SITUACIO_LABORAL")


# Configurar Selenium
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def wait_for_button_to_be_clickable(xpath, timeout=15):
    """Esperar que un botó sigui visible i clicable."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def solve_captcha(captcha_queue):
    """Funció per resoldre el CAPTCHA en un fil separat i passar el resultat via Queue."""
    # Importem el model de CAPTCHA dins del fil per evitar bloqueig
    from captcha_resolver import process_captcha  # Importem la funció per resoldre el CAPTCHA

    print("🧩 Resolent CAPTCHA...")
    captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'antispam.php')]")
    captcha_image_bytes = captcha_img.screenshot_as_png  # Capturem la imatge en memòria (en format PNG)

    # Passar la imatge capturada a la funció per resoldre el CAPTCHA
    captcha_text = process_captcha(captcha_image_bytes)
    
    # Enviar el resultat del CAPTCHA al Queue per retornar-lo al fil principal
    captcha_queue.put(captcha_text)


# Accedir a la pàgina del curs
url_oferta_cursos = f"https://portal.edu.gva.es/cefire/"
driver.get(url_oferta_cursos)

# Esperar que el botó d'oferta formativa sigui visible i clicar
wait_for_button_to_be_clickable("//span[@class='fl-button-text' and text()='OFERTA FORMATIVA']").click()
time.sleep(1)
url_curs = f'https://cefire.edu.gva.es/sfp/index.php?seccion=edicion&idioma=va&id={id_curs}'
driver.get(url_curs)

# Obtenir la data d'inici de la inscripció
data_inscripcio = driver.find_element(By.XPATH, "//label[contains(text(), 'Inici inscripció')]/following-sibling::div").text.strip()
print(f"Data trobada: {data_inscripcio}")
data_inici_inscripcio = parse_data_catala(data_inscripcio)
print(f"Data parsejada: {data_inici_inscripcio}")

# Calcular la diferència entre la data actual i la data d'inici de la inscripció
diferencia = (data_inici_inscripcio - datetime.now()).total_seconds()

if diferencia > 0:
    print(f"⏳ Encara no és el moment. Esperant {int(diferencia)} segons...")
    time.sleep(diferencia - 5)
else:
    print("✅ Ja es pot inscriure!")
    start_time = time.perf_counter()

# Intentar clicar el botó d'inscripció
boto_trobat = False
while not boto_trobat:
    try:
        wait_for_button_to_be_clickable("//button[span[contains(text(), 'Inscriure')]]").click()
        boto_trobat = True
        print("✅ Botó d'inscripció premut. Anant a la pàgina d'inscripció...")
        time.sleep(1)
    except Exception as e:
        print("❌ No s'ha trobat el botó d'inscripció. Refrescant la pàgina...")
        print(e)
        time.sleep(5)
        driver.refresh()

# Bucle per a intentar enviar la inscripció
intents = 3  # Número de vegades que intentarem enviar la inscripció
for attempts in range(intents):    
    # Creem un Queue per passar el resultat entre fils
    captcha_queue = Queue()

    # Llençar un fil per resoldre el CAPTCHA
    captcha_thread = Thread(target=solve_captcha, args=(captcha_queue,))
    captcha_thread.start()

    # Omplir les dades del formulari
    driver.find_element(By.NAME, "nif_nie").clear()
    driver.find_element(By.NAME, "nif_nie").send_keys(nif)
    driver.find_element(By.NAME, "nombre").clear()
    driver.find_element(By.NAME, "nombre").send_keys(nom)
    driver.find_element(By.NAME, "apellidos").clear()
    driver.find_element(By.NAME, "apellidos").send_keys(cognoms)
    driver.find_element(By.NAME, "telefono").clear()
    driver.find_element(By.NAME, "telefono").send_keys(telefon)
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "email2").clear()
    driver.find_element(By.NAME, "email2").send_keys(email)
    driver.find_element(By.NAME, "centro_nombre").clear()
    driver.find_element(By.NAME, "centro_nombre").send_keys(centre)
    driver.find_element(By.NAME, "centro_localidad").clear()
    driver.find_element(By.NAME, "centro_localidad").send_keys(localitat_centre)
    driver.find_element(By.NAME, "especialidad").clear()
    driver.find_element(By.NAME, "especialidad").send_keys(especialitat)

    # Seleccionar la situació laboral
    select_situacio = Select(driver.find_element(By.NAME, "situacion_laboral"))
    select_situacio.select_by_value(situacio_laboral)

    # Seleccionar càrrec
    select_carrec = Select(driver.find_element(By.NAME, "cargo"))
    select_carrec.select_by_value(carrec)

    # Omplir el camp del CAPTCHA
    captcha_input = driver.find_element(By.NAME, "antispam")
    captcha_input.clear()
    # Esperar que el CAPTCHA sigui resolt i obtenir el resultat
    captcha_thread.join()  # Esperem que el fil acabi d'executar-se
    captcha_text = captcha_queue.get()  # Obtenim el resultat del Queue
    print(f"🔍 Text detectat: {captcha_text}")

    if captcha_text:
        captcha_input.send_keys(captcha_text)

        # Prem el botó "Confirmar" per enviar la inscripció
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Confirmar']").click()
    else:
        print(f"❌ CAPTCHA no detectat. Ho intentem de nou. {intents - attempts} intents restants.")
        time.sleep(1)

    # Comprovar si la pàgina de confirmació es carrega
    if "han de ser exactamente los mismos" in driver.page_source.lower():
        driver.refresh()
        print(f"❌ CAPTCHA no detectat. Ho intentem de nou. {intents - attempts} intents restants.")
        time.sleep(1)
    else:
        break

end_time = time.perf_counter()

# Calcular el temps transcorregut
execution_time = (end_time - start_time) * 1000

print(f"✅ Inscripció enviada! Temps total: {execution_time:.2f} ms")
time.sleep(5)
driver.quit()
