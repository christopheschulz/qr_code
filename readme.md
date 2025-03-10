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