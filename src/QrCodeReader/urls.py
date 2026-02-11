from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from .views import (
    qr_reader, generate_qr_code_view, qr_history,
    about, privacy_policy, mentions_legales, health_check
)
from django.conf.urls.static import static
from django.conf import settings


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return [
            'generate_qr_code_view',
            'qrreader',
            'about',
            'privacy',
            'mentions_legales',
        ]

    def location(self, item):
        from django.urls import reverse
        return reverse(item)


sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('', generate_qr_code_view, name='generate_qr_code_view'),
    path('qr-reader/', qr_reader, name='qrreader'),
    path('qr-generator/', generate_qr_code_view, name='qrgenerator'),
    path('about/', about, name='about'),
    path('privacy/', privacy_policy, name='privacy'),
    path('mentions-legales/', mentions_legales, name='mentions_legales'),
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('google6630a1c4a0298bf9.html', TemplateView.as_view(template_name='verification/google6630a1c4a0298bf9.html')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
