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
