from django.conf.urls import include, url
from django.contrib import admin
from oscar.app import application

urlpatterns = [
    # Examples:
    # url(r'^$', 'djmarketplace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(application.urls)),
]
