from django.conf.urls import patterns, url

from review import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^(?P<itemid>\d+)/$', views.index, name='index'),
    url(r'^post/(?P<itemid>\d+)/$', views.insert, name='insert'),
)


