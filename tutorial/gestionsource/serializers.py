from idlelib.idle_test.test_io import S

from rest_framework import serializers
from gestionsource.models import SourceSite
from gestionsource.models import SourceRS
from gestionsource.models import CollecteSite
from gestionsource.models import CollecteRS
from gestionsource.models import Operateur


class SourceSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceSite
        fields = ('id', 'link', 'id_operateur')

class SourceRSSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceRS
        fields = ('id', 'link', 'id_operateur')


class CollecteSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollecteSite
        fields = ('id', 'id_source_site', 'xpath', 'timer')

class CollecteRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollecteRS
        fields = ('id', 'id_source_RS','appID','appSecret','timer' )

class OperateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operateur
        fields = ('id', 'nom','groupe','type','pays','continent','region')