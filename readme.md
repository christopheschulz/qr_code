# qr_code

python version 3.13
```
# import for generate qr_code
import qrcode
import qrcode.constants
# import for read qr_code
import cv2
```

# parameters:

    Use -g to generate a QR code, followed by the text to be encoded.

    Use -r, followed by the QR code image filename, to extract and decode its contents.

    Use -c to manage config


# parameters definition:
- version=1
- error_correction=qrcode.constants.ERROR_CORRECT_L
- box_size=10
- border=4

The version parameter is an integer from 1 to 40 that controls the size of the QR Code (the smallest, version 1, is a 21x21 matrix). Set to None and use the fit parameter when making the code to determine this automatically.

The error_correction parameter controls the error correction used for the QR Code. The following four constants are made available on the qrcode package:
- qrcode.constants.ERROR_CORRECT_L : About 7% or less errors can be corrected.
- qrcode.constants.ERROR_CORRECT_M : About 15% or less errors can be corrected.
- qrcode.constants.ERROR_CORRECT_Q : About 25% or less errors can be corrected.
- qrcode.constants.ERROR_CORRECT_H :About 30% or less errors can be corrected.


The box_size parameter controls how many pixels each “box” of the QR code is.

The border parameter controls how many boxes thick the border should be (the default is 4, which is the minimum according to the specs).




























# gestion d'une vcard
vcard_data = """BEGIN:VCARD
VERSION:3.0
N:Dupont;Jean;;;
FN:Jean Dupont
ORG:Entreprise XYZ
TITLE:Directeur Général
TEL;TYPE=WORK,VOICE:+33123456789
TEL;TYPE=CELL:+33698765432
EMAIL;TYPE=WORK:jean.dupont@example.com
URL:https://www.entreprise-xyz.com
ADR;TYPE=WORK:;;10 Rue Exemple;Paris;;75001;France
END:VCARD"""


# gestion email
## Définir l'adresse e-mail et le sujet/message (optionnel)
email = "exemple@email.com"
subject = "Sujet du message"
body = "Bonjour, ceci est un test."
## Format mailto avec sujet et corps
mailto_link = f"mailto:{email}?subject={subject}&body={body}"


# gestion sms
telephone = "+33612345678"
message = "Bonjour, ceci est un test de QR Code pour SMS."
## Format SMS pour QR Code
sms_data = f"SMSTO:{telephone}:{message}"


# gestion wifi
ssid = "Nom_du_WiFi"
password = "MotDePasseWiFi"
encryption = "WPA"  # Peut être WEP, WPA ou laisser vide pour un réseau ouvert
## Format du texte Wi-Fi pour un QR Code
wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{password};;"


# gestion coordonnées
## Coordonnées GPS de l'emplacement
latitude = 48.8566
longitude = 2.3522  # Paris
## Générer un lien Google Maps avec les coordonnées
google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"