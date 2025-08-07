from django import forms
from django.utils.safestring import mark_safe
import utils.qr_code as qr_code

QR_ERROR_CORRRECT = (
    (qr_code.QR_ERROR_CORRECT_L, "L 7%"),
    (qr_code.QR_ERROR_CORRECT_M, "M 15%"),
    (qr_code.QR_ERROR_CORRECT_Q, "Q 25%"),
    (qr_code.QR_ERROR_CORRECT_H, "H 30%"),
)



class QRBaseMixin(forms.Form):
    """Mixin pour inclure les champs QR communs à plusieurs formulaires."""
    qr_error_correction_form = forms.ChoiceField(
        choices=QR_ERROR_CORRRECT, 
        label=mark_safe("""Taux de correction d'erreur <span class="tooltip">
            <span class="tooltip-trigger">?</span>
            <div class="tooltip-content">
                <div class="font-semibold mb-2">💡 Capacités maximales selon le niveau :</div>
                <div class="space-y-1 text-sm">
                    <div><strong>Faible (7%)</strong> : 2,953 caractères • 7,089 chiffres</div>
                    <div><strong>Moyen (15%)</strong> : 2,331 caractères • 5,596 chiffres</div>
                    <div><strong>Élevé (25%)</strong> : 1,663 caractères • 3,993 chiffres</div>
                    <div><strong>Maximum (30%)</strong> : 1,273 caractères • 3,057 chiffres</div>
                </div>
                <div class="text-xs mt-2 opacity-80">
                    ⚖️ Plus le niveau est élevé, plus le QR résiste aux dommages, mais moins il peut contenir de données.
                </div>
            </div>
        </span>"""),
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )


class QrGenerateUrl(QRBaseMixin):
    url_to_convert = forms.URLField(
        max_length=500, 
        required=False,  # Géré dynamiquement par JavaScript
        label="Entrez votre URL à convertir",
        widget=forms.URLInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'https://exemple.com'
        })
    )


class QrGenerateurText(QRBaseMixin):
    text_to_convert = forms.CharField(
        required=False,  # Géré dynamiquement par JavaScript
        label="Entrez votre texte à convertir",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Entrez votre texte ici...'
        })
    )


class QrGenerateVCard(QRBaseMixin):
    name = forms.CharField(
        label="Nom", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Nom complet'
        })
    )
    phone = forms.CharField(
        label="Téléphone", 
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '+33 6 12 34 56 78'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'email@exemple.com'
        })
    )


class QrGeneratePhone(QRBaseMixin):
    phone = forms.CharField(
        label="Numéro de téléphone", 
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '+33 6 12 34 56 78'
        })
    )


class QrGenerateEmail(QRBaseMixin):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'email@exemple.com'
        })
    )
    subject = forms.CharField(
        label="Sujet", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Sujet de l\'email'
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Entrez votre message ici...'
        })
    )


class QrGenerateSMS(QRBaseMixin):
    phone = forms.CharField(
        label="Numéro de téléphone", 
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '+33 6 12 34 56 78'
        })
    )
    message = forms.CharField(
        label="Message", 
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Entrez votre message ici...'
        })
    )


class QrGenerateWiFi(QRBaseMixin):
    ssid = forms.CharField(
        label="Nom du réseau (SSID)", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Mon_WiFi'
        })
    )
    password = forms.CharField(
        label="Mot de passe", 
        max_length=100, 
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Mot de passe du WiFi'
        })
    )
    encryption = forms.ChoiceField(
        label="Type de cryptage", 
        choices=[('WPA', 'WPA'), ('WEP', 'WEP'), ('None', 'Aucun')],
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )


class QrGenerateLocation(QRBaseMixin):
    latitude = forms.CharField(
        label="Latitude",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '48.8566'
        })
    )
    longitude = forms.CharField(
        label="Longitude",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '2.3522'
        })
    )


class QrGenerateEvent(QRBaseMixin):
    title = forms.CharField(
        label="Titre de l'événement", 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Nom de l\'événement'
        })
    )
    location = forms.CharField(
        label="Lieu", 
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Adresse ou lieu de l\'événement'
        })
    )
    date = forms.DateTimeField(
        label="Date et heure", 
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )


class QrLoader(forms.Form):
    qr_img = forms.ImageField(
        label="", 
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )
