from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from uauth import views

# router注册视图
router = routers.SimpleRouter()
router.register(r"users-list", views.UserInfoList)
router.register(r"users-detail", views.UserInfoDetail)

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.log_in),
    url(r'^logout/$', views.log_out),
    url(r'^register/$', views.register),
    url(r'^auth-token/$', obtain_auth_token),
    url(r'^send-email/$', views.test_send_email),
    # url(r'^', include(router.urls)),
]

urlpatterns += router.urls
