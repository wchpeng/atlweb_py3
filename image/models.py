from django.contrib.auth.models import User
from django.db import models
# from django_thumbs.db.models import ImageWithThumbsField

from utils.image_utils import picture_upload_path, transform_datetime_to_timestamp, mod_dict_key
from db.base_model import BaseModel


class Picture(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brief = models.CharField(max_length=156, verbose_name="描述")
    # picture = ImageWithThumbsField(upload_to=picture_upload_path, verbose_name="相册图片", sizes=((300, 300),))
    picture = models.ImageField(upload_to=picture_upload_path, verbose_name="相册图片")

    def __str__(self):
        return "{} {}".format(self.id, self.brief[:8])


class Album(BaseModel):
    ALBUM_CATEGORY = ((1, "多相册"), (2, "单相册"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.PositiveSmallIntegerField(choices=ALBUM_CATEGORY, null=True, default=1, verbose_name="相册类型")
    name = models.CharField(max_length=16, unique=True, verbose_name="图册名字")
    brief = models.CharField(max_length=64, verbose_name="描述")
    pictures = models.ManyToManyField(Picture, blank=True, verbose_name="相册图片")

    def __str__(self):
        return "{} {}".format(self.id, self.name)

    class Meta:
        ordering = ("-add_date",)


class FavoriteAlbum(BaseModel):
    """收藏相册"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.userinfo.username, self.album.name)

    class Meta:
        ordering = ("-add_date",)
        unique_together = (("user", "album"),)


class FavoritePicture(BaseModel):
    """收藏图片"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.userinfo.username, self.picture.brief[:5])

    class Meta:
        unique_together = (("user", "picture"),)


# 写几个函数方法
from community.models import Review


def album_favorite_count(data):
    """给data添加收藏数favorite_count"""
    for temp in data:
        a_f_c = FavoriteAlbum.objects.filter(album_id=temp["id"]).count()
        temp["favorite_count"] = a_f_c


def album_review_count(data):
    """给data增加回复数review_count"""
    for temp in data:
        a_r_c = Review.objects.filter(album_id=temp["id"]).count()
        temp["review_count"] = a_r_c


def album_pic_count(data):
    """给data中添加图册的图片数量"""
    for temp in data:
        p_c = Album.objects.get(id=temp["id"]).pictures.count()
        temp["pic_count"] = p_c


def get_albums_data_index(**kwargs):
    """通过一些条件**kwargs来求取albums数据 主页专用"""
    data = Album.objects.filter(visible=True, **kwargs).order_by("-add_date").select_related("user__userinfo").\
        annotate(username=models.F("user__userinfo__username")).values("id", "username", "name", "brief", "add_date")
    transform_datetime_to_timestamp(data)
    # 增加第一张图片，如果没有就给一张默认值
    qs2 = Album.objects.filter(visible=True, **kwargs).order_by("-add_date").prefetch_related("pictures")
    for i, q in enumerate(qs2):
        pic = q.pictures.first()
        if pic:
            data[i]["first_pic"] = pic.picture.name
        else:
            data[i]["first_pic"] = "default_album.png"

    album_review_count(data)
    album_favorite_count(data)

    return list(data)


def get_albums_data_search_index(keyword):
    """通过一些条件**kwargs来求取albums数据 主页专用"""
    data = Album.objects.filter(models.Q(name__icontains=keyword) | models.Q(brief__icontains=keyword), visible=True)\
        .order_by("-add_date").select_related("user__userinfo")\
        .annotate(username=models.F("user__userinfo__username")).values("id", "username", "name", "brief", "add_date")
    transform_datetime_to_timestamp(data)
    # 增加第一张图片，如果没有就给一张默认值
    qs2 = Album.objects.filter(models.Q(name__icontains=keyword) | models.Q(brief__icontains=keyword), visible=True)\
        .order_by("-add_date").prefetch_related("pictures")
    for i, q in enumerate(qs2):
        pic = q.pictures.first()
        if pic:
            data[i]["first_pic"] = pic.picture.name
        else:
            data[i]["first_pic"] = "default_album.png"

    album_review_count(data)
    album_favorite_count(data)

    return list(data)


def get_favorite_albums_data_index(user_id):
    """通过一些条件**kwargs来求取albums数据 主页专用"""
    data = FavoriteAlbum.objects.filter(visible=True, user_id=user_id).order_by("-add_date").\
        select_related("album", "album__user__userinfo"). \
        annotate(
            username=models.F("album__user__userinfo__username"),
            name=models.F("album__name"),
            brief=models.F("album__brief"),
        ).values("album_id", "username", "name", "brief", "album__add_date")
    mod_dict_key(data)
    transform_datetime_to_timestamp(data)
    # 增加第一张图片，如果没有就给一张默认值
    qs2 = FavoriteAlbum.objects.filter(visible=True, user_id=user_id).order_by("-add_date").prefetch_related("album__pictures")
    for i, q in enumerate(qs2):
        pic = q.album.pictures.first()
        if pic:
            data[i]["first_pic"] = pic.picture.name
        else:
            data[i]["first_pic"] = "default_album.png"

    album_review_count(data)
    album_favorite_count(data)

    return list(data)


def get_albums_data_info(**kwargs):
    """通过一些条件**kwargs来求取albums数据 专门让info页使用"""
    data = Album.objects.filter(visible=True, **kwargs).order_by("-add_date").select_related("user__userinfo").\
        annotate(username=models.F("user__userinfo__username")).values("id", "username", "name", "brief")
    transform_datetime_to_timestamp(data)
    # 增加第一张图片，如果没有就给一张默认值
    qs2 = Album.objects.filter(visible=True, **kwargs).order_by("-add_date").prefetch_related("pictures")
    for i, q in enumerate(qs2):
        pic = q.pictures.first()
        if pic:
            data[i]["first_pic"] = pic.picture.name
        else:
            data[i]["first_pic"] = "default_album.png"

    album_pic_count(data)
    album_favorite_count(data)

    return list(data)


def get_favorite_albums_data_info(user_id):
    """通过一些条件**kwargs来求取albums数据 专门让info页使用"""
    data = FavoriteAlbum.objects.filter(visible=True, user_id=user_id).order_by("-add_date").\
        select_related("album", "album__user__userinfo"). \
        annotate(
            username=models.F("album__user__userinfo__username"),
            name=models.F("album__name"),
            brief=models.F("album__brief"),
        ).values("album_id", "username", "name", "brief")
    mod_dict_key(data)
    transform_datetime_to_timestamp(data)
    # 增加第一张图片，如果没有就给一张默认值
    qs2 = FavoriteAlbum.objects.filter(visible=True, user_id=user_id).order_by("-add_date").prefetch_related("album__pictures")
    for i, q in enumerate(qs2):
        pic = q.album.pictures.first()
        if pic:
            data[i]["first_pic"] = pic.picture.name
        else:
            data[i]["first_pic"] = "default_album.png"

    album_pic_count(data)
    album_favorite_count(data)

    return list(data)























def get_albums_count(user_id):
    """获取某用户id，他的相册数量"""
    return Album.objects.filter(visible=True, user_id=user_id).count()
