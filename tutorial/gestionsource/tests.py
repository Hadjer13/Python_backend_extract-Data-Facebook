# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from gestionsource.serializers import SourceDataSerializer
from gestionsource.serializers import CollecteSourceDataSerializer
from gestionsource.models import SourceData
from gestionsource.models import CollecteSourceData
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

sourcedate = SourceData(link='Twitter.com/MOBILIS-OFFICIELLE',type='Reseau social')
sourcedate.save()
#- met dans la base

serializer = SourceDataSerializer(sourcedate)
serializer.data
content = JSONRenderer().render(serializer.data)
content # json

sourcedate = SourceData(link='facebook.com/MOBILIS-OFFICIELLE',type='Reseau social')
sourcedate.save()

serializer = SourceDataSerializer(sourcedate)
serializer.data
content = JSONRenderer().render(serializer.data)
content

from django.utils.six import BytesIO

stream = BytesIO(content)
data = JSONParser().parse(stream) #python_format

serializer = SourceDataSerializer(data=data)
serializer.is_valid()

serializer.validated_data

serializer.save()

serializer = SourceDataSerializer(SourceData.objects.all(), many=True)
serializer.data
