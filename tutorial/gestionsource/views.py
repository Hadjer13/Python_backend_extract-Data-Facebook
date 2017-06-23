# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gestionsource.models import SourceSite , SourceRS , Operateur, CollecteSite , CollecteRS
from gestionsource.serializers import SourceSiteSerializer , SourceRSSerializer , OperateurSerializer, CollecteSiteSerializer , CollecteRSSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gestioncollecte.collecteDataOffre import scrapSite

@api_view(['GET', 'POST'])
def sourceSite_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        source = SourceSite.objects.all()
        serializer = SourceSiteSerializer(source, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SourceSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sourceSite_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        source = SourceSite.objects.get(pk=pk)
    except SourceSite.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SourceSiteSerializer(source)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SourceSiteSerializer(source, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        source.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def sourceRS_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        source = SourceRS.objects.all()
        serializer = SourceRSSerializer(source, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SourceRSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sourceRS_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        source = SourceRS.objects.get(pk=pk)
    except SourceRS.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SourceRSSerializer(source)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SourceRSSerializer(source, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        source.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
import threading
@api_view(['GET', 'POST'])
def collecteSite_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        collecte = CollecteSite.objects.all()
        serializer = CollecteSiteSerializer(collecte, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollecteSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # ICI appel a la fonction de collecte __mais Thread !! pour ne pas attendre la reponse
            #i = scrap(request.data)
            threadObj = threading.Thread(target=scrapSite, args=[request.data])
            threadObj.start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def collecteSite_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        collecte = CollecteSite.objects.get(pk=pk)
    except CollecteSite.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CollecteSiteSerializer(collecte)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollecteSiteSerializer(collecte, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        collecte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def collecteRS_list(request):

    if request.method == 'GET':
        collecte = CollecteRS.objects.all()
        serializer = CollecteRSSerializer(collecte, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollecteRSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def collecteRS_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        collecte = CollecteRS.objects.get(pk=pk)
    except CollecteRS.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CollecteRSSerializer(collecte)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollecteRSSerializer(collecte, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        collecte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def operateur_list(request):

    if request.method == 'GET':
        operateur = Operateur.objects.all()
        serializer = OperateurSerializer(operateur, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OperateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def operateur_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        operateur = Operateur.objects.get(pk=pk)
    except Operateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OperateurSerializer(operateur)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OperateurSerializer(operateur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        operateur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)