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
