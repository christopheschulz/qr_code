from django.shortcuts import render


def qr_reader(request):
    return render(request,"qr_reader.html")


def qr_generator(request):
    return render(request,"qr_generator.html")


def qr_history(request):
    return render(request,"qr_history.html")

def about(request):
    return render(request,"about.html")