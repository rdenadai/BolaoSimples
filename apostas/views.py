# -*- coding: utf-8 -*-
# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.db import connection, transaction
from models import Time, Jogo, Usuario, Aposta
from classes.serializer import Serialize
from datetime import datetime

# Traducao
from django.utils.translation import gettext as _trans, get_language, activate as activateLanguage

def retorna(message=None):
    if not message:
        message = '{success:false, result: { reason: "',_trans("Dados inválidos ou incorretos!"),'" } }'
    return HttpResponse(message, mimetype='text/javascript')

def index(request):
    return render_to_response('home/index.html', { 'language':get_language(), 'STATIC_URL':settings.STATIC_URL })

def jogo(request):
    jogos = Jogo.objects.select_related().all().exclude(calculado=True)
    for jogo in jogos:
        apostas = Aposta.objects.filter(jogo__pk=jogo.id, jogo__calculado=False).order_by("usuario__nome")
        jogo.apostas = apostas
    return render_to_response('home/jogo.html', { 'language':get_language(), 'STATIC_URL':settings.STATIC_URL, 'jogos':jogos })

def ranking(request):
	usuarios = Usuario.objects.all().order_by("-ranking")
	i = 1
	for usuario in usuarios:
		usuario.ordem = i
		i += 1
	return render_to_response('home/ranking.html', { 'language':get_language(), 'STATIC_URL':settings.STATIC_URL, 'usuarios':usuarios })

def pontuacao(request):
    jogos = list(Jogo.objects.select_related().all().exclude(calculado=False))
    for jogo in jogos:
        apostas = Aposta.objects.filter(jogo__pk=jogo.id, jogo__calculado=True).order_by("usuario__nome")
        jogo.apostas = apostas
    return render_to_response('home/pontuacao.html', { 'language':get_language(), 'STATIC_URL':settings.STATIC_URL, 'jogos':jogos })

def apostas(request):
    apostas = None
    try:
        idJogo = int(request.POST.get("idJogo", 0))
        apostas = Aposta.objects.filter(jogo__pk=idJogo).order_by("usuario__nome")
    except ValueError:
        pass
    return render_to_response('home/apostas.html', { 'idJogo':idJogo,'language':get_language(), 'STATIC_URL':settings.STATIC_URL, 'apostas':apostas })

def formulario(request):
    idJogo = None
    jogo = None
    try:
        idJogo = int(request.POST.get("idJogo", 0))
        jogo = Jogo.objects.select_related().get(id=idJogo)
    except ValueError:
        pass
    usuarios = Usuario.objects.filter(ativo=True).order_by('nome')
    return render_to_response('home/formulario.html', { 'language':get_language(), 'STATIC_URL':settings.STATIC_URL, 'usuarios':usuarios, 'jogo':jogo, 'idJogo':idJogo })


@transaction.autocommit
def salvar(request):
    message = '{"success":false, "message":"Erro ao salvar aposta, tente novamente!"}'
    try:
        idJogo = int(request.POST.get("idJogo", 0))
        idUsuario = int(request.POST.get("idUsuario", 0))
        resultadoprimeirotime = int(request.POST.get("resultadoprimeirotime", 0))
        resultadosegundotime = int(request.POST.get("resultadosegundotime", 0))
    except ValueError:
        message = '{"success":false, "message":"Erro ao recuperar parâmetros!"}'
    
    try:
        existe = Aposta.objects.filter(jogo__pk=idJogo, usuario__pk=idUsuario)
        if len(existe) == 0:
            jogo = Jogo.objects.get(pk=idJogo)
            usuario = Usuario.objects.get(pk=idUsuario)
            aposta = Aposta(jogo=jogo, usuario=usuario, primeirotime=resultadoprimeirotime, segundotime=resultadosegundotime)
            aposta.save()
            if aposta.id > 0:
                message = '{"success":true, "message":"Aposta salva com sucesso! Boa sorte..."}'
        else:
            message = '{"success":false, "message":"Ow maluco, vc ta tentando fazer aposta em um jogo no qual ja apostou! Prestenção retardado!"}'
    except:
        message = '{"success":false, "message":"Erro ao executar a operação para salvar aposta!"}'
    return retorna(message)


def formCalcular(request):
    data = datetime.now()
    jogos = Jogo.objects.select_related().all().exclude(calculado=True).exclude(data__gt=datetime(data.year, data.month, data.day))
    return render_to_response('home/formulario-calcular.html', { 'language':get_language(), 'STATIC_URL':settings.STATIC_URL, 'jogos':jogos })


@transaction.autocommit
def calcular(request):
    try:
        idJogos = request.POST.getlist('jogo')
        for idJogo in idJogos:
            jogo = Jogo.objects.get(pk=idJogo)
            apostas = Aposta.objects.filter(jogo=jogo)
            for aposta in apostas:
                usuario = Usuario.objects.get(pk=aposta.usuario.id)
                aposta1time = aposta.primeirotime
                aposta2time = aposta.segundotime
                jogo1time = jogo.resultadoprimeirotime
                jogo2time = jogo.resultadosegundotime
                pts = 0
                if jogo1time != '' and jogo2time != '':
                    if jogo1time > jogo2time:
                        if aposta1time > aposta2time:
                            pts += 5
                        if aposta1time == jogo1time:
                            pts += 2
                        if aposta2time == jogo2time:
                            pts += 2
                    elif jogo2time > jogo1time:
                        if aposta2time > aposta1time:
                            pts += 5
                        if aposta2time == jogo2time:
                            pts += 2
                        if aposta1time == jogo1time:
                            pts += 2
                    elif jogo1time == jogo2time:
                        if aposta1time == aposta2time:
                            pts += 5
                        if aposta1time == jogo1time:
                            pts += 2
                        if aposta2time == jogo2time:
                            pts += 2
                    usuario.ranking += pts
                    usuario.save()
                aposta.pontos = pts
                aposta.save()
            jogo.calculado = True
            jogo.save()
    except:
        pass
    return redirect('/bolao/admin-calcular/')
