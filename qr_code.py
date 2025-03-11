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
QR_CONFIG_FILE = "config.json"

QR_ERROR_CORRECT_L = qrcode.constants.ERROR_CORRECT_L # 7%
QR_ERROR_CORRECT_M = qrcode.constants.ERROR_CORRECT_M # 15%
QR_ERROR_CORRECT_Q = qrcode.constants.ERROR_CORRECT_Q # 25%
QR_ERROR_CORRECT_H = qrcode.constants.ERROR_CORRECT_H # 30%


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
   
    file = get_qr_code_img_file_path()
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


#file
def get_file_path(file,dir):
    p = Path.cwd()
    folder = p / dir
    file_path = folder / file
    if Path(file_path).exists():
        return file_path


def get_qr_code_img_file_path():
    p = Path.cwd()
    qr_img_folder = p / DIR_QR_IMG
    file_path = ""
    qr_img_number = 0
    
    while Path(file_path).exists():
        file_path = qr_img_folder / f"QR{str(qr_img_number).zfill(3)}.png"
        qr_img_number += 1
    return file_path


# Config 
def config_user_input():
    
    print("Veuillez entrer les valeurs des configurations suivantes demandée.")
    qr_version = input("Entrez la version du QR code (1 à 40 ou entrée vide pour adaptation auto de la version) :")
    if qr_version == "":
        qr_version = None

    qr_error_correct = input("Entrer le facteur d'erreur du QR Code (L/M/Q/H) :")
    if qr_error_correct.upper() == "L":
        qr_error_correct = QR_ERROR_CORRECT_L
    elif qr_error_correct.upper() == "M":
         qr_error_correct = QR_ERROR_CORRECT_M
    elif qr_error_correct.upper() == "Q":
         qr_error_correct = QR_ERROR_CORRECT_Q
    elif qr_error_correct.upper() == "H":
         qr_error_correct = QR_ERROR_CORRECT_H
    else:
        qr_error_correct = ""
        
    qr_box_size = input("Entrez la grandeur du QR Code :")
    qr_border = input("Entrez la largeur du bord (minimum 4):")

    # check si les valeurs sont ok sinon rectifie et en informe l'utilisateur
    qr_version,qr_error_correct,qr_box_size,qr_border = check_qr_code_config_parameters(qr_version,qr_error_correct,qr_box_size,qr_border)

    return qr_version,qr_error_correct,qr_box_size,qr_border


def load_qr_config():
    p = Path.cwd()
    folder = p / DIR_QR_CONFIG
    file_path = folder / QR_CONFIG_FILE
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Problème avec la lecture du json")
        return
    except FileNotFoundError:
        print(f"Il semblerai que le fichier {file_path} soit introuvable")
        return
    
    qr_version = data["version"]
    qr_error_correct = data["error_correction"]
    qr_box_size = data["box_size"]
    qr_border = data["border"]

    # check si les valeurs sont ok sinon rectifie et en informe l'utilisateur
    qr_version,qr_error_correct,qr_box_size,qr_border = check_qr_code_config_parameters(qr_version,qr_error_correct,qr_box_size,qr_border)
    
    return qr_version,qr_error_correct,qr_box_size,qr_border


def save_qr_config(file_path,qr_version,qr_error_correct,qr_box_size,qr_border):
    # # check si les valeurs sont ok sinon rectifie et en informe l'utilisateur
    # qr_version,qr_error_correct,qr_box_size,qr_border = qr_code_parameters_checker(qr_version,qr_error_correct,qr_box_size,qr_border)
    
    qr_config_dict = {}

    update_config_version = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
   
    qr_config_dict["update"] = update_config_version
    qr_config_dict["version"] = qr_version
    qr_config_dict["error_correction"] = qr_error_correct
    qr_config_dict["box_size"] = qr_box_size
    qr_config_dict["border"] = qr_border

    try :
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(qr_config_dict, f, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        print("Problème avec la lecture du json")
        return
    except FileNotFoundError:
        print(f"Il semblerai que le fichier {file_path} soit introuvable")
        return


def check_qr_code_config_parameters(qr_version,qr_error_correct,qr_box_size,qr_border):
    parameter_changed = False # pour la recherche de modif
    # version
    if not qr_version == None:
        if str(qr_version).isdigit():
            qr_version = int(qr_version)
        else:
            print("Le paramètre 'version' doit être un int . Nouvelle valeur initialisée à 1 ")
            qr_version = 1
            parameter_changed = True
        if qr_version > 40:
            print("Le paramètre 'version' ne peut pas être supérieur à 40. Nouvelle valeur initialisée à 40 ")
            qr_version = 40
            parameter_changed = True
        elif qr_version < 1:
            print("Le paramètre 'version' ne peut pas être infèrieur à 1. Nouvelle valeur initialisée à 1 ")
            qr_version = 1
            parameter_changed = True
    
    # error_correction
    if str(qr_error_correct).isdigit():
        qr_error_correct = int(qr_error_correct)
    else:
        print("Le paramètre 'error correction'  doit être un int. Nouvelle valeur initialisée à 0 ")
        qr_error_correct = 0
        parameter_changed = True
    if qr_error_correct > 3:
        print("Le paramètre 'error correction'  ne peut pas être supérieur à 3. Nouvelle valeur initialisée à 3 ")
        qr_error_correct = 3
        parameter_changed = True
    elif qr_error_correct < 0:
        print("Le paramètre 'error correction'  ne peut pas être infèrieur à 0. Nouvelle valeur initialisée à 0 ")
        qr_error_correct = 0
        parameter_changed = True

    # box size
    if str(qr_box_size).isdigit():
        qr_box_size = int(qr_box_size)
    else:
        print("Le paramètre 'box size'  doit être un int. Nouvelle valeur initialisée à 10 ")
        qr_box_size = 10
        parameter_changed = True
    if qr_box_size < 1:
        print("Le paramètre 'box size'  ne peut pas être infèrieur à 1. Nouvelle valeur initialisée à 10 ")
        qr_box_size = 10
        parameter_changed = True

    # border
    if str(qr_border).isdigit():
        qr_border = int(qr_border)
    else:
        print("Le paramètre 'border'  doit être un int. Nouvelle valeur initialisée à 4 ")
        qr_border = 4
        parameter_changed = True
    if qr_border < 4:
        print("Le paramètre 'border'  ne peut pas être infèrieur à 4. Nouvelle valeur initialisée à 4 ")
        qr_border = 4
        parameter_changed = True
    
    if parameter_changed:
        file_path = get_file_path(QR_CONFIG_FILE, DIR_QR_CONFIG)
        save_qr_config(file_path,
                       qr_version,
                       qr_error_correct,
                       qr_box_size,
                       qr_border)
        
    return qr_version,qr_error_correct,qr_box_size,qr_border


#arguments
def get_arguments():
    arguments = sys.argv[1:]
    return arguments
   

def display_help_arguments():
    print(" Use -g to generate a QR code, followed by the text to be encoded."
    "\n Use -r, followed by the QR code image filename, to extract and decode its contents."
    "\n Use -c to manage config")


def is_length_arguments_ok(arguments,lenght):
    return len(arguments) == lenght


# handle
def handle_generate_qr(qr_entry):
    config_args = load_qr_config()
    if config_args:
        qr_text = qr_entry
        generate_qr_code(qr_text,*config_args)


def handle_decode_qr(qr_entry):
    file_path = get_file_path(qr_entry, DIR_QR_IMG)
    if not file_path:
        print(f"le fichier {qr_entry} n'existe pas !")
        return
    print(read_qr_code(file_path))


def handle_change_config_qr():
    file_path = get_file_path(QR_CONFIG_FILE, DIR_QR_CONFIG)
    if not file_path:
        print(f"le fichier de config {QR_CONFIG_FILE} n'existe pas !")
        return
    config_args = config_user_input()
    save_qr_config(file_path,
                        *config_args)


# main
def main():
    arguments = get_arguments()
    qr_handler = arguments[0] 
    
    if qr_handler == "-g" and is_length_arguments_ok(arguments,2): # générer un qr_code
        qr_entry = arguments[1]
        handle_generate_qr(qr_entry)
    elif qr_handler == "-r" and is_length_arguments_ok(arguments,2): # lire un qr_code à partir d'une image
        qr_entry = arguments[1]
        handle_decode_qr(qr_entry)
    elif qr_handler == "-c" and is_length_arguments_ok(arguments,1): # changer config QR code
        handle_change_config_qr() 
    else:
        display_help_arguments()

 
if __name__ == "__main__":
    main()
 