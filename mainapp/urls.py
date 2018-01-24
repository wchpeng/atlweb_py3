from django.conf.urls import url
from mainapp import views


urlpatterns = [
    url(r'^api_doc/$', views.get_api_doc),   # api文档
]