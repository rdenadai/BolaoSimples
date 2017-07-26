from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from apostas import views as ap_views

urlpatterns = [
    # Grapelli
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    # Admin
    url(r'^admin/', include(admin.site.urls)),  # admin site
    # Sistema
    url('^$', ap_views.index),
    url('^jogo/', ap_views.jogo),
    url('^ranking/', ap_views.ranking),
    url('^pontuacao/', ap_views.pontuacao),
    url('^apostas/', ap_views.apostas),
    url('^formulario/', ap_views.formulario),
    url('^salvar/', ap_views.salvar),
    url('^admin-calcular/', ap_views.form_calcular),
    url('^calcular/', ap_views.calcular),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
