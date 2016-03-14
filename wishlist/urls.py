from django.conf.urls import patterns, url
from wishlist import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<itemid>\d+)/add/$', views.insert, name='insert'),
    url(r'^(?P<wishid>\d+)/update/$', views.update, name='update'),
    url(r'^(?P<wishid>\d+)/delete/$', views.delete, name='delete'),
)