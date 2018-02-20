from django.db import models
from django.contrib.auth.models import User

from db.base_model import BaseModel


class FollowUser(BaseModel):
    mark = models.CharField(max_length=10, null=True, blank=True, verbose_name="备注")
    to_user = models.ForeignKey(User, related_name="follow_to", on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name="follow_from", on_delete=models.CASCADE)

    def __str__(self):
        return "{} to {}".format(self.from_user.username, self.to_user.username)

    class Meta:
        unique_together = (("from_user", "to_user"),)
        ordering = ("-id",)


class BlackUser(BaseModel):
    mark = models.CharField(max_length=10, null=True, blank=True, verbose_name="备注")
    to_user = models.ForeignKey(User, related_name="black_to", on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name="black_from", on_delete=models.CASCADE)

    def __str__(self):
        return "{} to {}".format(self.from_user.username, self.to_user.username)

    class Meta:
        unique_together = (("from_user", "to_user"),)
        ordering = ("-id",)


# 自己写的几个函数
def follow_count(user_id):
    """我关注的人的数量"""
    return FollowUser.objects.filter(visible=True, from_user_id=user_id).count()


def followed_count(user_id):
    """关注我的人的数量"""
    return FollowUser.objects.filter(visible=True, to_user_id=user_id).count()


def black_count(user_id):
    """我拉黑的人的数量"""
    return BlackUser.objects.filter(visible=True, from_user_id=user_id).count()


def blacked_count(user_id):
    """拉黑我的人的数量"""
    return BlackUser.objects.filter(visible=True, to_user_id=user_id).count()


