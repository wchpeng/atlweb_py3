from django.conf.urls import url

from chat import views

urlpatterns = [
    url(r'index/$', views.chat_index),  # 交流
    # url(r'index2/$', views.we_chat2),  # 交流
]