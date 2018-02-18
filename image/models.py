from django.contrib.auth.models import User
from django.db import models
# from django_thumbs.db.models import ImageWithThumbsField

from db.base_model import BaseModel
from utils.image_utils import picture_upload_path


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


class FavoriteAlbum(BaseModel):
    """收藏相册"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.userinfo.username, self.album.name)

    class Meta:
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
