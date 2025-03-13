from django.shortcuts import render
from QrCodeReader.forms import QrGenerateForm


import qr_code

def qr_reader(request):
    return render(request,"qr_reader.html")


def qr_generator(request):
    if request.method == "POST":
        qr_generate_form = QrGenerateForm(request.POST)
        if qr_generate_form.is_valid():
            qr_entry = qr_generate_form.cleaned_data['text_to_convert_form']
           
            qr_code.handle_generate_qr(qr_entry)
    else:    
        qr_generate_form = QrGenerateForm()

    return render(request,"qr_generator.html",{"form" : qr_generate_form})


def qr_history(request):
    return render(request,"qr_history.html")

def about(request):
    return render(request,"about.html")