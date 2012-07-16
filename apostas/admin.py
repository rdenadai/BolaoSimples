# -*- coding: utf-8 -*-
from apostas.models import Time, Jogo, Usuario, Aposta, Campeonato
from django.contrib import admin



class JogoAdmin(admin.ModelAdmin):
    list_display = ['jogo', 'campeonato', 'datajogo']
    
    def jogo(self, obj):
        return u'%s %s x %s %s' % (obj.primeirotime, obj.resultadoprimeirotime, obj.resultadosegundotime, obj.segundotime)

class ApostaAdmin(admin.ModelAdmin):
    list_display = ['jogo', 'usuario', 'data']

admin.site.register(Jogo, JogoAdmin)
admin.site.register(Aposta, ApostaAdmin)

admin.site.register(Time)
#admin.site.register(Jogo)
admin.site.register(Usuario)
#admin.site.register(Aposta)
admin.site.register(Campeonato)