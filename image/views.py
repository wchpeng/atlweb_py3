from django.shortcuts import render
from rest_framework import permissions, mixins, generics, viewsets, filters, status
from rest_framework.response import Response
from django_filters import rest_framework
from django.contrib.auth.models import User
from django.db.models import F
from django.db import transaction
from django.http.response import JsonResponse
from datetime import datetime
from PIL import Image

from image.models import Picture, Album, FavoriteAlbum
from image.serializers import AlbumListSerializer, AlbumDetailSerializer, PictureSerializer
from utils.permissions import IsOwnerRetrieveUpdate
from utils.image_utils import transform_datetime_to_timestamp, handle_upload_pic
from image.models import album_favorite_count, album_review_count


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
        serializer = self.get_serializer(data)
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
    qs = Album.objects.filter(visible=True).order_by("-add_date").select_related("user__userinfo").\
        annotate(username=F("user__userinfo__username")).only(
        "username",
        "name",
        "brief",
        "add_date"
    )
    data = qs.values("id", "username", "name", "brief", "add_date")
    transform_datetime_to_timestamp(data)
    # 增加第一张图片，如果没有就给一张默认值
    qs2 = Album.objects.filter(visible=True).order_by("-add_date").prefetch_related("pictures")
    for i, q in enumerate(qs2):
        pic = q.pictures.first()
        if pic:
            data[i]["first_pic"] = pic.picture.name
        else:
            data[i]["first_pic"] = "default_album.png"

    album_favorite_count(data)
    album_review_count(data)
    now = datetime.now()

    # return JsonResponse(list(data), safe=False)
    return render(request, "image/index.html", {"data": data, "now": now})


def index1(request):
    qs = Album.objects.filter(visible=True).order_by("-add_date").select_related("user__userinfo").\
        annotate(username=F("user__userinfo__username")).only(
        "username",
        "name",
        "brief",
        "add_date"
    )
    data = qs.values("id", "username", "name", "brief", "add_date")
    transform_datetime_to_timestamp(data)
    # 增加第一张图片，如果没有就给一张默认值
    qs2 = Album.objects.filter(visible=True).order_by("-add_date").prefetch_related("pictures")
    for i, q in enumerate(qs2):
        pic = q.pictures.first()
        if pic:
            data[i]["first_pic"] = pic.picture.name
        else:
            data[i]["first_pic"] = "default_album.png"

    album_favorite_count(data)
    album_review_count(data)
    now = datetime.now()

    return JsonResponse(list(data), safe=False)
    # return render(request, "image/index.html", {"data": data, "now": now})


def upload_pic(request):
    """上传图片"""
    pic = request.FILES["picture"]
    album_id = request.POST.get("album", "")
    brief = request.POST.get("brief", "")
    album = Album.objects.get(id=album_id)

    if not album_id:
        return JsonResponse({"detail": "id缺失"})

    with transaction.atomic():
        pic = handle_upload_pic(pic)
        p = Picture(
            brief=brief,
            picture=pic,
            user=request.user
        )
        album.pictures.add(p)

    return JsonResponse({"detail": True})


def album_page(request, user_id, album_id):
    user = User.objects.get(id=user_id)
    album = Album.objects.get(id=album_id)
    qs = Album.objects.filter(user=user).only("id", "name")
    if user.id == request.user.id:
        owner = True
    else:
        owner = False
    return render(request, "image/album_page.html", {"qs": qs, "owner": owner, "album_id": int(album_id), "album_pictures": album.pictures.all()})
