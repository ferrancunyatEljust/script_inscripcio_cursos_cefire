
# Script d'Inscripció als Curs CEFIRE

Aquest script automatitza el procés d'inscripció a un curs del portal CEFIRE. Utilitza **Selenium** per interactuar amb la pàgina web i una xarxa neuronal convolucional molt simple per resoldre el CAPTCHA,  utilitzant un model de reconeixement de caràcters.

## Requisits

Assegura't de tindre instal·lat el navegador *Google Chrome*. Si es vol utilitzar Firefox o qualsevol altre, s'hauria d'utilitzar el webdriver de selenium corresponent.

## Instal·lació

1. **Crea un entorn virtual** (opcional però recomanat):

   ```bash
   python -m venv venv
   ```

2. **Activa l'entorn virtual**:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/macOS**: `source venv/bin/activate`

3. **Instal·la les dependències**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuració

Abans d'executar l'script, has de configurar les variables d'entorn. Tens l'arxiu d'exemple [.env.example](.env.example) que hauràs de modificar amb les teues dades. Una vegada modificat, guarda'l com a `.env` a la mateixa carpeta que el teu script.

L'id del curs, el pots obtindre de la URL amb la informació del curs, per exemple:

`https://cefire.edu.gva.es/sfp/index.php?seccion=edicion&id=12688077`

L'id del curs seria `12688077`.

```env .env.example
   # Exemple de fitxer .env per a la configuració del projecte

   # ID del curs per inscriure's.
   ID_CURS=12345678

   # NIF o NIE de l'usuari
   NIF=12345678A

   # Nom de la persona
   NOM=Juan

   # Cognoms de la persona
   COGNOMS=Pérez Pérez

   # Telèfon de la persona
   TELEFON=600000000

   # Correu electrònic principal
   EMAIL=juan.perez@example.com

   # Nom del centre
   CENTRO_NOMBRE=IES Jaume II "El Just"

   # Localitat del centre
   CENTRO_LOCALIDAD=Tavernes de la Valldigna

   # Especialitat de la persona
   ESPECIALIDAD=SAI

   # Càrrec laboral (veure les opcions disponibles)
   CARGO=sin cargo
   '''
      "sin cargo" -> Sense càrrec
      "tutor_coordinador" -> Tutor / Coordinador
      "equipo_directivo" -> Equip Directiu
      "asesor" -> Assessor
      "jefatura_departamento" -> Cap De Departament
   '''


   # Situació laboral (veure les opcions disponibles)
   SITUACION_LABORAL=
   ''' 
      3 -> Funcionari de carrera definitiu
      2 -> Funcionari de carrera provisional
      4 -> Funcionari en pràctiques
      1 -> Funcionari interí
      0 -> En borsa / Altres
   '''

```

Aquestes variables s'utilitzen per omplir el formulari de registre.

## Com executar l'script

Per executar l'script, simplement fes-ho des de la línia de comandes:

```bash
python main.py
```

### Descripció del funcionament:

1. **Carrega les variables d'entorn** per obtenir la informació del curs i la teva informació personal.
2. **Accedeix a la pàgina del curs** i espera fins que el moment per inscriure's sigui el correcte (segons la data).
3. **Resoldre el CAPTCHA**:
   - El script captura la imatge del CAPTCHA, la passa a un model de reconeixement de caràcters (OCR) per obtenir el text.
   - Es resol el CAPTCHA en un fil separat per evitar bloquejar l'execució de Selenium.
4. **Omple el formulari d'inscripció** amb la informació personal i el text del CAPTCHA resolt.
5. **Intenta enviar la inscripció**. Si el CAPTCHA no es detecta correctament, es torna a intentar fins a un màxim de 3 intents.
6. **Mostra el temps total** que ha trigat en completar la inscripció.

### Exemple de sortida de la consola:

```
Data trobada: 2025-04-01
Data parsejada: 2025-04-01 00:00:00
⏳ Encara no és el moment. Esperant 3600 segons...
✅ Ja es pot inscriure!
🧩 Resolent CAPTCHA...
🔍 Text detectat: 12345
✅ Inscripció enviada! Temps total: 1500.25 ms
```

## Advertència important

## Importants Advertències

L'script ha sigut provat per l'autor, no obstant això, l'autor d'aquest repositori no es fa responsable si la inscripció no es completa o si es produeixen errors durant el procés d'inscripció. Aquest script automatitza la interacció amb el portal CEFIRE, però pot estar subjecte a canvis en la pàgina web o en els mecanismes de seguretat, com el CAPTCHA. Assegura't de revisar que la inscripció s'haja completat correctament després d'executar l'script.

Aquest script és proporcionat "tal qual" i s'utilitza sota el teu propi risc. L'ús d'aquest script per qualsevol fi no autoritzat o en contravenció de les condicions del portal CEFIRE és responsabilitat de l'usuari.


## Entrenament de l'OCR

Si vols reentrenar el model que resol el captcha, ho pots fer amb el següent script de python.

- [Model](keras_cnn/dataset_digit/model/model.py)

Si vols provar el nou model que has reentrenat, utilitza:

- [Captcha resolver train](keras_cnn/dataset_digit/model/captcha_resolver_train.py)

## Contribucions

Si tens millores per aportar o has trobat algun error, per favor, fes un **fork** del projecte i envia un **pull request**.

---

Aquest projecte està disponible sota la llicència GNU/GPLv3.
