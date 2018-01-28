from django.shortcuts import render
from rest_framework import permissions, mixins, generics, viewsets

from image.models import Picture, Album
from image.serializers import AlbumListSerializer, AlbumDetailSerializer
from image.permissions import IsOwnerMod


# album list 显示
class AlbumListViews(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Album.objects.filter(visible=True)
    serializer_class = AlbumListSerializer


# album detail 图册详情
class AlbumDetailViews(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Album.objects.filter(visible=True)
    serializer_class = AlbumDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)


# album update 图册修改
class AlbumModViews(viewsets.ModelViewSet):
    queryset = Album.objects.filter(visible=True)
    serializer_class = AlbumDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerMod)
