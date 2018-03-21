from django.shortcuts import render
from rest_framework import permissions, mixins, generics, viewsets, filters, pagination
from django_filters import rest_framework
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count

from community import serializers, models
from community.utils import select_page_range
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


def all_blog(request):
    """所有的blogs页"""
    page = int(request.GET.get("page", "1"))

    all_blog = models.Blog.objects.filter(visible=True).order_by("-id")
    all_category = models.BlogCategory.objects\
        .filter(visible=True)\
        .annotate(blog_nums=Count("blog"))\
        .order_by("-blog_nums")

    blog_paginator = Paginator(all_blog, settings.BLOG_PER_PAGE)
    blogs = blog_paginator.get_page(page)
    blog_pages = select_page_range(list(blog_paginator.page_range), page)

    ret = {
        "all_category": all_category,
        "blogs": blogs,
        "blog_pages": blog_pages,
        "random_class": ["success", "info", "warning", "danger"]
    }

    return render(request, "blog/all_blog.html", ret)


def my_blog(request):
    """我的blogs页"""
    page = int(request.GET.get("page", "1"))

    all_blog = models.Blog.objects.filter(visible=True, user=request.user).order_by("-id")
    all_category = models.BlogCategory.objects\
        .filter(visible=True, user=request.user)\
        .annotate(blog_nums=Count("blog"))\
        .order_by("-blog_nums")

    blog_paginator = Paginator(all_blog, settings.BLOG_PER_PAGE)
    blogs = blog_paginator.get_page(page)
    blog_pages = select_page_range(list(blog_paginator.page_range), page)

    ret = {
        "all_category": all_category,
        "blogs": blogs,
        "blog_pages": blog_pages,
        "random_class": ["success", "info", "warning", "danger"]
    }

    return render(request, "blog/my_blog.html", ret)


def his_blog(request, user_id):
    page = int(request.GET.get("page", "1"))

    all_blog = models.Blog.objects.filter(visible=True, user_id=user_id).order_by("-id")
    all_category = models.BlogCategory.objects\
        .filter(visible=True, user_id=user_id)\
        .annotate(blog_nums=Count("blog"))\
        .order_by("-blog_nums")

    blog_paginator = Paginator(all_blog, settings.BLOG_PER_PAGE)
    blogs = blog_paginator.get_page(page)
    blog_pages = select_page_range(list(blog_paginator.page_range), page)

    ret = {
        "all_category": all_category,
        "blogs": blogs,
        "blog_pages": blog_pages,
        "random_class": ["success", "info", "warning", "danger"]
    }

    return render(request, "blog/his_blog.html", ret)


def blog_category(request, category_id):
    page = int(request.GET.get("page", "1"))

    all_blog = models.Blog.objects.filter(visible=True, category_id=category_id).order_by("-id")
    all_category = models.BlogCategory.objects.get(id=category_id).user.blogcategory_set\
        .filter(visible=True)\
        .annotate(blog_nums=Count("blog"))\
        .order_by("-blog_nums")

    blog_paginator = Paginator(all_blog, settings.BLOG_PER_PAGE)
    blogs = blog_paginator.get_page(page)
    blog_pages = select_page_range(list(blog_paginator.page_range), page)

    ret = {
        "all_category": all_category,
        "blogs": blogs,
        "blog_pages": blog_pages,
        "random_class": ["success", "info", "warning", "danger"]
    }

    return render(request, "blog/category_blog.html", ret)


def blog_detail(request, blog_id):
    """blog detail"""
    blog = models.Blog.objects.get(id=blog_id)

    ret = {
        "blog": blog,
    }

    return render(request, "blog/blog_detail.html", ret)
