from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from uauth import views

urlpatterns = [
    url(r'^auth-token/$', obtain_auth_token),
    url(r'^$', views.index),
    url(r'^login/$', views.log_in),
    url(r'^logout/$', views.log_out),
    url(r'^register/$', views.register),
    # url(r'send-email/$', views.test_send_email),
]