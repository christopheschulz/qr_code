import os
import base64
import hashlib
import qrcode
from io import BytesIO
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from .forms import (
    QrGenerateUrl, QrGenerateurText, QrGenerateVCard, QrGeneratePhone,
    QrGenerateEmail, QrGenerateSMS, QrGenerateWiFi, QrGenerateLocation,
    QrGenerateEvent, QrLoader
)
from utils.qr_code import generate_qr_code, get_qr_code_img_file_path, read_qr_code

def generate_qr_code_view(request):
    form_type = request.POST.get("form_type", "url")
    qr_code_base64 = None
    session_key = 'last_qr_hash'

    # Stocker les classes de formulaire
    forms = {
        "url": QrGenerateUrl,
        "vcard": QrGenerateVCard,
        "phone": QrGeneratePhone,
        "text": QrGenerateurText,
        "email": QrGenerateEmail,
        "sms": QrGenerateSMS,
        "wifi": QrGenerateWiFi,
        "location": QrGenerateLocation,
        "event": QrGenerateEvent,
    }

    # Instances des formulaires pour affichage
    form_instances = {key: form_class() for key, form_class in forms.items()}

    if request.method == "POST":
        form_class = forms.get(form_type)
        if form_class:
            form = form_class(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                qr_error_correction = int(data.get("qr_error_correction_form", 1))
                qr_box_size = int(data.get("qr_box_size_form", 10))
                qr_data = ""

                # Construction des données à encoder
                if form_type == "url":
                    qr_data = data['url_to_convert']
                elif form_type == "vcard":
                    qr_data = f"BEGIN:VCARD\nFN:{data['name']}\nTEL:{data['phone']}\nEMAIL:{data['email']}\nEND:VCARD"
                elif form_type == "phone":
                    qr_data = f"tel:{data['phone']}"
                elif form_type == "text":
                    qr_data = data['text_to_convert']
                elif form_type == "email":
                    qr_data = f"mailto:{data['email']}?subject={data['subject']}&body={data['message']}"
                elif form_type == "sms":
                    qr_data = f"sms:{data['phone']}?body={data['message']}"
                elif form_type == "wifi":
                    qr_data = f"WIFI:T:{data['encryption']};S:{data['ssid']};P:{data['password']};;"
                elif form_type == "location":
                    qr_data = f"geo:{data['latitude']},{data['longitude']}"
                elif form_type == "event":
                    qr_data = f"BEGIN:VEVENT\nSUMMARY:{data['title']}\nLOCATION:{data['location']}\nDTSTART:{data['date']}\nEND:VEVENT"

                # Générer une signature unique (facultatif si pas de cache session)
                qr_unique_str = f"{qr_data}|{qr_error_correction}|{qr_box_size}"
                qr_hash = hashlib.md5(qr_unique_str.encode()).hexdigest()

                # Génération du QR Code en mémoire
                qr = qrcode.QRCode(
                    version=None,
                    error_correction=qr_error_correction,
                    box_size=qr_box_size,
                    border=4
                )
                qr.add_data(qr_data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")

                # Encodage en base64 directement
                qr_code_base64 = f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

            else:
                print(f"Formulaire invalide: {form.errors}")
        else:
            print(f"Type de formulaire inconnu: {form_type}")
    else:
        print("Requête GET reçue")

    return render(request, "qr_generator.html", {
        "forms": form_instances,
        "image_url": qr_code_base64
    })


def qr_reader(request):
    qr_reader_form = QrLoader()
    image_url = ""
    result = ""

    if request.method == "POST":
        qr_reader_form = QrLoader(request.POST, request.FILES)
        if qr_reader_form.is_valid():
            qr_img = qr_reader_form.cleaned_data['qr_img']
            if not qr_img.content_type.startswith('image/'):
                qr_reader_form.add_error('qr_img', 'Le fichier téléchargé n\'est pas une image valide.')
            else:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
                os.makedirs(upload_dir, exist_ok=True)

                file_path = os.path.join(upload_dir, str(qr_img))
                with open(file_path, 'wb+') as destination:
                    for chunk in qr_img.chunks():
                        destination.write(chunk)

                image_url = f"{settings.MEDIA_URL}qr_codes/{str(qr_img)}"
                print(image_url)
                print(file_path)

                result = read_qr_code(file_path)
                print(result)

                if not result:
                    result = "Ce fichier n'est pas un QR Code"

    return render(request, "qr_reader.html", {'form': qr_reader_form, 'result': result, 'image_url': image_url})


def qr_history(request):
    return render(request, "qr_history.html")


def about(request):
    return render(request, "about.html")
