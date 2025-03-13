from django import forms

QR_ERROR_CORRRECT =(
("QR_ERROR_CORRRECT_L","L 7%"),
("QR_ERROR_CORRRECT_M","M 15%"),
("QR_ERROR_CORRRECT_Q","Q 25%"),
("QR_ERROR_CORRRECT_H","H 30%")
)


QR_BOX_SIZE = (
    ("box50","50x50"),
    ("box100","100x100"),
    ("box150","150x150"),
    ("box200","200x200"),
    ("box250","250x250"),
    ("box500","500x500"),
)


class QrReaderForm(forms.Form):
    qr_error_correction_form = forms.ChoiceField(choices=QR_ERROR_CORRRECT)
    qr_box_size_form = forms.ChoiceField(choices=QR_BOX_SIZE)
    text_to_convert_form = forms.CharField(required=True)