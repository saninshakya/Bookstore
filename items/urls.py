from django.conf.urls import patterns, url

from items import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^insert/$', views.insert, name='insert'),
    url(r'^detail/(?P<itemid>\d+)/$', views.detail, name='detail'),
    url(r'^detail/(?P<itemid>\d+)/edit/$', views.edit, name='edit'),
    url(r'^detail/(?P<itemid>\d+)/delete/$', views.delete, name='delete'),
    url(r'^insert/bulk/$', views.insert_bulk, name='insert_bulk'),
    url(r'^download/static/data/tableofcontent/(?P<filename>\d+)/$', views.pdf_download, name='pdf_download'),
)