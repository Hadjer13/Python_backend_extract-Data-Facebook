from django.conf.urls import url
from gestionsource import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^source_site/$', views.sourceSite_list),
    url(r'^source_site/(?P<pk>[0-9]+)/$', views.sourceSite_detail),

    url(r'^source_rs/$', views.sourceRS_list),
    url(r'^source_rs/(?P<pk>[0-9]+)/$', views.sourceRS_detail),

    url(r'^collecte_site/$', views.collecteSite_list),
    url(r'^collecte_site/(?P<pk>[0-9]+)/$', views.collecteSite_detail),

    url(r'^collecte_rs/$', views.collecteRS_list),
    url(r'^collecte_rs/(?P<pk>[0-9]+)/$', views.collecteRS_detail),

    url(r'^operateur/$', views.operateur_list),
    url(r'^operateur/(?P<pk>[0-9]+)/$', views.operateur_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
