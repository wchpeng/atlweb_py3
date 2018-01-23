from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    visible = models.BooleanField(default=True, verbose_name="是否可见")
    mod_date = models.DateTimeField(auto_now=True, verbose_name="更新日期")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    class Meta:
        abstract = True
