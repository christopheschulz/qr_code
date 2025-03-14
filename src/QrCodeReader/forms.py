from django import forms
import qr_code

QR_ERROR_CORRRECT =(
(qr_code.QR_ERROR_CORRECT_L,"L 7%"),
(qr_code.QR_ERROR_CORRECT_M,"M 15%"),
(qr_code.QR_ERROR_CORRECT_Q,"Q 25%"),
(qr_code.QR_ERROR_CORRECT_H,"H 30%")
)


QR_BOX_SIZE = (
    (50,"50x50"),
    (100,"100x100"),
    (150,"150x150"),
    (200,"200x200"),
    (250,"250x250"),
    (500,"500x500"),
)


class QrGenerateForm(forms.Form):
    qr_error_correction_form = forms.ChoiceField(choices=QR_ERROR_CORRRECT,label="Taux de correction d'erreur")
    qr_box_size_form = forms.ChoiceField(choices=QR_BOX_SIZE,label="Taille QR Code")
    text_to_convert_form = forms.CharField(max_length= 50, required=True, widget=forms.Textarea,label="Entrez votre texte à convertir")
