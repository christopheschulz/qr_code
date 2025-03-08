import sys
import json
from pathlib import Path

# gestion génération QR code
import qrcode
import qrcode.constants
#gestion lecture QR code
import cv2

DIR_QR_IMG = "qr_img"
DIR_QR_CONFIG = "config"

def qr_code_generation_parameters(qr_version,qr_error_correct,qr_box_size,qr_border):
    # version

    # The version parameter is an integer from 1 to 40 
    # that controls the size of the QR Code 
    # (the smallest, version 1, is a 21x21 matrix). 
    # Set to None and use the fit parameter when making 
    # the code to determine this automatically.

    # constante d'erreur de génération voir fichier help for QR code dans help
    QR_ERROR_CORRECT_L = qrcode.constants.ERROR_CORRECT_L # 7%
    QR_ERROR_CORRECT_M = qrcode.constants.ERROR_CORRECT_M # 15%
    QR_ERROR_CORRECT_Q = qrcode.constants.ERROR_CORRECT_Q # 25%
    QR_ERROR_CORRECT_H = qrcode.constants.ERROR_CORRECT_H # 30%

    # box size
    # The box_size parameter controls how many 
    # pixels each “box” of the QR code is.


    # border
    # The border parameter controls how many 
    # boxes thick the border should be 
    # (the default is 4, which is the minimum according to the specs).
    return qr_version,qr_error_correct,qr_box_size,qr_border

def generate_qr_code(qr_text,
                     qr_version=None,
                     qr_error_correction=qrcode.constants.ERROR_CORRECT_M,
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
    qr_img_folder = p / DIR_QR_IMG
    file_path = ""
    qr_img_number = 0
    
    while Path(file_path).exists():
        file_path = qr_img_folder / f"QR{str(qr_img_number).zfill(3)}.png"
        qr_img_number += 1
    return file_path


def get_file_path(file):
    p = Path.cwd()
    qr_img_folder = p / DIR_QR_IMG
    file_path = qr_img_folder / file
    if Path(file_path).exists():
        return file_path
   

def load_qr_config():
    pass


def save_qr_config(qr_version,qr_error_correction,qr_box_size,qr_border):
    ## to do
    # je pense qu'ici il serait bon de checker si les 
    # valeurs sont correctes avant sauvegarde
    qr_config_dict = {}
    p = Path.cwd()
    qr_config_folder = p / DIR_QR_CONFIG
    file = "qr_code.config"
    file_path = qr_config_folder / file
    qr_config_dict["version"] = qr_version
    qr_config_dict["error_correction"] = qr_error_correction
    qr_config_dict["box_size"] = qr_box_size
    qr_config_dict["border"] = qr_border

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(qr_config_dict, f, indent=4, ensure_ascii=False)


def get_arguments():
    arguments = sys.argv[1:]
    return arguments
   

def len_arguments_is_valid(arguments,len_arguments):
    return len(arguments) == len_arguments


def display_help_arguments():
    print(" Use -g to generate a QR code, followed by the text to be encoded."
    "\n Use -r, followed by the QR code image filename, to extract and decode its contents.")


def main():
    arguments = get_arguments()
    len_arguments = 2
    if not len_arguments_is_valid(arguments,len_arguments):
        display_help_arguments()
        return
    qr_handler = arguments[0]
    qr_entry = arguments[1]

    if qr_handler == "-g":
        qr_text = qr_entry
        ## pour l'instant je ne gère pas les paramètres de la classe qrcode
        generate_qr_code(qr_text)
    elif qr_handler == "-r":
        file_name = qr_entry
        file_path = get_file_path(file_name)
        if not file_path:
            print("file not exist")
            return
        print(read_qr_code(file_path))
    elif qr_handler == "-conf":
        print("gestion config à faire")

    else :
         display_help_arguments()


if __name__ == "__main__":
     # main()

    save_qr_config(qr_version=None,
                     qr_error_correction=qrcode.constants.ERROR_CORRECT_M,
                     qr_box_size=10,
                     qr_border=4)