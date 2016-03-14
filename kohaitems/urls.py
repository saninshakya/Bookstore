from django.conf.urls import patterns, url

from kohaitems import views

urlpatterns = patterns('',
	url(r'^display/$', views.display_item_from_koha, name='display_item_from_koha'),
)
 