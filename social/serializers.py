from rest_framework import serializers

from social.models import FollowUser, BlackUser


class FollowSerializer(serializers.ModelSerializer):
    """关注序列化"""
    def to_representation(self, instance):
        ret = super(FollowSerializer, self).to_representation(instance)
        ret["username"] = instance.to_user.userinfo.username
        ret["avatar"] = instance.to_user.userinfo.avatar.url
        ret["signature"] = instance.to_user.userinfo.signature
        ret["user_hash"] = instance.to_user.userinfo.user_hash
        return ret

    class Meta:
        model = FollowUser
        fields = ("from_user", "to_user", "mark")


class BlackSerializer(serializers.ModelSerializer):
    """拉黑序列化"""
    class Meta:
        model = FollowUser
        fields = ("from_user", "to_user", "mark")
