from rest_framework import serializers

from community.models import Reply, Review


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


