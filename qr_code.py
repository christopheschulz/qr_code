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


def generate_qr_code(qr_text,
                     qr_version=None,
                     qr_error_correction=QR_ERROR_CORRECT_M,
                     qr_box_size=10,
                     qr_border=4):
    
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qr_error_correction,
        box_size=qr_box_size,
        border=qr_border,
    )
    qr.add_data(qr_text) # entre parenthèses c'est le texte à transformer
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    ## to do
    # attention là il faut une gestion de fichier
    file = save_file()
    img.save(file)


def read_qr_code(file):
    # read the QRCODE image
    img = cv2.imread(file)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    # detect and decode
    # retourne un tuple. Le texte est dans la première variable de ce tuple
    data = detector.detectAndDecode(img) 
    text_qr_code = data[0]
    return text_qr_code


def save_file():
    p = Path.cwd()
    qr_folder = p / "QR"
    file_path = ""
    qr_img_number = 0
    
    while Path(file_path).exists():
        qr_img_number += 1
        file_path = qr_folder / f"QR{str(qr_img_number).zfill(3)}.png"
       
    return file_path


def load_file(file):
    p = Path.cwd()
    qr_folder = p / "QR"
    file_path = qr_folder / file
    if Path(file_path).exists():
        return file_path
   

def get_arguments():
    arguments = sys.argv[1:]
    return arguments
   

def len_arguments_is_valid(arguments,len_arguments):
    return len(arguments) == len_arguments


def arguments_has_error():
    print(" Use -g to generate a QR code, followed by the text to be encoded."
    "\n Use -r, followed by the QR code image filename, to extract and decode its contents.")


def qr_code():
    arguments = get_arguments()
    len_arguments = 2
    if not len_arguments_is_valid(arguments,len_arguments):
        arguments_has_error()
        return
    qr_handler = arguments[0]
    qr_entry = arguments[1]

    if qr_handler == "-g":
        qr_text = qr_entry
        ## pour l'instant je ne gère pas les paramètres de la classe qrcode
        generate_qr_code(qr_text)
    
    elif qr_handler == "-r":
        file_name = qr_entry
        file_path = load_file(file_name)
        if not file_path:
            print("file not exist")
            return
        print(read_qr_code(file_path))
    else :
         arguments_has_error()


qr_code()