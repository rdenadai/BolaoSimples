# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.db import connection, transaction
from .models import Time, Jogo, Usuario, Aposta
from classes.serializer import Serialize
from datetime import datetime

# Traducao
from django.utils.translation import gettext as _trans, get_language, activate as activateLanguage


def retorna(message=None):
    if not message:
        message = {
            'success': False,
            'result': {
                'reason': _trans("Dados inválidos ou incorretos!")
            }
        }
    return HttpResponse(json.dumps(message), content_type='text/javascript')


def index(request):
    return render_to_response('home/index.html', {'language': get_language(), 'STATIC_URL': settings.STATIC_URL})


def jogo(request):
    jogos = Jogo.objects.select_related().all().exclude(calculado=True)
    for jogo in jogos:
        jogo.apostas = Aposta.objects.filter(jogo__pk=jogo.id, jogo__calculado=False).order_by("usuario__nome")
    return render_to_response('home/jogo.html',
                              {'language': get_language(), 'STATIC_URL': settings.STATIC_URL, 'jogos': jogos})


def ranking(request):
    usuarios = Usuario.objects.all().order_by("-ranking")
    for i, usuario in enumerate(usuarios):
        usuario.ordem = i
    return render_to_response('home/ranking.html',
                              {'language': get_language(), 'STATIC_URL': settings.STATIC_URL, 'usuarios': usuarios})


def pontuacao(request):
    jogos = list(Jogo.objects.select_related().all().exclude(calculado=False))
    for jogo in jogos:
        jogo.apostas = Aposta.objects.filter(jogo__pk=jogo.id, jogo__calculado=True).order_by("usuario__nome")
    return render_to_response('home/pontuacao.html',
                              {'language': get_language(), 'STATIC_URL': settings.STATIC_URL, 'jogos': jogos})


def apostas(request):
    apostas = None
    try:
        id_jogo = int(request.POST.get("idJogo", 0))
        apostas = Aposta.objects.filter(jogo__pk=id_jogo).order_by("usuario__nome")
    except ValueError:
        pass
    return render_to_response('home/apostas.html',
                              {'idJogo': id_jogo, 'language': get_language(), 'STATIC_URL': settings.STATIC_URL,
                               'apostas': apostas})


def formulario(request):
    id_jogo = None
    jogo = None
    try:
        id_jogo = int(request.POST.get("idJogo", 0))
        jogo = Jogo.objects.select_related().get(id=id_jogo)
    except ValueError:
        pass
    usuarios = Usuario.objects.filter(ativo=True).order_by('nome')
    return render_to_response('home/formulario.html',
                              {'language': get_language(), 'STATIC_URL': settings.STATIC_URL, 'usuarios': usuarios,
                               'jogo': jogo, 'idJogo': id_jogo})


@transaction.atomic
def salvar(request):
    message = {'success': False, 'message': _trans("Erro ao salvar aposta, tente novamente!")}
    try:
        id_jogo = int(request.POST.get("idJogo", 0))
        id_usuario = int(request.POST.get("idUsuario", 0))
        resultado_primeiro_time = int(request.POST.get("resultadoprimeirotime", 0))
        resultado_segundo_time = int(request.POST.get("resultadosegundotime", 0))
    except ValueError:
        message['message'] = _trans("Erro ao recuperar parâmetros!")
    
    try:
        existe = Aposta.objects.filter(jogo__pk=id_jogo, usuario__pk=id_usuario)
        if len(existe) == 0:
            jogo = Jogo.objects.get(pk=id_jogo)
            usuario = Usuario.objects.get(pk=id_usuario)
            aposta = Aposta(jogo=jogo, usuario=usuario, primeirotime=resultado_primeiro_time,
                            segundotime=resultado_segundo_time)
            aposta.save()
            if aposta.id > 0:
                message['success'] = True
                message['message'] = _trans("Aposta salva com sucesso! Boa sorte...")
        else:
            message['message'] = _trans(
                "Ow maluco, vc ta tentando fazer aposta em um jogo no qual ja apostou! Prestenção retardado!")
    except:
        message['message'] = _trans("Erro ao executar a operação para salvar aposta!")
    return retorna(message)


def form_calcular(request):
    data = datetime.now()
    jogos = Jogo.objects.select_related().all().exclude(calculado=True).exclude(
        data__gt=datetime(data.year, data.month, data.day))
    return render_to_response('home/formulario-calcular.html',
                              {'language': get_language(), 'STATIC_URL': settings.STATIC_URL, 'jogos': jogos})


@transaction.atomic
def calcular(request):
    try:
        id_jogos = request.POST.getlist('jogo')
        for id_jogo in id_jogos:
            jogo = Jogo.objects.get(pk=id_jogo)
            apostas = Aposta.objects.filter(jogo=jogo)
            for aposta in apostas:
                usuario = Usuario.objects.get(pk=aposta.usuario.id)
                aposta1_time = aposta.primeirotime
                aposta2_time = aposta.segundotime
                jogo1_time = jogo.resultadoprimeirotime
                jogo2_time = jogo.resultadosegundotime
                pts = 0
                if jogo1_time != '' and jogo2_time != '':
                    if jogo1_time > jogo2_time:
                        if aposta1_time > aposta2_time:
                            pts += 5
                        if aposta1_time == jogo1_time:
                            pts += 2
                        if aposta2_time == jogo2_time:
                            pts += 2
                    elif jogo2_time > jogo1_time:
                        if aposta2_time > aposta1_time:
                            pts += 5
                        if aposta2_time == jogo2_time:
                            pts += 2
                        if aposta1_time == jogo1_time:
                            pts += 2
                    elif jogo1_time == jogo2_time:
                        if aposta1_time == aposta2_time:
                            pts += 5
                        if aposta1_time == jogo1_time:
                            pts += 2
                        if aposta2_time == jogo2_time:
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
