from django.shortcuts import render
from rest_framework import permissions, mixins, generics, viewsets, filters
from rest_framework.response import Response
from django_filters import rest_framework

from image.models import Picture, Album
from image.serializers import AlbumListSerializer, AlbumDetailSerializer, PictureSerializer
from utils.permissions import IsOwnerRetrieveUpdate


# album list 显示
class AlbumListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Album.objects.filter(visible=True).order_by("add_date")
    serializer_class = AlbumListSerializer
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ("user",)
    ordering_fields = ("add_date", )
    search_fields = ("brief", "name")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 保存latest_album
        if request.user.id == instance.user.id:
            request.user.latest_album = instance.name
            request.user.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# album update 图册修改
class AlbumModView(viewsets.ModelViewSet):
    queryset = Album.objects.filter(visible=True)
    serializer_class = AlbumDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerRetrieveUpdate)


class PictureCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """create 图片"""
    queryset = Picture.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PictureSerializer
