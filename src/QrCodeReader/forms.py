import re
from django import forms
from django.utils.safestring import mark_safe
import utils.qr_code as qr_code

QR_ERROR_CORRECT = (
    (qr_code.QR_ERROR_CORRECT_L, "L 7%"),
    (qr_code.QR_ERROR_CORRECT_M, "M 15%"),
    (qr_code.QR_ERROR_CORRECT_Q, "Q 25%"),
    (qr_code.QR_ERROR_CORRECT_H, "H 30%"),
)

# Constante CSS commune pour les widgets de formulaire
FORM_INPUT_CSS = 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'


def _clean_phone_number(value):
    """Valide et nettoie un numéro de téléphone."""
    if not value:
        return value
    cleaned = re.sub(r'[^\d+\-\s()]', '', value)
    digits_only = re.sub(r'[^\d]', '', cleaned)
    if len(digits_only) < 6:
        raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 6 chiffres.")
    return cleaned


class QRBaseMixin(forms.Form):
    """Mixin pour inclure les champs QR communs à plusieurs formulaires."""
    qr_error_correction_form = forms.ChoiceField(
        choices=QR_ERROR_CORRECT,
        label=mark_safe('Taux de correction d\'erreur <span class="info-tooltip">?<span class="tooltip-text">Capacités maximales selon le niveau :<br>• Faible (7%) : 2,953 caractères<br>• Moyen (15%) : 2,331 caractères<br>• Élevé (25%) : 1,663 caractères<br>• Maximum (30%) : 1,273 caractères<br><br>Plus le niveau est élevé, plus le QR résiste aux dommages, mais moins il peut contenir de données.</span></span>'),
        widget=forms.Select(attrs={
            'class': FORM_INPUT_CSS
        })
    )


class QrGenerateUrl(QRBaseMixin):
    url_to_convert = forms.URLField(
        max_length=500,
        required=False,  # Tous les formulaires sont rendus sur la même page ; validé côté serveur par validate_form_by_type()
        label="Entrez votre URL à convertir",
        widget=forms.URLInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'https://exemple.com'
        })
    )


class QrGenerateurText(QRBaseMixin):
    text_to_convert = forms.CharField(
        required=False,  # Tous les formulaires sont rendus sur la même page ; validé côté serveur par validate_form_by_type()
        label="Entrez votre texte à convertir",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': FORM_INPUT_CSS,
            'placeholder': 'Entrez votre texte ici...'
        })
    )


class QrGenerateVCard(QRBaseMixin):
    name = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'Nom complet'
        })
    )
    phone = forms.CharField(
        label="Téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': '+33 6 12 34 56 78'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'email@exemple.com'
        })
    )

    def clean_phone(self):
        return _clean_phone_number(self.cleaned_data.get('phone', ''))


class QrGeneratePhone(QRBaseMixin):
    phone = forms.CharField(
        label="Numéro de téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': '+33 6 12 34 56 78'
        })
    )

    def clean_phone(self):
        return _clean_phone_number(self.cleaned_data.get('phone', ''))


class QrGenerateEmail(QRBaseMixin):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'email@exemple.com'
        })
    )
    subject = forms.CharField(
        label="Sujet",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'Sujet de l\'email'
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': FORM_INPUT_CSS,
            'placeholder': 'Entrez votre message ici...'
        })
    )


class QrGenerateSMS(QRBaseMixin):
    phone = forms.CharField(
        label="Numéro de téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': '+33 6 12 34 56 78'
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': FORM_INPUT_CSS,
            'placeholder': 'Entrez votre message ici...'
        })
    )

    def clean_phone(self):
        return _clean_phone_number(self.cleaned_data.get('phone', ''))


class QrGenerateWiFi(QRBaseMixin):
    ssid = forms.CharField(
        label="Nom du réseau (SSID)",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'Mon_WiFi'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'Mot de passe du WiFi'
        })
    )
    encryption = forms.ChoiceField(
        label="Type de cryptage",
        choices=[('WPA', 'WPA'), ('WEP', 'WEP'), ('None', 'Aucun')],
        widget=forms.Select(attrs={
            'class': FORM_INPUT_CSS
        })
    )


class QrGenerateLocation(QRBaseMixin):
    latitude = forms.FloatField(
        label="Latitude",
        min_value=-90.0,
        max_value=90.0,
        widget=forms.NumberInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': '48.8566',
            'step': 'any',
        })
    )
    longitude = forms.FloatField(
        label="Longitude",
        min_value=-180.0,
        max_value=180.0,
        widget=forms.NumberInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': '2.3522',
            'step': 'any',
        })
    )


class QrGenerateEvent(QRBaseMixin):
    title = forms.CharField(
        label="Titre de l'événement",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'Nom de l\'événement'
        })
    )
    location = forms.CharField(
        label="Lieu",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': FORM_INPUT_CSS,
            'placeholder': 'Adresse ou lieu de l\'événement'
        })
    )
    date = forms.DateTimeField(
        label="Date et heure",
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': FORM_INPUT_CSS
        })
    )


class QrLoader(forms.Form):
    qr_img = forms.ImageField(
        label="Sélectionnez une image de QR code",
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': FORM_INPUT_CSS,
            'aria-label': 'Sélectionnez une image de QR code à décoder',
        })
    )
