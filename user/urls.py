from django.conf.urls import patterns, url

from user import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_account, name='login_account'),
    url(r'^logout/$', views.logout_account, name='logout_account'),    
)