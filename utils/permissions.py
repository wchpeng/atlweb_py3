from rest_framework import permissions


class IsOwnerRetrieveUpdate(permissions.BasePermission):
    """只有user是request.user才能update/retrieve"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrTopLevelUpdate(permissions.BasePermission):
    """只有图册主人或者图片主人或发布人才能删除review"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user == obj.album.user or request.user == obj.picture.user
