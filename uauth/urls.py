from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from uauth import views

# router注册视图
router = routers.SimpleRouter()
router.register(r"users-list", views.UserInfoList)
router.register(r"users-detail", views.UserInfoDetail)

urlpatterns = [
    url(r'^$', views.index),                                      # 登陆后主页
    url(r'^login/$', views.log_in),                               # 登陆页面
    url(r'^logout/$', views.log_out),                             # 登出
    url(r'^register/$', views.register),                          # 注册
    url(r'^auth-token/$', obtain_auth_token),                     # 获取token
    url(r'^send-email/$', views.test_send_email),                 # 发送邮件（测试）
    url(r"^my-info-page/$", views.my_info_page),                  # 我的信息页
    url(r"^his-info-page/(.+?)/$", views.his_info_page),          # 别人的信息页
    url(r"^exist-username-email/$", views.exist_username_email),  # email和username是否存在
    url(r"^mod-userinfo/$", views.mod_userinfo),                  # 修改个人信息
    # url(r'^', include(router.urls)),
    url(r"^user-info-list/$", views.get_excel_userinfo),
]

urlpatterns += router.urls
