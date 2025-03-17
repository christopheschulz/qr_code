import os
import base64
from io import BytesIO
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from .forms import (
    QrGenerateUrl, QrGenerateurText, QrGenerateVCard, QrGeneratePhone,
    QrGenerateEmail, QrGenerateSMS, QrGenerateWiFi, QrGenerateLocation,
    QrGenerateEvent,QrLoader
)
from utils.qr_code import generate_qr_code, get_qr_code_img_file_path,read_qr_code  # Import de tes fonctions QR

def generate_qr_code_view(request):
    form_type = request.POST.get("form_type", "url")
    qr_code_base64 = None

    forms = {
        "url": QrGenerateUrl(),
        "vcard": QrGenerateVCard(),
        "phone": QrGeneratePhone(),
        "text": QrGenerateurText(),
        "email": QrGenerateEmail(),
        "sms": QrGenerateSMS(),
        "wifi": QrGenerateWiFi(),
        "location": QrGenerateLocation(),
        "event": QrGenerateEvent(),
    }

    form = forms.get(form_type)

    if request.method == "POST":
        form = forms.get(form_type)(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            qr_data = ""

            # Récupération des valeurs du formulaire
            qr_error_correction = int(data.get("qr_error_correction_form", 1))  # Valeur par défaut : 1 (M)
            qr_box_size = int(data.get("qr_box_size_form", 10))  # Valeur par défaut : 10

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

            # Génération du QR code avec les valeurs du formulaire
            generate_qr_code(
                qr_text=qr_data,
                qr_version=None,  # Auto-adaptation
                qr_error_correction=qr_error_correction,
                qr_box_size=qr_box_size,
                qr_border=4  # Valeur par défaut
            )

            # Charger le fichier généré et le convertir en base64
            qr_file_path = get_qr_code_img_file_path()
            if Path(qr_file_path).exists():
                with open(qr_file_path, "rb") as qr_file:
                    qr_code_base64 = base64.b64encode(qr_file.read()).decode()

    # 🔥 Ajouter une gestion pour les requêtes GET
    return render(request, "qr_generator.html", {
        "form": form,
        "forms": forms,
        "qr_code_base64": qr_code_base64
    })

def qr_reader(request):
    
    if request.method == "POST":
        qr_reader_form = QrLoader(request.POST, request.FILES)
        if qr_reader_form.is_valid():
            qr_img = qr_reader_form.cleaned_data['qr_img']

            upload_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, str(qr_img))
            
            with open(file_path, 'wb+') as destination:
                for chunk in qr_img.chunks():
                    destination.write(chunk)
            image_url = f"{settings.MEDIA_URL}qr_codes/{str(qr_img)}"

            result = read_qr_code(file_path)
            
            if not result:
                result = "Ce fichier n'est pas un QR Code"
            
    else:
        qr_reader_form = QrLoader()
        image_url = ""
        result = ""
    
    return render(request,"qr_reader.html",{'form' : qr_reader_form, 'result' : result, 'image_url': image_url})


def qr_history(request):
    return render(request,"qr_history.html")


def about(request):
    return render(request,"about.html")