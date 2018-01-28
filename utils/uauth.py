from uauth.models import UserInfo
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.authtoken.models import Token
import hashlib
import time


# 加密
def get_user_hash(val):
    sha1 = hashlib.sha1()
    sha1.update((str(val)+str(time.time())).encode())
    return sha1.hexdigest()


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


def avatar_upload_path(instance, filename):
    suffix = filename[filename.rfind("."):]
    return "{}/{}{}".format(instance.userinfo.user_hash, get_user_hash(filename), suffix)

