from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download_charges/(?P<findex>[\w\-\.\W]+)/$', views.download_levels_pdf, name='download_levels_pdf'),
]
