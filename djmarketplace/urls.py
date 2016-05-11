from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from oscar.app import application
from apps.partner.app import application as ShopApplication

urlpatterns = [
    # Examples:
    # url(r'^$', 'djmarketplace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(application.urls)),
    url(r'gateway/', include('apps.gateway.urls')),
    url(r'shop/', include(ShopApplication.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
