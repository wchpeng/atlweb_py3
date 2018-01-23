from django.db import models
from django.contrib.auth.models import User

from db.base_model import BaseModel


class UserInfo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.BooleanField(default=1, verbose_name="性别")
    user_hash = models.CharField(max_length=40, verbose_name="唯一标示")
    birthday = models.DateTimeField(verbose_name="生日", null=True, blank=True)
    mark = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="评分")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="地址")
    signature = models.CharField(max_length=50, null=True, blank=True, verbose_name="签名")
    username = models.CharField(max_length=12, null=True, blank=True, verbose_name="用户名")
    avatar = models.ImageField(upload_to="avatar", default="default_avatar.png", verbose_name="头像")

    def __str__(self):
        return "{} {}".format(self.id, self.username)

    class Meta:
        ordering = ("-id",)
