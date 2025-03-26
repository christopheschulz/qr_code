import os
import base64
import hashlib
import qrcode
import cv2
import numpy as np
from io import BytesIO
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
from .forms import (
    QrGenerateUrl, QrGenerateurText, QrGenerateVCard, QrGeneratePhone,
    QrGenerateEmail, QrGenerateSMS, QrGenerateWiFi, QrGenerateLocation,
    QrGenerateEvent, QrLoader
)
from utils.qr_code import generate_qr_code, get_qr_code_img_file_path, read_qr_code
import json

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


def read_qr_with_cv2(img_data):
    try:
        # Convertir les bytes en image OpenCV
        np_arr = np.asarray(bytearray(img_data), dtype=np.uint8)
        img_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img_cv2 is None:
            raise ValueError("Impossible de décoder l'image (image corrompue)")

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img_cv2)

        if bbox is not None and data:
            return data
        return None
    except Exception as e:
        print("Erreur de lecture QR :", e)
        return None


def qr_reader(request):
    qr_reader_form = QrLoader()
    result = ""
    image_base64 = ""

    if request.method == "POST":
        qr_reader_form = QrLoader(request.POST, request.FILES)
        if qr_reader_form.is_valid():
            qr_img = qr_reader_form.cleaned_data['qr_img']

            if not qr_img.content_type.startswith('image/'):
                qr_reader_form.add_error('qr_img', '❌ Le fichier téléchargé n\'est pas une image valide.')
                return render(request, "qr_reader.html", {'form': qr_reader_form, 'result': '', 'image_url': ''})

            if qr_img.size > 4 * 1024 * 1024:
                qr_reader_form.add_error('qr_img', '❌ Le fichier est trop volumineux (4 Mo max).')
                return render(request, "qr_reader.html", {'form': qr_reader_form, 'result': '', 'image_url': ''})

            # Lecture des données binaires
            img_data = qr_img.read()

            # ✅ Appel de ta fonction utilitaire
            result = read_qr_with_cv2(img_data)
            if not result:
                qr_reader_form.add_error('qr_img', "❌ Ce fichier n'est pas un QR Code valide ou est corrompu.")
                return render(request, "qr_reader.html", {'form': qr_reader_form, 'result': result, 'image_url': ''})

            # Encodage Base64 pour l'affichage
            image_base64 = base64.b64encode(img_data).decode('utf-8')

    return render(request, "qr_reader.html", {
        'form': qr_reader_form,
        'result': result,
        'image_url': image_base64
    })



def qr_history(request):
    return render(request, "qr_history.html")


def about(request):
    return render(request, "about.html")

def privacy_policy(request):
    context = {
        'current_date': datetime.now()
    }
    return render(request, 'privacy.html', context)
