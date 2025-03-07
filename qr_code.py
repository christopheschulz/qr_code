import sys
from pathlib import Path

import qrcode
import qrcode.constants
import cv2

# constante
QR_ERROR_CORRECT_L = qrcode.constants.ERROR_CORRECT_L # 7%
QR_ERROR_CORRECT_M = qrcode.constants.ERROR_CORRECT_M # 15%
QR_ERROR_CORRECT_Q = qrcode.constants.ERROR_CORRECT_Q # 25%
QR_ERROR_CORRECT_H = qrcode.constants.ERROR_CORRECT_H # 30%

# variable à gérer avant la génération
qr_version = None # maximum 40
qr_box_size = 10
qr_border = 4 # minimum 4
qr_img_number = 0


def generate_qr_code(qr_version=1,
                     qr_error_correction=QR_ERROR_CORRECT_M,
                     qr_box_size=10,
                     qr_border=4):
    
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qr_error_correction,
        box_size=qr_box_size,
        border=qr_border,
    )
    qr.add_data('Some data') # entre parenthèses c'est le texte à transformer
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    ## to do
    # attention là il faut une gestion de fichier
    file = file_name_path()
    img.save(file)


def read_qr_code():
    # read the QRCODE image
    ## to do
    # attention là il faut une gestion de fichier
    file = save_file()
    img = cv2.imread(file)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    # detect and decode
    data = detector.detectAndDecode(img) 
    text_qr_code = data[0]
    print(text_qr_code)   


def save_file():
    p = Path.cwd()
    qr_folder = p / "QR"
    
    while Path(file_path).exists():
        file_name = f"QR{str(qr_img_number).zfill(3)}.png"
        file_path = qr_folder / file_name
        qr_img_number += 1
       
    return file_path


def get_arguments():
    arguments = sys.argv[1:]


def qr_code():
    
    generate_qr_code(qr_version,QR_ERROR_CORRECT_L,qr_box_size,qr_border)
    # read_qr_code()


qr_code()