import sys
import qrcode
import qrcode.constants

# constante
QR_ERROR_CORRECT_L = qrcode.constants.ERROR_CORRECT_L # 7%
QR_ERROR_CORRECT_M = qrcode.constants.ERROR_CORRECT_M # 15%
QR_ERROR_CORRECT_Q = qrcode.constants.ERROR_CORRECT_Q # 25%
QR_ERROR_CORRECT_H = qrcode.constants.ERROR_CORRECT_H # 30%
# variable à gérer avant la génération
qr_version = None # maximum 40
qr_box_size = 10
qr_border = 4 # minimum 4


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
    img.save("some_file.png")


def qr_code():
    
    generate_qr_code(qr_version,QR_ERROR_CORRECT_L,qr_box_size,qr_border)


qr_code()