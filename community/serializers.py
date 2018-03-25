from rest_framework import serializers

from community.models import Reply, Review, Blog
from community.utils import ridding_html_tag


class ReplyDetailSerializer(serializers.ModelSerializer):
    """retrieve"""
    class Meta:
        model = Reply
        fields = ("id", "content", "add_date")


class ReplyModSerializer(serializers.ModelSerializer):
    """update"""
    class Meta:
        model = Reply
        fields = ("id", "visible")


class ReplyCreateSerializer(serializers.ModelSerializer):
    """create"""
    class Meta:
        model = Reply
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    """list"""
    class Meta:
        model = Review
        fields = ("id", "content", "add_date", "album")


class ReviewModSerializer(serializers.ModelSerializer):
    """update"""
    class Meta:
        model = Review
        fields = ("id", "visible")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """create"""
    class Meta:
        model = Review
        fields = "__all__"


class BlogDetailSerializer(serializers.ModelSerializer):
    """blog detail"""
    def to_representation(self, instance):
        ret = super(BlogDetailSerializer, self).to_representation(instance)
        ret["username"] = instance.user.userinfo.username
        return ret

    class Meta:
        model = Blog
        fields = ("title", "content", "add_date")


class BlogListSerializer(serializers.ModelSerializer):
    """blog list"""
    def to_representation(self, instance):
        ret = super(BlogListSerializer, self).to_representation(instance)
        ret["content"] = ridding_html_tag(ret["content"], 50)
        ret["liked_count"] = instance.liked_count
        ret["reviewed_count"] = 5
        return ret

    class Meta:
        model = Blog
        fields = ("id", "title", "content")
