# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SourceSite(models.Model):

    link = models.CharField(max_length=100, blank=True, default='')
    id_operateur = models.IntegerField(default=0,null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class SourceRS(models.Model):


    link = models.CharField(max_length=100, blank=True, default='')
    id_operateur = models.IntegerField(default=0,null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)



class CollecteSite(models.Model):


    xpath = models.CharField(max_length=100, blank=True, default='')
    timer = models.IntegerField(default=0,null=False, blank=True)
    id_source_site = models.IntegerField(default=0,null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class CollecteRS(models.Model):


    type = models.CharField(max_length=100, blank=True, default='')
    appID = models.CharField(max_length=100, blank=True, default='')
    appSecret = models.CharField(max_length=100, blank=True, default='')
    id_source_RS = models.IntegerField(default=0,null=False, blank=True)
    timer = models.IntegerField(default=0,null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class Operateur(models.Model):


    nom = models.CharField(max_length=100, blank=True, default='')
    groupe = models.CharField(max_length=50, blank=True, default='')
    type = models.CharField(max_length=50, blank=True, default='')
    pays = models.CharField(max_length=50, blank=True, default='')
    continent = models.CharField(max_length=50, blank=True, default='')
    region = models.CharField(max_length=50, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)