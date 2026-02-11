import os
import base64
import hashlib
import qrcode
import qrcode.constants
import cv2
import numpy as np
from io import BytesIO
from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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

def validate_form_by_type(form, form_type):
    """Validation personnalisée selon le type de formulaire actif"""
    if not form.is_valid():
        return False
    
    data = form.cleaned_data
    
    # Vérifier les champs requis selon le type
    required_fields = {
        'url': ['url_to_convert'],
        'text': ['text_to_convert'],
        'email': ['email'],
        'phone': ['phone'],
        'sms': ['phone', 'message'],
        'wifi': ['ssid', 'password'],
        'vcard': ['name'],
        'location': ['latitude', 'longitude'],
        'event': ['title', 'date']
    }
    
    fields_to_check = required_fields.get(form_type, [])
    
    for field_name in fields_to_check:
        field_value = data.get(field_name)
        if not field_value or (isinstance(field_value, str) and not field_value.strip()):
            form.add_error(field_name, "Ce champ est requis.")
            return False
    
    return True

def get_qr_capacity_info(error_correction_level):
    """Retourne les informations de capacité selon le niveau de correction d'erreur"""
    # Capacités maximales (QR Code version 40) pour différents types de données
    capacities = {
        0: {  # ERROR_CORRECT_L (7%)
            'numeric': 7089,
            'alphanumeric': 4296,
            'byte': 2953,
            'description': 'Faible (7%)'
        },
        1: {  # ERROR_CORRECT_M (15%) - DÉFAUT
            'numeric': 5596,
            'alphanumeric': 3391,
            'byte': 2331,
            'description': 'Moyen (15%)'
        },
        2: {  # ERROR_CORRECT_Q (25%)
            'numeric': 3993,
            'alphanumeric': 2420,
            'byte': 1663,
            'description': 'Élevé (25%)'
        },
        3: {  # ERROR_CORRECT_H (30%)
            'numeric': 3057,
            'alphanumeric': 1852,
            'byte': 1273,
            'description': 'Maximum (30%)'
        }
    }
    
    return capacities.get(error_correction_level, capacities[1])

def generate_qr_code_view(request):
    form_type = request.POST.get("form_type", "url")
    qr_code_base64 = None
    qr_code_download_base64 = None
    session_key = 'last_qr_hash'
    form_errors = []

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
    
    # Informations sur les capacités des QR codes
    capacity_info = {
        level: get_qr_capacity_info(level) for level in range(4)
    }

    if request.method == "POST":
        print(f"📝 POST reçu - Form type: {form_type}")
        form_class = forms.get(form_type)
        if form_class:
            form = form_class(request.POST)
            print(f"📋 Formulaire créé: {form_class.__name__}")
            
            # Validation personnalisée selon le type de formulaire
            is_form_valid = validate_form_by_type(form, form_type)
            
            if is_form_valid:
                data = form.cleaned_data
                qr_error_correction_value = int(data.get("qr_error_correction_form", 1))
                
                # Conversion des valeurs d'error correction vers les constantes qrcode
                # Les valeurs du formulaire sont 0, 1, 2, 3 (définies dans forms.py)
                error_correction_map = {
                    0: qrcode.constants.ERROR_CORRECT_L,  # 7%
                    1: qrcode.constants.ERROR_CORRECT_M,  # 15%
                    2: qrcode.constants.ERROR_CORRECT_Q,  # 25%
                    3: qrcode.constants.ERROR_CORRECT_H,  # 30%
                }
                qr_error_correction = error_correction_map.get(qr_error_correction_value, qrcode.constants.ERROR_CORRECT_M)
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
                qr_unique_str = f"{qr_data}|{qr_error_correction}|10"  # box_size fixe
                qr_hash = hashlib.md5(qr_unique_str.encode()).hexdigest()

                # Génération du QR Code avec taille automatique
                qr = qrcode.QRCode(
                    version=None,  # Taille automatique selon les données
                    error_correction=qr_error_correction,
                    box_size=10,   # Taille fixe raisonnable
                    border=4
                )
                qr.add_data(qr_data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")

                # Une seule image pour affichage et téléchargement
                qr_code_base64 = f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
                qr_code_download_base64 = qr_code_base64  # Même image
                
                print(f"✅ QR code généré avec succès pour: {qr_data[:50]}...")
                print(f"📱 Image générée: {img.size}, Version QR: {qr.version}")
                
                # Si c'est une requête normale (pas AJAX), stocker les données en session et rediriger
                if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    # Stocker les résultats en session pour PRG pattern
                    request.session['qr_generation_result'] = {
                        'image_url': qr_code_base64,
                        'download_url': qr_code_download_base64,
                        'form_type': form_type,
                        'form_data': dict(request.POST)
                    }
                    # Redirection pour éviter la resoumission
                    return redirect('generate_qr_code_view')
                
                # Conserver les données du formulaire actuel après génération réussie (AJAX uniquement)
                form_instances[form_type] = form

            else:
                # Collecter toutes les erreurs de formulaire
                for field, errors in form.errors.items():
                    for error in errors:
                        form_errors.append(f"{field}: {error}")
                print(f"Formulaire invalide: {form.errors}")
                
                # Mettre à jour l'instance du formulaire avec les erreurs pour l'affichage
                form_instances[form_type] = form
        else:
            form_errors.append(f"Type de formulaire inconnu: {form_type}")
            print(f"Type de formulaire inconnu: {form_type}")
    else:
        print("Requête GET reçue")
        
        # Récupérer les résultats depuis la session (pattern PRG)
        session_result = request.session.pop('qr_generation_result', None)
        if session_result:
            qr_code_base64 = session_result['image_url']
            qr_code_download_base64 = session_result['download_url']
            form_type = session_result['form_type']
            
            # Reconstituer le formulaire avec les données
            form_class = forms.get(form_type)
            if form_class:
                # Convertir les données de session en format QueryDict
                from django.http import QueryDict
                form_data = QueryDict('')
                for key, value in session_result['form_data'].items():
                    if isinstance(value, list):
                        for v in value:
                            form_data = form_data.copy()
                            form_data.appendlist(key, v)
                    else:
                        form_data = form_data.copy()
                        form_data[key] = value
                
                form = form_class(form_data)
                form_instances[form_type] = form
                print(f"✅ Données restaurées depuis la session pour {form_type}")

    # Si c'est une requête AJAX, retourner du JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': qr_code_base64 is not None,
            'image_url': qr_code_base64,
            'download_url': qr_code_download_base64,
            'errors': form_errors,
            'current_form_type': form_type
        })

    return render(request, "qr_generator.html", {
        "forms": form_instances,
        "image_url": qr_code_base64,
        "download_url": qr_code_download_base64,
        "form_errors": form_errors,
        "current_form_type": form_type,  # Maintenir le type actuel
        "capacity_info": capacity_info,  # Informations sur les capacités
        "active_page": "generator"  # Ajouter le contexte de page active
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
                return render(request, "qr_reader.html", {'form': qr_reader_form, 'result': '', 'image_url': '', 'active_page': 'reader'})

            if qr_img.size > 4 * 1024 * 1024:
                qr_reader_form.add_error('qr_img', '❌ Le fichier est trop volumineux (4 Mo max).')
                return render(request, "qr_reader.html", {'form': qr_reader_form, 'result': '', 'image_url': '', 'active_page': 'reader'})

            # Lecture des données binaires
            img_data = qr_img.read()

            # ✅ Appel de ta fonction utilitaire
            result = read_qr_with_cv2(img_data)
            if not result:
                qr_reader_form.add_error('qr_img', "❌ Ce fichier n'est pas un QR Code valide ou est corrompu.")
                return render(request, "qr_reader.html", {'form': qr_reader_form, 'result': result, 'image_url': '', 'active_page': 'reader'})

            # Encodage Base64 pour l'affichage
            image_base64 = base64.b64encode(img_data).decode('utf-8')

    return render(request, "qr_reader.html", {
        'form': qr_reader_form,
        'result': result,
        'image_url': image_base64,
        'active_page': 'reader'
    })



def qr_history(request):
    return render(request, "qr_history.html")


def about(request):
    return render(request, "about.html", {'active_page': 'about'})

def privacy_policy(request):
    context = {
        'current_date': datetime.now(),
        'active_page': 'privacy'
    }
    return render(request, 'privacy.html', context)

def mentions_legales(request):
    context = {
        'current_date': datetime.now(),
        'active_page': 'mentions_legales'
    }
    return render(request, "mentions_legales.html", context)
