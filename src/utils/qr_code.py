import logging
import datetime
import json
from pathlib import Path
from django.conf import settings

import qrcode
import qrcode.constants
import cv2
import numpy as np

logger = logging.getLogger(__name__)

DIR_QR_IMG = "QrCodeReader/static/qr_img"
DIR_QR_CONFIG = "QrCodeReader/config"
QR_CONFIG_FILE = "config.json"

QR_ERROR_CORRECT_L = qrcode.constants.ERROR_CORRECT_L  # 7%
QR_ERROR_CORRECT_M = qrcode.constants.ERROR_CORRECT_M  # 15%
QR_ERROR_CORRECT_Q = qrcode.constants.ERROR_CORRECT_Q  # 25%
QR_ERROR_CORRECT_H = qrcode.constants.ERROR_CORRECT_H  # 30%


def generate_qr_code(qr_text, qr_version=None, qr_error_correction=1,
                     qr_box_size=10, qr_border=4):
    """Génère un QR code et le sauvegarde dans un fichier."""
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qr_error_correction,
        box_size=qr_box_size,
        border=qr_border,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    file = get_qr_code_img_file_path()
    img.save(file)


def read_qr_code(file):
    """Lit un QR code depuis un fichier image."""
    img = cv2.imread(file)
    if img is None:
        logger.error("Impossible de lire l'image %s", file)
        return None
    detector = cv2.QRCodeDetector()
    decoded_text, points, _ = detector.detectAndDecode(img)
    if decoded_text:
        return decoded_text
    else:
        logger.warning("QR détecté mais illisible ou vide")
        return None


def read_qr_code_from_bytes(img_data):
    """Lit un QR code depuis des données binaires d'image."""
    try:
        np_arr = np.asarray(bytearray(img_data), dtype=np.uint8)
        img_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img_cv2 is None:
            raise ValueError("Impossible de décoder l'image")

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img_cv2)

        if bbox is not None and data:
            return data
        return None
    except Exception as e:
        logger.error("Erreur de lecture QR: %s", e)
        return None


def get_file_path(file, dir):
    """Retourne le chemin complet d'un fichier dans un répertoire."""
    folder = Path(settings.BASE_DIR) / dir
    file_path = folder / file
    if file_path.exists():
        return file_path


def get_qr_code_img_file_path():
    """Génère un chemin de fichier unique pour une image QR."""
    qr_img_folder = Path(settings.BASE_DIR) / DIR_QR_IMG
    qr_img_folder.mkdir(parents=True, exist_ok=True)
    qr_img_number = 0
    file_path = qr_img_folder / f"QR{str(qr_img_number).zfill(3)}.png"
    while file_path.exists():
        qr_img_number += 1
        file_path = qr_img_folder / f"QR{str(qr_img_number).zfill(3)}.png"
    return file_path


def load_qr_config():
    """Charge la configuration QR depuis le fichier JSON."""
    p = Path.cwd()
    folder = p / DIR_QR_CONFIG
    file_path = folder / QR_CONFIG_FILE
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        logger.error("Problème avec la lecture du JSON de config")
        return
    except FileNotFoundError:
        logger.error("Fichier de config introuvable: %s", file_path)
        return

    qr_version = data["version"]
    qr_error_correct = data["error_correction"]
    qr_box_size = data["box_size"]
    qr_border = data["border"]

    qr_version, qr_error_correct, qr_box_size, qr_border = check_qr_code_config_parameters(
        qr_version, qr_error_correct, qr_box_size, qr_border
    )
    return qr_version, qr_error_correct, qr_box_size, qr_border


def save_qr_config(file_path, qr_version, qr_error_correct, qr_box_size, qr_border):
    """Sauvegarde la configuration QR dans un fichier JSON."""
    qr_version, qr_error_correct, qr_box_size, qr_border = check_qr_code_config_parameters(
        qr_version, qr_error_correct, qr_box_size, qr_border
    )

    qr_config_dict = {
        "update": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "version": qr_version,
        "error_correction": qr_error_correct,
        "box_size": qr_box_size,
        "border": qr_border,
    }

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(qr_config_dict, f, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        logger.error("Fichier de config introuvable: %s", file_path)


def check_qr_code_config_parameters(qr_version, qr_error_correct, qr_box_size, qr_border):
    """Valide et corrige les paramètres de configuration QR."""
    parameter_changed = False

    # version
    if qr_version is not None:
        if str(qr_version).isdigit():
            qr_version = int(qr_version)
        else:
            logger.warning("Paramètre 'version' invalide, initialisé à 1")
            qr_version = 1
            parameter_changed = True
        if qr_version > 40:
            logger.warning("Paramètre 'version' > 40, ramené à 40")
            qr_version = 40
            parameter_changed = True
        elif qr_version < 1:
            logger.warning("Paramètre 'version' < 1, ramené à 1")
            qr_version = 1
            parameter_changed = True

    # error_correction
    if str(qr_error_correct).isdigit():
        qr_error_correct = int(qr_error_correct)
    else:
        logger.warning("Paramètre 'error_correction' invalide, initialisé à 0")
        qr_error_correct = 0
        parameter_changed = True
    if qr_error_correct > 3:
        logger.warning("Paramètre 'error_correction' > 3, ramené à 3")
        qr_error_correct = 3
        parameter_changed = True
    elif qr_error_correct < 0:
        logger.warning("Paramètre 'error_correction' < 0, ramené à 0")
        qr_error_correct = 0
        parameter_changed = True

    # box size
    if str(qr_box_size).isdigit():
        qr_box_size = int(qr_box_size)
    else:
        logger.warning("Paramètre 'box_size' invalide, initialisé à 10")
        qr_box_size = 10
        parameter_changed = True
    if qr_box_size < 1:
        logger.warning("Paramètre 'box_size' < 1, ramené à 10")
        qr_box_size = 10
        parameter_changed = True

    # border
    if str(qr_border).isdigit():
        qr_border = int(qr_border)
    else:
        logger.warning("Paramètre 'border' invalide, initialisé à 4")
        qr_border = 4
        parameter_changed = True
    if qr_border < 4:
        logger.warning("Paramètre 'border' < 4, ramené à 4")
        qr_border = 4
        parameter_changed = True

    if parameter_changed:
        file_path = get_file_path(QR_CONFIG_FILE, DIR_QR_CONFIG)
        if file_path:
            save_qr_config(file_path, qr_version, qr_error_correct, qr_box_size, qr_border)

    return qr_version, qr_error_correct, qr_box_size, qr_border
