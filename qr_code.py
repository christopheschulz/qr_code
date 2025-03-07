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
                     qr_version=1,
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
    ## to do
    # load file à défibir
    # file = load_file() 
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
    print(""" -g to generate a QR code \n -r to read a QR code
""")


def qr_code():
    arguments = get_arguments()
    len_arguments = 1
    if not len_arguments_is_valid(arguments,len_arguments):
        arguments_has_error()
        return
    if arguments[0] == "-g":
        ## to do
        # pour l'instant j'envoie le lien en manuel, à gérer avec ligne de commande
        qr_text = "https://docs.python.org/3/library/pathlib.html#module-pathlib"
        generate_qr_code(qr_text,qr_version,QR_ERROR_CORRECT_L,qr_box_size,qr_border)
    elif arguments[0] == "-r":
    ## to do
    # pour l'instant j'envoie le fichier en manuel, à gérer avec ligne de commande
        file_name = "QR002.png"
        file_path = load_file(file_name)
        if not file_path:
            return
        read_qr_code(file_path)
    else :
         arguments_has_error()


qr_code()