import re
import json

from django.contrib import messages
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, models
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, generics, permissions, viewsets, filters

from uauth.tasks import send_email
from uauth.models import UserInfo, create_user
from uauth.serializers import UserInfoDetailSerializer, UserInfoListSerializer, UserInfoRetrieveSerializer
from utils.permissions import IsOwnerRetrieveUpdate
from image.models import get_albums_data_info, get_favorite_albums_data_info, get_albums_count, Album
from social.models import followed_count, follow_count


# 登陆
@require_http_methods(["GET", "POST"])
def log_in(request):
    if request.method == "GET":
        return render(request, "uauth/login.html", {"error": False})
    else:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # request.session.set_expiry(300)
            messages.info(request, "登陆")
            return redirect(index)
        return render(request, "uauth/login.html", {"error": True, "detail": "账号或密码错误"})


# 注册
@require_POST
def register(request):
    email = request.POST.get("email", "")
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    if not re.match(r'^[a-zA-Z0-9]\w{7,}$', username):
        return JsonResponse({"detail": "用户名不合规范"})
    if all([username, password, email]):
        try:
            user = create_user(username=username, password=password, email=email)
        except IntegrityError:
            return JsonResponse({"detail": "用户名已存在"})
        login(request, user)
        request.session.set_expiry(300)
        messages.info(request, "注册")
        return redirect(index)
    return JsonResponse({"detail": "用户名或者密码不能为空"})


# 登出
@login_required(login_url="/uauth/login/")
@require_GET
def log_out(request):
    logout(request)
    return redirect("/uauth/login/")


# 登陆后首页
@login_required(login_url="/uauth/login")
def index(request):
    # print(request.session["_auth_user_id"])
    return render(request, "uauth/index.html")


# 判断用户名和email是否存在
def exist_username_email(request):
    kwargs = dict(request.GET)
    for i in kwargs.keys():
        kwargs[i] = kwargs[i][0]
    try:
        models.User.objects.get(**kwargs)
    except models.User.DoesNotExist:
        return JsonResponse({"error": False})
    else:
        return JsonResponse({"error": True})


# 测试发送邮件
@api_view(["POST"])
def test_send_email(request):
    to_email = request.data.get("to_email", "")
    subject = request.data.get("subject", "")
    message = request.data.get("message", "")
    html_message = request.data.get("html_message", "")

    print(to_email, subject, message)

    if to_email:
        ret = send_email.delay(to_email=to_email, subject=subject, message=message, html_message=html_message)
        return JsonResponse({"detail": str(ret)})
    return JsonResponse({"detail": "to_email is None."})


# 用户详情
class UserInfoDetail(generics.RetrieveUpdateAPIView, viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerRetrieveUpdate)
    serializer_class = UserInfoDetailSerializer


# 用户列表
class UserInfoList(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoRetrieveSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserInfoListSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


@login_required(login_url="/uauth/login/")
def my_info_page(request):
    user = request.user
    user_info = UserInfo.objects.filter(user=user).values("user_id", "signature", "username", "avatar")[0]
    user_info["follow"] = follow_count(user.id)
    user_info["followed"] = followed_count(user.id)
    user_info["albums_count"] = get_albums_count(user.id)

    qs = Album.objects.filter(user=user).only("id", "name")
    current_path = request.get_full_path()
    albums_data = get_albums_data_info(user=user)
    fav_albums_data = get_favorite_albums_data_info(user.id)

    ret = {
        "qs": qs,
        "owner": True,
        "user_info": user_info,
        "albums_data": albums_data,
        "current_path": current_path,
        "fav_albums_data": fav_albums_data
    }

    return render(request, "uauth/user_info.html", ret)
    # return JsonResponse(ret)


@login_required(login_url="/uauth/login/")
def his_info_page(request, username):
    user = UserInfo.objects.get(username=username).user
    # user = models.User.objects.get(id=user_id)
    user_info = UserInfo.objects.filter(user=user).values("user_id", "signature", "username", "avatar")[0]
    user_info["follow"] = follow_count(user.id)
    user_info["followed"] = followed_count(user.id)
    user_info["albums_count"] = get_albums_count(user.id)

    albums_data = get_albums_data_info(user_id=user.id)
    # fav_albums_data = get_favorite_albums_data_info(user.id)

    ret = {
        "owner": False,
        "user_info": user_info,
        "albums_data": albums_data,
        # "fav_albums_data": fav_albums_data
    }

    # return render(request, "uauth/user_info.html", ret)
    return JsonResponse(ret)
