# -*- coding: utf-8 -*-
from django.db import models

class Time(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	nome = models.CharField("nome", max_length=255)
	brasao = models.CharField("brasao", max_length=255)
	
	def __unicode__(self):
		return self.nome

	def natural_key(self):
		return (self.nome)

	class Meta:
		db_table = 'time'
		ordering = ['nome']


class Campeonato(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	nome = models.CharField("nome", max_length=255)
	
	def __unicode__(self):
		return self.nome

	def natural_key(self):
		return (self.nome)

	class Meta:
		db_table = 'campeonato'
		ordering = ['nome']


class Jogo(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	primeirotime = models.ForeignKey(Time, related_name="primeirotime", null=True, on_delete=models.DO_NOTHING)
	resultadoprimeirotime = models.IntegerField("resultadoprimeirotime", null=True, blank=True)
	segundotime = models.ForeignKey(Time, related_name="segundotime", null=True, on_delete=models.DO_NOTHING)
	resultadosegundotime = models.IntegerField("resultadosegundotime", null=True, blank=True)
	data = models.DateField("data", auto_now_add=True)
	calculado = models.BooleanField("calculado")
	campeonato = models.ForeignKey(Campeonato, null=True)
	datajogo = models.DateField("datajogo", null=True)

	def __unicode__(self):
		return u'%s %s x %s %s' % (self.primeirotime, self.resultadoprimeirotime, self.resultadosegundotime, self.segundotime)

	def natural_key(self):
		return (self.primeirotime, self.segundotime)

	class Meta:
		db_table = 'jogo'
		ordering = ['-datajogo', 'calculado', 'id']


class Usuario(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField("nome", max_length=255)
    login = models.EmailField("login", max_length=255)
    senha = models.CharField("senha", max_length=32)
    ranking = models.IntegerField("ranking")
    ativo = models.BooleanField("ativo")
    
    def __unicode__(self):
	    return self.nome
    
    def natural_key(self):
    	return (self.nome)
    
    class Meta:
    	db_table = 'usuario'
    	unique_together = (('login'),)
    	ordering = ['nome']


class Aposta(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	jogo = models.ForeignKey(Jogo)
	usuario = models.ForeignKey(Usuario)
	primeirotime = models.IntegerField("primeirotime")
	segundotime = models.IntegerField("segundotime")
	data = models.DateField("data", auto_now_add=True)
	pontos = models.IntegerField("pontos", null=True, blank=True)

	def __unicode__(self):
		return u'%s - %s' % (self.jogo, self.usuario)

	def natural_key(self):
		return (self.jogo, self.usuario)

	class Meta:
		db_table = 'aposta'
		ordering = ['-data']
