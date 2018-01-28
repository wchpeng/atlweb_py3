from django.contrib.auth.models import User
from django.db import models

from db.base_model import BaseModel
from utils.image_utils import picture_upload_path


class Picture(BaseModel):
    brief = models.CharField(max_length=156, verbose_name="描述")
    picture = models.ImageField(upload_to=picture_upload_path, verbose_name="相册图片")

    def __str__(self):
        return "{} {}".format(self.id, self.brief[:8])


class Album(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brief = models.CharField(max_length=64, verbose_name="描述")
    pictures = models.ManyToManyField(Picture, verbose_name="相册图片")
    name = models.CharField(max_length=16, unique=True, verbose_name="图册名字")

    def __str__(self):
        return "{} {}".format(self.id, self.name)
