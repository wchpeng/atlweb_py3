from rest_framework import serializers

from image.models import Picture, Album


class AlbumListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(AlbumListSerializer, self).to_representation(instance)
        ret["picture"] = instance.pictures.first().url

    class Meta:
        model = Album
        fields = ("id", "brief", "date_added")


class AlbumDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ("id", "brief", "pictures", "date_added")