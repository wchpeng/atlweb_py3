from django.contrib.auth.models import User
from django.db import models, transaction
from rest_framework.authtoken.models import Token

from db.base_model import BaseModel
from utils.uauth_utils import avatar_upload_path, get_user_hash


class UserInfo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.BooleanField(default=1, verbose_name="性别")
    user_hash = models.CharField(max_length=40, verbose_name="唯一标示")
    birthday = models.DateTimeField(verbose_name="生日", null=True, blank=True)
    email = models.EmailField(verbose_name="邮箱")
    mark = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="评分")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="地址")
    signature = models.CharField(max_length=50, null=True, blank=True, verbose_name="签名")
    username = models.CharField(max_length=12, null=True, blank=True, verbose_name="用户名")
    avatar = models.ImageField(upload_to=avatar_upload_path, default="default_avatar.png", verbose_name="头像")

    latest_albums = models.CharField(max_length=16, default="我的相册", verbose_name="最近操作的albums")

    def __str__(self):
        return "{} {}".format(self.id, self.username)

    class Meta:
        ordering = ("-id",)


def create_user(**kwargs):
    with transaction.atomic():
        user = User.objects.create_user(**kwargs)
        Token.objects.create(user=user)
        UserInfo.objects.create(
            user=user,
            username=kwargs["username"],
            user_hash=get_user_hash(user.id)
        )
    return user
