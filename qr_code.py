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

# fichier
p = Path.cwd()
files = p / "QR" / "some_file.png"


def get_arguments():
    arguments = sys.argv[1:]


def generate_qr_code(qr_version,qr_error_correction,qr_box_size,qr_border):
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qr_error_correction,
        box_size=qr_box_size,
        border=qr_border,
    )
    qr.add_data('Some data')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    ## to do
    # gestion de  fichiers nom ect..
    
    img.save(files)


def qr_code():
    
    generate_qr_code(qr_version,QR_ERROR_CORRECT_L,qr_box_size,qr_border)
    read_qr_code()

def read_qr_code():
    # read the QRCODE image
    img = cv2.imread("site.png")
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    # detect and decode
    data, bbox, straight_qrcode = detector.detectAndDecode(img) 
    # if there is a QR code
    if bbox is not None:
        print(f"QRCode data:\n{data}")
        # display the image with lines
        # length of bounding box
        n_lines = len(bbox)
        for i in range(n_lines):
            # draw all lines
            point1 = tuple(bbox[i][0])
            point2 = tuple(bbox[(i+1) % n_lines][0])
            cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)

qr_code()