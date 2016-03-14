from django.conf.urls import patterns, url

from category import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^insert/$', views.insert, name='insert'),
    url(r'^detail/(?P<categoryid>\d+)/edit/$', views.edit, name='edit'),
    url(r'^detail/(?P<categoryid>\d+)/delete/$', views.delete, name='delete'),
)