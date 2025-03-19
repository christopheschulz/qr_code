"""
URL configuration for QrCodeReader project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import qr_reader,generate_qr_code_view,qr_history,about
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', generate_qr_code_view, name='qrgenerator'),
    path('qrreader', qr_reader, name='qrreader'),
    path('qrgenerator', generate_qr_code_view, name='qrgenerator'),
    path('qrhistory', qr_history, name='qrhistory'),
    path('about', about, name='about'),
    path('admin/', admin.site.urls),
    path('google6630a1c4a0298bf9.html', TemplateView.as_view(template_name='verification/google6630a1c4a0298bf9.html')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
