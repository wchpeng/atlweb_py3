from rest_framework import serializers

from uauth.models import UserInfo


class UserInfoDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = "__all__"
        read_only = ("id", "user", "user_hash")


class UserInfoRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ("id", "gender", "signature", "username", "avatar", "birthday")


class UserInfoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ("id", "user", "gender", "signature", "username", "avatar", "birthday")