from django.shortcuts import render
from QrCodeReader.forms import QrGenerateForm
DIR_QR_CONFIG = "QrCodeReader/config"
QR_CONFIG_FILE = "config.json"

import qr_code

def qr_reader(request):
    return render(request,"qr_reader.html")


def qr_generator(request):
    if request.method == "POST":
        qr_generate_form = QrGenerateForm(request.POST)
        if qr_generate_form.is_valid():
            print(qr_generate_form.cleaned_data)
            qr_entry = qr_generate_form.cleaned_data['text_to_convert_form']
            
            qr_version = None
            qr_error_correct = int(qr_generate_form.cleaned_data['qr_error_correction_form'])
            qr_box_size = int(qr_generate_form.cleaned_data['qr_box_size_form'])
            
            file_path = qr_code.get_file_path(qr_code.QR_CONFIG_FILE,qr_code.DIR_QR_CONFIG)
            print(file_path)
            qr_code.save_qr_config(file_path,
                                   qr_version,
                                   qr_error_correct,
                                   qr_box_size,
                                   qr_border=4)
            qr_code.handle_generate_qr(qr_entry)
    else:    
        qr_generate_form = QrGenerateForm()

    return render(request,"qr_generator.html",{"form" : qr_generate_form})


def qr_history(request):
    return render(request,"qr_history.html")

def about(request):
    return render(request,"about.html")