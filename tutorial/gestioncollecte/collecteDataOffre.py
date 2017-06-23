from lxml import html
# encoding: utf-8
import codecs
import io
import urllib2
import json
import datetime
import csv
import time
import requests
from gestionsource.serializers import CollecteSiteSerializer, SourceSiteSerializer
from gestionsource.models import SourceSite
from gestioncollecte.models import Offre
from gestioncollecte.serializers import OffreSerializer

def scrapSite(d):


    print "Thread started"
    serializer = CollecteSiteSerializer(data=d)
    if serializer.is_valid():
        path = serializer.data['xpath']
        print path
        pk = serializer.data['id_source_site']
        print pk
        source = SourceSite.objects.get(pk=pk)
        serializer2 = SourceSiteSerializer(source)

        page = requests.get(serializer2.data['link'])

        tree = html.fromstring(page.content)

        offres = tree.xpath(path)
        for o in offres:
            o = o.strip()
            o = o.encode('UTF-8')
            o = str(o)
            print o
            ffre = Offre.objects.create(name=o,link=serializer2.data['link'],id_operateur=serializer2.data['id_operateur'])
            print "object constructed"

        print "Thread finished"
        return 0
    else:
        print "Thread stopped"
        return -1
