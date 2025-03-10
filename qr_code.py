import sys
import datetime
import json
from pathlib import Path

# gestion génération QR code
import qrcode
import qrcode.constants
#gestion lecture QR code
import cv2

DIR_QR_IMG = "qr_img"
DIR_QR_CONFIG = "config"
QR_CONFIG_FILE = "qr_code.config"

QR_ERROR_CORRECT_L = qrcode.constants.ERROR_CORRECT_L # 7%
QR_ERROR_CORRECT_M = qrcode.constants.ERROR_CORRECT_M # 15%
QR_ERROR_CORRECT_Q = qrcode.constants.ERROR_CORRECT_Q # 25%
QR_ERROR_CORRECT_H = qrcode.constants.ERROR_CORRECT_H # 30%
print(QR_ERROR_CORRECT_L,QR_ERROR_CORRECT_M,QR_ERROR_CORRECT_Q,QR_ERROR_CORRECT_H)


def generation_qr_code_parameters_checker(qr_version,qr_error_correct,qr_box_size,qr_border):
   
    if qr_version.isdigit():
        qr_version = int(qr_version)
    else:
        print("Le paramètre 'version' doit être un int . Nouvelle valeur initialisée à 1 ")
        qr_version = 1
    if qr_version > 40:
        print("Le paramètre 'version' ne peut pas être supérieur à 40. Nouvelle valeur initialisée à 40 ")
        qr_version = 40
    elif qr_version < 1:
        print("Le paramètre 'version' ne peut pas être infèrieur à 1. Nouvelle valeur initialisée à 1 ")
        qr_version = 1
    
    if qr_error_correct.isdigit():
        qr_error_correct = int(qr_error_correct)
    else:
        print("Le paramètre 'error correction'  doit être un int. Nouvelle valeur initialisée à 0 ")
        qr_error_correct = 0
    if qr_error_correct > 3:
        print("Le paramètre 'error correction'  ne peut pas être supérieur à 3. Nouvelle valeur initialisée à 3 ")
        qr_error_correct = 3
    elif qr_error_correct < 0:
        print("Le paramètre 'error correction'  ne peut pas être infèrieur à 0. Nouvelle valeur initialisée à 0 ")
        qr_error_correct = 0

    if qr_box_size.isdigit():
        qr_box_size = int(qr_box_size)
    else:
        print("Le paramètre 'box size'  doit être un int. Nouvelle valeur initialisée à 1 ")
        qr_box_size = 1
    if qr_box_size < 1:
        print("Le paramètre 'box size'  ne peut pas être infèrieur à 1. Nouvelle valeur initialisée à 1 ")
        qr_box_size = 1

    if qr_border.isdigit():
        qr_border = int(qr_border)
    else:
        print("Le paramètre 'border'  doit être un int. Nouvelle valeur initialisée à 4 ")
        qr_border = 4
    if qr_border < 4:
        print("Le paramètre 'border'  ne peut pas être infèrieur à 4. Nouvelle valeur initialisée à 4 ")
        qr_box_size = 4
   
    return qr_version,qr_error_correct,qr_box_size,qr_border


def generate_qr_code(qr_text,
                     qr_version=None,
                     qr_error_correction=1,
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
   
    file = save_qr_code_img()
    img.save(file)


def save_qr_code_img():
    p = Path.cwd()
    qr_img_folder = p / DIR_QR_IMG
    file_path = ""
    qr_img_number = 0
    
    while Path(file_path).exists():
        file_path = qr_img_folder / f"QR{str(qr_img_number).zfill(3)}.png"
        qr_img_number += 1
    return file_path


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


def get_file_path(file,dir):
    p = Path.cwd()
    folder = p / dir
    file_path = folder / file
    if Path(file_path).exists():
        return file_path


# Config 
def manage_config():
    ## todo
    # reste à gérer les errrus de
    print("Veuillez entrer les valeurs des configurations suivantes demandée.")
    qr_version = input("Entrez la version du QR code (1 - 40) :")
    qr_error_correct = input("Entrer le facteur d'erreur du QR Code (L/M/Q/H) :")
    if qr_error_correct.upper() == "L":
        qr_error_correct = str(QR_ERROR_CORRECT_L)
    elif qr_error_correct.upper() == "M":
         qr_error_correct = str(QR_ERROR_CORRECT_M)
    elif qr_error_correct.upper() == "Q":
         qr_error_correct = str(QR_ERROR_CORRECT_Q)
    elif qr_error_correct.upper() == "H":
         qr_error_correct = str(QR_ERROR_CORRECT_H)
    else:
        qr_error_correct = ""
        
    qr_box_size = input("Entrez la grandeur du QR Code :")
    qr_border = input("Entrez la largeur du bord (minimum 4):")

    qr_version,qr_error_correct,qr_box_size,qr_border = generation_qr_code_parameters_checker(qr_version,qr_error_correct,qr_box_size,qr_border)

    return qr_version,qr_error_correct,qr_box_size,qr_border


def load_qr_config():
    p = Path.cwd()
    folder = p / DIR_QR_CONFIG
    file_path = folder / QR_CONFIG_FILE
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    qr_version = data["version"]
    qr_error_correction = data["error_correction"]
    qr_box_size = data["box_size"]
    qr_border= data["border"]
    return qr_version,qr_error_correction,qr_box_size,qr_border


def save_qr_config(file_path,qr_version,qr_error_correction,qr_box_size,qr_border):
    ## to do
    # je pense qu'ici il serait bon de checker si les 
    # valeurs sont correctes avant sauvegarde
    qr_config_dict = {}

    update_config_version = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
   
    qr_config_dict["update"] = update_config_version
    qr_config_dict["version"] = qr_version
    qr_config_dict["error_correction"] = qr_error_correction
    qr_config_dict["box_size"] = qr_box_size
    qr_config_dict["border"] = qr_border

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(qr_config_dict, f, indent=4, ensure_ascii=False)


#arguments
def get_arguments():
    arguments = sys.argv[1:]
    return arguments
   

def len_arguments_is_valid(arguments,len_arguments):
    return len(arguments) == len_arguments


def display_help_arguments():
    print(" Use -g to generate a QR code, followed by the text to be encoded."
    "\n Use -r, followed by the QR code image filename, to extract and decode its contents."
    "\n Use -c to manage config, followed by name of config Enter in a selected config mode")


# main
def main():
    arguments = get_arguments()
    len_arguments = 2
    if not len_arguments_is_valid(arguments,len_arguments):
        display_help_arguments()
        return
    qr_handler = arguments[0]
    qr_entry = arguments[1]

    if qr_handler == "-g": # générer un qr_code
        config_args = load_qr_config()
       
        qr_text = qr_entry
        ## pour l'instant je ne gère pas les paramètres de la classe qrcode
        generate_qr_code(qr_text,*config_args)

    elif qr_handler == "-r": # lire un qr_code à partir d'une image
        file_name = qr_entry
        file_path = get_file_path(file_name, DIR_QR_IMG)
        if not file_path:
            print(f"le fichier {file_name} n'existe pas !")
            return
        print(read_qr_code(file_path))
        
    elif qr_handler == "-c":
        file_name = qr_entry
        file_path = get_file_path(file_name, DIR_QR_CONFIG)
        if not file_path:
            print(f"le fichier de config {file_name} n'existe pas !")
            return
        config_args = manage_config()
        save_qr_config(file_path,
                       *config_args)
        
    else :
         display_help_arguments()


if __name__ == "__main__":
    main()

    