from idlelib.idle_test.test_io import S

from rest_framework import serializers
from gestioncollecte.models import Page
from gestioncollecte.models import Publication
from gestioncollecte.models import Reaction
from gestioncollecte.models import Offre



class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('idPage', 'name','link', 'nbAbonnee','idOperateur','created')

class PublicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = ('idPub','idPage' ,'link','content', 'typePub', 'nbLike','nbShare','nbComment','created')

class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id','idPub','typeRea', 'nbRea', 'created')

class OffreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offre
        fields = ('id','name','link', 'idOperateur', 'created')