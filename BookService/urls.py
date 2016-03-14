from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BookService.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^items/', include('items.urls')),
    url(r'^category/', include('category.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^review/', include('review.urls')),
	url(r'^wishlist/', include('wishlist.urls')),
    url(r'^koha/', include('kohaitems.urls')),
)
