from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.GatewayView.as_view(), name='gateway')
]
