import io
import qrcode
from django.test import TestCase
from utils.qr_code import (
    read_qr_code_from_bytes,
    check_qr_code_config_parameters,
)


class ReadQrCodeFromBytesTest(TestCase):
    def _make_qr_bytes(self, data):
        """Génère les bytes PNG d'un QR code contenant `data`."""
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    def test_valid_qr_code(self):
        data = 'https://example.com'
        img_bytes = self._make_qr_bytes(data)
        result = read_qr_code_from_bytes(img_bytes)
        self.assertEqual(result, data)

    def test_text_qr_code(self):
        data = 'Hello World'
        img_bytes = self._make_qr_bytes(data)
        result = read_qr_code_from_bytes(img_bytes)
        self.assertEqual(result, data)

    def test_invalid_image(self):
        result = read_qr_code_from_bytes(b'not an image')
        self.assertIsNone(result)

    def test_empty_bytes(self):
        result = read_qr_code_from_bytes(b'')
        self.assertIsNone(result)

    def test_plain_image_no_qr(self):
        """Une image blanche ne contient pas de QR code."""
        from PIL import Image
        img = Image.new('RGB', (100, 100), 'white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        result = read_qr_code_from_bytes(buf.getvalue())
        self.assertIsNone(result)


class CheckQrConfigParametersTest(TestCase):
    def test_valid_parameters(self):
        v, e, b, bo = check_qr_code_config_parameters(1, 1, 10, 4)
        self.assertEqual(v, 1)
        self.assertEqual(e, 1)
        self.assertEqual(b, 10)
        self.assertEqual(bo, 4)

    def test_version_too_high(self):
        v, e, b, bo = check_qr_code_config_parameters(50, 1, 10, 4)
        self.assertEqual(v, 40)

    def test_version_too_low(self):
        v, e, b, bo = check_qr_code_config_parameters(0, 1, 10, 4)
        self.assertEqual(v, 1)

    def test_version_none(self):
        v, e, b, bo = check_qr_code_config_parameters(None, 1, 10, 4)
        self.assertIsNone(v)

    def test_error_correction_too_high(self):
        v, e, b, bo = check_qr_code_config_parameters(1, 5, 10, 4)
        self.assertEqual(e, 3)

    def test_error_correction_too_low(self):
        v, e, b, bo = check_qr_code_config_parameters(1, -1, 10, 4)
        self.assertEqual(e, 0)

    def test_box_size_too_low(self):
        v, e, b, bo = check_qr_code_config_parameters(1, 1, 0, 4)
        self.assertEqual(b, 10)

    def test_border_too_low(self):
        v, e, b, bo = check_qr_code_config_parameters(1, 1, 10, 2)
        self.assertEqual(bo, 4)

    def test_invalid_string_parameters(self):
        v, e, b, bo = check_qr_code_config_parameters('abc', 'xyz', 'def', 'ghi')
        self.assertEqual(v, 1)
        self.assertEqual(e, 0)
        self.assertEqual(b, 10)
        self.assertEqual(bo, 4)
