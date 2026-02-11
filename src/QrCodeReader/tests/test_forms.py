from django.test import TestCase
from QrCodeReader.forms import (
    QrGenerateUrl, QrGenerateurText, QrGenerateVCard, QrGeneratePhone,
    QrGenerateEmail, QrGenerateSMS, QrGenerateWiFi, QrGenerateLocation,
    QrGenerateEvent, QrLoader
)


class QrGenerateUrlTest(TestCase):
    def test_valid_url(self):
        form = QrGenerateUrl(data={
            'url_to_convert': 'https://example.com',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_url(self):
        form = QrGenerateUrl(data={
            'url_to_convert': 'not-a-url',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_empty_url_allowed(self):
        """url_to_convert est required=False (validé côté serveur)."""
        form = QrGenerateUrl(data={
            'url_to_convert': '',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())


class QrGenerateLocationTest(TestCase):
    def test_valid_location(self):
        form = QrGenerateLocation(data={
            'latitude': 48.8566,
            'longitude': 2.3522,
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_latitude_out_of_range(self):
        form = QrGenerateLocation(data={
            'latitude': 91.0,
            'longitude': 2.3522,
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('latitude', form.errors)

    def test_longitude_out_of_range(self):
        form = QrGenerateLocation(data={
            'latitude': 48.0,
            'longitude': -181.0,
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('longitude', form.errors)

    def test_boundary_values(self):
        form = QrGenerateLocation(data={
            'latitude': 90.0,
            'longitude': 180.0,
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

        form = QrGenerateLocation(data={
            'latitude': -90.0,
            'longitude': -180.0,
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())


class QrGenerateWiFiTest(TestCase):
    def test_valid_wifi(self):
        form = QrGenerateWiFi(data={
            'ssid': 'MyNetwork',
            'password': 'mypassword',
            'encryption': 'WPA',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_no_encryption(self):
        form = QrGenerateWiFi(data={
            'ssid': 'OpenNetwork',
            'password': '',
            'encryption': 'None',
            'qr_error_correction_form': 1,
        })
        # password is required
        self.assertFalse(form.is_valid())


class QrGenerateVCardTest(TestCase):
    def test_valid_vcard(self):
        form = QrGenerateVCard(data={
            'name': 'Jean Dupont',
            'phone': '+33 6 12 34 56 78',
            'email': 'jean@example.com',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_phone(self):
        form = QrGenerateVCard(data={
            'name': 'Jean Dupont',
            'phone': '123',
            'email': 'jean@example.com',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)


class QrGeneratePhoneTest(TestCase):
    def test_valid_phone(self):
        form = QrGeneratePhone(data={
            'phone': '+33 6 12 34 56 78',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_short_phone(self):
        form = QrGeneratePhone(data={
            'phone': '12',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())


class QrGenerateSMSTest(TestCase):
    def test_valid_sms(self):
        form = QrGenerateSMS(data={
            'phone': '+33 6 12 34 56 78',
            'message': 'Hello!',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_phone_in_sms(self):
        form = QrGenerateSMS(data={
            'phone': '12',
            'message': 'Hello!',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())


class QrGenerateEmailTest(TestCase):
    def test_valid_email(self):
        form = QrGenerateEmail(data={
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'Hello',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = QrGenerateEmail(data={
            'email': 'not-an-email',
            'subject': 'Test',
            'message': 'Hello',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class QrGenerateEventTest(TestCase):
    def test_valid_event(self):
        form = QrGenerateEvent(data={
            'title': 'Conference',
            'location': 'Paris',
            'date': '2025-06-15 14:00',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())


class QrLoaderTest(TestCase):
    def test_no_file(self):
        form = QrLoader(data={})
        self.assertFalse(form.is_valid())
