from django.shortcuts import render
from rest_framework import permissions, mixins, generics, viewsets, filters
from django_filters import rest_framework

from image.models import Picture, Album
from image.serializers import AlbumListSerializer, AlbumDetailSerializer, PictureSerializer
from utils.permissions import IsOwnerRetrieveUpdate


# album list 显示
class AlbumListViews(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Album.objects.filter(visible=True).order_by("add_date")
    serializer_class = AlbumListSerializer
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ("user",)
    ordering_fields = ("add_date", )
    search_fields = ("brief", "name")


# album detail 图册详情
class AlbumDetailViews(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Album.objects.filter(visible=True)
    serializer_class = AlbumDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)


# album update 图册修改
class AlbumModViews(viewsets.ModelViewSet):
    queryset = Album.objects.filter(visible=True)
    serializer_class = AlbumDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerRetrieveUpdate)


class PictureCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """create 图片"""
    queryset = Picture.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PictureSerializer
