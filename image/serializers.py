from rest_framework import serializers

from image.models import Picture, Album


class AlbumListSerializer(serializers.ModelSerializer):
    """图册list"""
    def to_representation(self, instance):
        ret = super(AlbumListSerializer, self).to_representation(instance)
        ret["picture"] = instance.pictures.first().url

    class Meta:
        model = Album
        fields = ("id", "name", "brief", "add_date")


class AlbumDetailSerializer(serializers.ModelSerializer):
    """图册详情"""
    class Meta:
        model = Album
        fields = ("id", "name", "brief", "pictures", "add_date")


class AlbumCreateSerializer(serializers.ModelSerializer):

    # pictures = serializers.ManyRelatedField(Picture, allow_null=True, required=False)

    """图册详情"""
    class Meta:
        model = Album
        fields = ("name", "brief", "user")


class PictureSerializer(serializers.ModelSerializer):
    """create 图片"""
    class Meta:
        model = Picture
        fields = "__all__"
