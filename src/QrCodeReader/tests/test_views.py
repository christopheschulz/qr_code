import io
import qrcode
from django.test import TestCase, Client
from django.urls import reverse


class GeneratorViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_generator(self):
        resp = self.client.get(reverse('generate_qr_code_view'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Générateur de QR Code')

    def test_post_url_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'url',
            'url_to_convert': 'https://example.com',
            'qr_error_correction_form': 1,
        })
        # PRG pattern: should redirect
        self.assertEqual(resp.status_code, 302)

    def test_post_url_then_get_shows_qr(self):
        self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'url',
            'url_to_convert': 'https://example.com',
            'qr_error_correction_form': 1,
        })
        resp = self.client.get(reverse('generate_qr_code_view'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'data:image/png;base64,')

    def test_post_text_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'text',
            'text_to_convert': 'Hello World',
            'qr_error_correction_form': 0,
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_wifi_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'wifi',
            'ssid': 'MyNetwork',
            'password': 'password123',
            'encryption': 'WPA',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_invalid_url(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'url',
            'url_to_convert': 'not-a-url',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Erreurs de validation')

    def test_post_empty_required_field(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'url',
            'url_to_convert': '',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ce champ est requis')

    def test_ajax_request(self):
        resp = self.client.post(
            reverse('generate_qr_code_view'),
            {
                'form_type': 'text',
                'text_to_convert': 'Ajax test',
                'qr_error_correction_form': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertIn('data:image/png;base64,', data['image_url'])

    def test_unknown_form_type(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'unknown',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 200)


class ReaderViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_reader(self):
        resp = self.client.get(reverse('qrreader'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Lecteur de QR Code')

    def test_upload_valid_qr(self):
        # Generate a real QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data('https://example.com')
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        buf.name = 'test_qr.png'

        resp = self.client.post(reverse('qrreader'), {
            'form_type': 'file',
            'qr_img': buf,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'https://example.com')

    def test_upload_non_image(self):
        fake_file = io.BytesIO(b'not an image')
        fake_file.name = 'test.txt'

        resp = self.client.post(reverse('qrreader'), {
            'form_type': 'file',
            'qr_img': fake_file,
        })
        self.assertEqual(resp.status_code, 200)


# ============================================================
# Tests de sécurité : emojis, données trop volumineuses, pas de 500
# ============================================================

class GeneratorSecurityTest(TestCase):
    """Vérifie que les entrées invalides donnent des erreurs propres et jamais une 500."""

    def setUp(self):
        self.client = Client()

    # --- Emojis rejetés (pas de page 500) ---

    def test_post_emoji_in_text_no_500(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'text',
            'text_to_convert': 'Hello 😀',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'Server Error')
        self.assertContains(resp, 'emojis')

    def test_post_emoji_in_vcard_no_500(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'vcard',
            'name': 'Jean 🎉',
            'phone': '+33612345678',
            'email': 'jean@example.com',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'emojis')

    def test_post_emoji_in_wifi_no_500(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'wifi',
            'ssid': 'WiFi🔥',
            'password': 'pass123',
            'encryption': 'WPA',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'emojis')

    # --- Emojis rejetés via AJAX ---

    def test_ajax_emoji_returns_error_json(self):
        resp = self.client.post(
            reverse('generate_qr_code_view'),
            {
                'form_type': 'text',
                'text_to_convert': 'Test 🎉🔥',
                'qr_error_correction_form': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertFalse(data['success'])
        self.assertTrue(len(data['errors']) > 0)
        self.assertTrue(any('emojis' in e for e in data['errors']))

    # --- Données trop volumineuses ---

    def test_oversized_text_shows_capacity_error(self):
        """Texte > capacité QR au niveau H (1273 octets) affiche une erreur, pas une 500."""
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'text',
            'text_to_convert': 'A' * 1300,
            'qr_error_correction_form': 3,  # H = max 1273 octets
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'volumineuses')

    def test_ajax_oversized_text_returns_error_json(self):
        resp = self.client.post(
            reverse('generate_qr_code_view'),
            {
                'form_type': 'text',
                'text_to_convert': 'A' * 1300,
                'qr_error_correction_form': 3,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertFalse(data['success'])
        self.assertTrue(any('volumineuses' in e for e in data['errors']))

    # --- Tous les types de QR codes génèrent correctement ---

    def test_post_vcard_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'vcard',
            'name': 'Jean Dupont',
            'phone': '+33612345678',
            'email': 'jean@example.com',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_phone_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'phone',
            'phone': '+33612345678',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_email_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'email',
            'email': 'test@example.com',
            'subject': 'Bonjour',
            'message': 'Hello world',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_sms_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'sms',
            'phone': '+33612345678',
            'message': 'Bonjour',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_location_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'location',
            'latitude': 48.8566,
            'longitude': 2.3522,
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 302)

    def test_post_event_qr_code(self):
        resp = self.client.post(reverse('generate_qr_code_view'), {
            'form_type': 'event',
            'title': 'Conference',
            'location': 'Paris',
            'date': '2025-06-15 14:00',
            'qr_error_correction_form': 1,
        })
        self.assertEqual(resp.status_code, 302)

    # --- AJAX pour tous les types ---

    def test_ajax_vcard_success(self):
        resp = self.client.post(
            reverse('generate_qr_code_view'),
            {
                'form_type': 'vcard',
                'name': 'Jean Dupont',
                'phone': '+33612345678',
                'email': 'jean@example.com',
                'qr_error_correction_form': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertIn('data:image/png;base64,', data['image_url'])

    def test_ajax_wifi_success(self):
        resp = self.client.post(
            reverse('generate_qr_code_view'),
            {
                'form_type': 'wifi',
                'ssid': 'MonReseau',
                'password': 'motdepasse',
                'encryption': 'WPA',
                'qr_error_correction_form': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        self.assertTrue(data['success'])

    # --- Accents français acceptés (pas de faux positif) ---

    def test_french_accents_generate_qr(self):
        resp = self.client.post(
            reverse('generate_qr_code_view'),
            {
                'form_type': 'text',
                'text_to_convert': 'Rendez-vous au café à côté de la bibliothèque',
                'qr_error_correction_form': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        self.assertTrue(data['success'])


class StaticPagesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_page(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)

    def test_privacy_page(self):
        resp = self.client.get(reverse('privacy'))
        self.assertEqual(resp.status_code, 200)

    def test_mentions_legales_page(self):
        resp = self.client.get(reverse('mentions_legales'))
        self.assertEqual(resp.status_code, 200)

    def test_health_check(self):
        resp = self.client.get(reverse('health_check'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'ok')

    def test_robots_txt(self):
        resp = self.client.get(reverse('robots_txt'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'User-agent')

    def test_sitemap(self):
        resp = self.client.get(reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<?xml')
