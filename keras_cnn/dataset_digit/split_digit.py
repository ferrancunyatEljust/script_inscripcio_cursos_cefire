import os
from PIL import Image

# Directori amb les imatges
image_dir = os.path.join(os.path.dirname(__file__), "val_images")  # Canvia aquest camí pel teu directori real

digit_widths = [17, 17, 18, 18, 17, 18, 17, 20, 18]

# Funció per processar cada imatge
def process_captcha_image(image_path):
    # Carregar la imatge
    captcha_image = Image.open(image_path)

    frame_width = 3
    frame_height = 2
    # Eliminar els marges de la imatge
    captcha_image = captcha_image.crop((frame_width, frame_height, captcha_image.width - frame_width, captcha_image.height - frame_height))
    
    # Extreure el nom del fitxer sense extensió (el número del captcha)
    base_name = os.path.basename(image_path)
    label = base_name.split('.')[0]  # Obtenir el número sense l'extensió (ex: '14287' -> '14287')

    acc_width = 0
    for digit in label:
        if not digit.isdigit():
            continue
        # Dividir la imatge i desar cada part amb l'etiqueta
        i = int(digit)
        digit_width = digit_widths[i]
        digit_image = captcha_image.crop((acc_width, 0, acc_width + digit_width, captcha_image.height))
        acc_width += digit_width
        # Guardar amb el nom format digit_label_X.png
        output_filename = f"{digit}_{label}.png"
        digit_image.save(os.path.join(image_dir, output_filename))

# Processar totes les imatges al directori
for filename in os.listdir(image_dir):
    if filename.endswith('.png'):  # Només processar imatges .png
        process_captcha_image(os.path.join(image_dir, filename))
