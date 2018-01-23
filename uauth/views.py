from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from rest_framework.decorators import api_view, permission_classes
import re

from uauth.models import UserInfo
from utils.uauth import create_user


# 登陆
@require_http_methods(["GET", "POST"])
def log_in(request):
    if request.method == "GET":
        return render(request, "uauth/login.html")
    else:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return render(request, "uauth/index.html", {"status": "登陆"})
        return render(request, "uauth/login.html", {"detail": "账号或密码错误"})


# 注册
@require_POST
def register(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    if not re.match(r'^[a-zA-Z0-9]\w{8,}$', username):
        return JsonResponse({"detail": "用户名不合规范"})
    if all([username, password]):
        try:
            user = create_user(username=username, password=password)
        except IntegrityError:
            return JsonResponse({"detail": "用户名已存在"})
        login(request, user)
        return render(request, "uauth/index.html", {"status": "注册"})
    return JsonResponse({"detail": "用户名或者密码不能为空"})


@login_required(login_url="/uauth/login/")
@require_POST
def log_out(request):
    logout(request.user)
    return redirect("/uauth/login/")


@login_required(login_url="/uauth/login")
def index(request):
    return render(request, "uauth/index.html", {"status": "再次进入"})





