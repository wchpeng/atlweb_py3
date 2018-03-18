"""atlweb_py3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .settings import DEBUG
from .settings import MEDIA_ROOT

schema_view = get_schema_view(title="api docs", url="127.0.0.1:8000/uauth/login/", renderer_classes=(SwaggerUIRenderer, OpenAPIRenderer))

urlpatterns = [
    url(r'^docs/$', schema_view, name="docs"),
    url(r'^api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT, 'show_indexes': True}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('uauth/', include('uauth.urls')),
    path('image/', include('image.urls')),
    path('mainapp/', include('mainapp.urls')),
    path('community/', include('community.urls')),
    path('chat/', include('chat.urls')),
    path('social/', include('social.urls')),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
