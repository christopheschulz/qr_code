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


# ============================================================
# Tests de validation des caractères (rejet hors Latin-1)
# ============================================================

class CharacterValidationTest(TestCase):
    """Vérifie que les emojis et caractères non-Latin-1 sont rejetés
    sur tous les types de formulaires via QRBaseMixin.clean()."""

    def test_emoji_rejected_in_text(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'Bonjour 😀',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_emoji_rejected_in_url(self):
        form = QrGenerateUrl(data={
            'url_to_convert': 'https://example.com/😀',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_emoji_rejected_in_vcard_name(self):
        form = QrGenerateVCard(data={
            'name': 'Jean 🎉 Dupont',
            'phone': '+33 6 12 34 56 78',
            'email': 'jean@example.com',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_emoji_rejected_in_wifi_ssid(self):
        form = QrGenerateWiFi(data={
            'ssid': 'WiFi🔥',
            'password': 'password',
            'encryption': 'WPA',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_emoji_rejected_in_sms_message(self):
        form = QrGenerateSMS(data={
            'phone': '+33 6 12 34 56 78',
            'message': 'Hello 👍',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_emoji_rejected_in_email_subject(self):
        form = QrGenerateEmail(data={
            'email': 'test@example.com',
            'subject': 'Sujet 🚀',
            'message': 'Hello',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_emoji_rejected_in_event_title(self):
        form = QrGenerateEvent(data={
            'title': 'Concert 🎵',
            'location': 'Paris',
            'date': '2025-06-15 14:00',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_chinese_characters_rejected(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'Hello 你好世界',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_arabic_characters_rejected(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'Bienvenue مرحبا',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_cyrillic_characters_rejected(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'Привет мир',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())

    def test_french_accents_accepted(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'Café résumé naïve àéîõü ç',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_german_characters_accepted(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'über Straße Mädchen',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_latin1_symbols_accepted(self):
        form = QrGenerateurText(data={
            'text_to_convert': '©2024 ®marque £50 ¥100 §1',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_error_message_is_user_friendly(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'Test 😀',
            'qr_error_correction_form': 1,
        })
        form.is_valid()
        all_errors = form.errors.get('__all__', [])
        self.assertTrue(any('emojis' in str(e) for e in all_errors))


# ============================================================
# Tests des limites max_length
# ============================================================

class MaxLengthValidationTest(TestCase):
    """Vérifie que les champs sans max_length d'origine sont maintenant limités."""

    def test_text_max_length_respected(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'A' * 2953,
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_text_exceeds_max_length(self):
        form = QrGenerateurText(data={
            'text_to_convert': 'A' * 2954,
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('text_to_convert', form.errors)

    def test_email_message_max_length_respected(self):
        form = QrGenerateEmail(data={
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'A' * 2000,
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_email_message_exceeds_max_length(self):
        form = QrGenerateEmail(data={
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'A' * 2001,
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_sms_message_max_length_respected(self):
        form = QrGenerateSMS(data={
            'phone': '+33 6 12 34 56 78',
            'message': 'A' * 1600,
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_sms_message_exceeds_max_length(self):
        form = QrGenerateSMS(data={
            'phone': '+33 6 12 34 56 78',
            'message': 'A' * 1601,
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)


# ============================================================
# Tests du nettoyage des numéros de téléphone (cas limites)
# ============================================================

class PhoneCleaningTest(TestCase):
    """Vérifie le nettoyage et la validation des numéros de téléphone."""

    def test_phone_with_special_chars_cleaned(self):
        form = QrGeneratePhone(data={
            'phone': '+33 (0)6-12-34-56-78',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())
        # Les caractères spéciaux injectés doivent être nettoyés
        self.assertNotIn('!', form.cleaned_data.get('phone', ''))

    def test_phone_strips_injected_chars(self):
        """Les caractères non-téléphone sont supprimés."""
        form = QrGeneratePhone(data={
            'phone': '+33;612345678',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())
        self.assertNotIn(';', form.cleaned_data['phone'])

    def test_phone_exactly_6_digits(self):
        form = QrGeneratePhone(data={
            'phone': '123456',
            'qr_error_correction_form': 1,
        })
        self.assertTrue(form.is_valid())

    def test_phone_5_digits_rejected(self):
        form = QrGeneratePhone(data={
            'phone': '12345',
            'qr_error_correction_form': 1,
        })
        self.assertFalse(form.is_valid())
