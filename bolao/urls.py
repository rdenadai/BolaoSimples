from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
import apostas

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bolao.views.home', name='home'),
    # url(r'^bolao/', include('bolao.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Sistema
    ('^$', 'apostas.views.index'),
    ('^jogo/', 'apostas.views.jogo'),
    ('^ranking/', 'apostas.views.ranking'),
    ('^pontuacao/', 'apostas.views.pontuacao'),
    ('^apostas/', 'apostas.views.apostas'),
    ('^formulario/', 'apostas.views.formulario'),
    ('^salvar/', 'apostas.views.salvar'),
    ('^admin-calcular/', 'apostas.views.formCalcular'),
    ('^calcular/', 'apostas.views.calcular'),
    # Grapelli
    (r'^grappelli/', include('grappelli.urls')),
)
