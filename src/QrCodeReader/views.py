from django.shortcuts import render
from QrCodeReader.forms import QrReaderForm

def qr_reader(request):
    return render(request,"qr_reader.html")


def qr_generator(request):
    qr_text_form = QrReaderForm()


    return render(request,"qr_generator.html",{"form" : qr_text_form})


def qr_history(request):
    return render(request,"qr_history.html")

def about(request):
    return render(request,"about.html")