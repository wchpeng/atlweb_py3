from rest_framework import permissions


class IsOwnerMod(permissions.BasePermission):
    """判断request的user是否是这个相册的user"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
