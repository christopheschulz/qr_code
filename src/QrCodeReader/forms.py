from django import forms
import utils.qr_code as qr_code

QR_ERROR_CORRRECT = (
    (qr_code.QR_ERROR_CORRECT_L, "L 7%"),
    (qr_code.QR_ERROR_CORRECT_M, "M 15%"),
    (qr_code.QR_ERROR_CORRECT_Q, "Q 25%"),
    (qr_code.QR_ERROR_CORRECT_H, "H 30%"),
)

QR_BOX_SIZE = (
    (50, "50x50"),
    (100, "100x100"),
    (150, "150x150"),
    (200, "200x200"),
    (250, "250x250"),
    (500, "500x500"),
)


class QRBaseMixin(forms.Form):
    """Mixin pour inclure les champs QR communs à plusieurs formulaires."""
    qr_error_correction_form = forms.ChoiceField(
        choices=QR_ERROR_CORRRECT, label="Taux de correction d'erreur"
    )
    qr_box_size_form = forms.ChoiceField(
        choices=QR_BOX_SIZE, label="Taille QR Code"
    )


class QrGenerateUrl(QRBaseMixin):
    url_to_convert = forms.URLField(max_length=50, required=True, label="Entrez votre URL à convertir")


class QrGenerateurText(QRBaseMixin):
    text_to_convert = forms.CharField(
    required=True, 
    label="Entrez votre texte à convertir",
    widget=forms.Textarea(attrs={
        'rows': 4,
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Entrez votre texte ici...'
    })
)


class QrGenerateVCard(QRBaseMixin):
    name = forms.CharField(label="Nom", max_length=100)
    phone = forms.CharField(label="Téléphone", max_length=20)
    email = forms.EmailField(label="Email")


class QrGeneratePhone(QRBaseMixin):
    phone = forms.CharField(label="Numéro de téléphone", max_length=20)


class QrGenerateEmail(QRBaseMixin):
    email = forms.EmailField(label="Email")
    subject = forms.CharField(label="Sujet", max_length=100)
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'w-full p-2 border rounded',
            'placeholder': 'Entrez votre message ici...'
    }))


class QrGenerateSMS(QRBaseMixin):
    phone = forms.CharField(label="Numéro de téléphone", max_length=20)
    message = forms.CharField(
        label="Message", 
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'w-full p-2 border rounded',
            'placeholder': 'Entrez votre message ici...'
    }))


class QrGenerateWiFi(QRBaseMixin):
    ssid = forms.CharField(label="Nom du réseau (SSID)", max_length=100)
    password = forms.CharField(label="Mot de passe", max_length=100, widget=forms.PasswordInput)
    encryption = forms.ChoiceField(label="Type de cryptage", choices=[('WPA', 'WPA'), ('WEP', 'WEP'), ('None', 'Aucun')])


class QrGenerateLocation(QRBaseMixin):
    latitude = forms.CharField(label="Latitude")
    longitude = forms.CharField(label="Longitude")


class QrGenerateEvent(QRBaseMixin):
    title = forms.CharField(label="Titre de l'événement", max_length=100)
    location = forms.CharField(label="Lieu", max_length=200)
    date = forms.DateTimeField(label="Date et heure", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class QrLoader(forms.Form):
    qr_img = forms.ImageField(label="", 
                              widget=forms.FileInput(attrs={'accept': 'image/*'}))
