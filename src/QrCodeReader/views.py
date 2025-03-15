import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from QrCodeReader.forms import QrGenerateForm,QrLoader
DIR_QR_CONFIG = "QrCodeReader/config"
QR_CONFIG_FILE = "config.json"

import qr_code


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
            print(image_url)

            result = qr_code.read_qr_code(file_path)
            if result == None:
                result = "Ce fichier n'est pas un QR Code"

           
    else:
        qr_reader_form = QrLoader()
        image_url = ""
        result = ""

    return render(request,"qr_reader.html",{"form" : qr_reader_form,"result" : result,'image_url': image_url})


def qr_generator(request):
    if request.method == "POST":
        qr_generate_form = QrGenerateForm(request.POST)
        if qr_generate_form.is_valid():
            qr_entry = qr_generate_form.cleaned_data['text_to_convert_form']
            qr_version = None
            qr_error_correct = int(qr_generate_form.cleaned_data['qr_error_correction_form'])
            qr_box_size = int(qr_generate_form.cleaned_data['qr_box_size_form'])
            
            # attention le chemin d'url n'est que correcte en debug
            file_path = qr_code.get_file_path(qr_code.QR_CONFIG_FILE,qr_code.DIR_QR_CONFIG)
            print(file_path)
            qr_code.save_qr_config(file_path,
                                   qr_version,
                                   qr_error_correct,
                                   qr_box_size,
                                   qr_border=4)
            qr_code.handle_generate_qr(qr_entry)
            image_url = "static/qr_img/QR000.png"
            
    else:    
        qr_generate_form = QrGenerateForm()
        image_url = ""

    return render(request,"qr_generator.html",{"form" : qr_generate_form,"image_url":image_url})


def qr_history(request):
    return render(request,"qr_history.html")


def about(request):
    return render(request,"about.html")