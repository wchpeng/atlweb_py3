from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from rest_framework import permissions, mixins, generics, viewsets
from db.base_model import BaseModel
from image.models import Album, Picture


class Blog(BaseModel):
    """blog"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    content = RichTextUploadingField()

    def __str__(self):
        return "{} {}".format(self.id, self.title[:10])

    class Meta:
        ordering = ("-id",)


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=512, verbose_name="内容")
    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.CASCADE, verbose_name="图册")
    picture = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.CASCADE, verbose_name="图片")

    # def to_detail(self):
    #     reply = []

    def __str__(self):
        return "{} {}".format(self.id, self.content[:8])

    class Meta:
        verbose_name_plural = "评论"
        ordering = ("-id",)


class Reply(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=512, verbose_name="内容")
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    source = models.ForeignKey("self", null=True, blank=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.id, self.content[:8])

    class Meta:
        verbose_name_plural = "回复"
        ordering = ("-id",)