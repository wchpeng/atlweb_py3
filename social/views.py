from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, generics, viewsets, permissions, filters

from social.models import FollowUser, BlackUser
from social.serializers import FollowSerializer, BlackSerializer
from utils.pagination import MyPagination
from utils.permissions import IsOwnerRetrieveUpdate


class FollowView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = FollowUser.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerRetrieveUpdate)
    pagination_class = MyPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("to_user__userinfo__username", "mark")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(from_user=request.user, visible=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BlackView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = BlackUser.objects.filter(visible=True)
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerRetrieveUpdate)
    pagination_class = MyPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("to_user__user__userinfo__username", "mark")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(from_user=request.user, visible=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
