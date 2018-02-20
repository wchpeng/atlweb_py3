from django.shortcuts import render, redirect
from rest_framework import permissions, mixins, generics, viewsets, filters, status
from rest_framework.response import Response
from django_filters import rest_framework
from django.contrib.auth.models import User
from django.db import transaction
from django.http.response import JsonResponse
from datetime import datetime

from uauth.models import UserInfo
from image.models import Picture, Album, FavoriteAlbum, get_albums_data_index, get_albums_data_search_index
from image.serializers import AlbumListSerializer, AlbumDetailSerializer, PictureSerializer, AlbumCreateSerializer
from utils.image_utils import handle_upload_pic
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

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        serializer = AlbumCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PictureCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """create 图片"""
    queryset = Picture.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PictureSerializer


def index(request):
    data = get_albums_data_index()
    now = datetime.now()

    # return JsonResponse(list(data), safe=False)
    return render(request, "image/index.html", {"data": data, "now": now})


def search_index(request):
    keyword = request.GET.get("keyword")
    data = get_albums_data_search_index(keyword[0:15])
    now = datetime.now()

    # return JsonResponse(list(data), safe=False)
    return render(request, "image/index.html", {"data": data, "now": now})


def index1(request):
    data = get_albums_data_index()
    now = datetime.now()

    return JsonResponse(list(data), safe=False)
    # return render(request, "image/index.html", {"data": data, "now": now})


def upload_pic(request):
    """上传图片"""
    pic = request.FILES["picture"]
    album_id = request.POST.get("album", "")
    brief = request.POST.get("brief", "")
    album = Album.objects.get(id=album_id)
    path = request.POST.get("current_path", "")

    if not album_id:
        return JsonResponse({"detail": "id缺失"})

    with transaction.atomic():
        pic = handle_upload_pic(pic)
        p = Picture(
            brief=brief,
            picture=pic,
            user=request.user
        )
        p.save()
        album.pictures.add(p)
        # return
        return redirect(path)
    # return JsonResponse({"detail": "error"})


def album_detail_page(request, username, album_id):
    user = UserInfo.objects.get(username=username).user
    # user = User.objects.get(id=user_id)
    album = Album.objects.get(id=album_id)
    qs = Album.objects.filter(user=user).only("id", "name")
    path = request.get_full_path()
    if user.id == request.user.id:
        owner = True
    else:
        owner = False

    ret = {
        "qs": qs,
        "current_path": path,
        "owner": owner,
        "current_album": album,
        "album_pictures": album.pictures.all()
    }
    return render(request, "image/album_page.html", ret)
