from django.shortcuts import render
from rest_framework import permissions, mixins, generics, viewsets, filters, pagination
from django_filters import rest_framework

from community import serializers
from community import models
from utils.pagination import MyPagination
from utils.permissions import IsOwnerRetrieveUpdate, IsOwnerOrTopLevelUpdate


# update 这里是逻辑删除review
class ReviewUpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Review.objects.filter(visible=True)
    serializer_class = serializers.ReviewModSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrTopLevelUpdate)


# 这个是创建review/retrieve_review
class ReviewCreateRetrieveView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


# list review
class ReviewListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Review.objects.filter(visible=True)
    serializer_class = serializers.ReviewListSerializer
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ("user", "album")
    ordering_fields = ("add_date", "id")
    pagination_class = MyPagination


# list/retrieve/create reply
class ReplyListCreateDetailView(mixins.RetrieveModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
    queryset = models.Reply.objects.filter(visible=True)
    serializer_class = serializers.ReplyCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.OrderingFilter, rest_framework.DjangoFilterBackend)
    ordering_fields = ("add_date", "id")
    filter_fields = ("user", "review", "add_date")


# update reply
class ReplyUpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Reply.objects.all()
    serializer_class = serializers.ReplyModSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerRetrieveUpdate)