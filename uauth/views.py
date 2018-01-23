from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from rest_framework.decorators import api_view, permission_classes
import re

from uauth.models import UserInfo
from utils.uauth import create_user, send_email


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
            messages.info(request, "登陆")
            return redirect(index)
        return render(request, "uauth/login.html", {"detail": "账号或密码错误"})


# 注册
@require_POST
def register(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    if not re.match(r'^[a-zA-Z0-9]\w{7,}$', username):
        return JsonResponse({"detail": "用户名不合规范"})
    if all([username, password]):
        try:
            user = create_user(username=username, password=password)
        except IntegrityError:
            return JsonResponse({"detail": "用户名已存在"})
        login(request, user)
        messages.info(request, "注册")
        return redirect(index)
    return JsonResponse({"detail": "用户名或者密码不能为空"})


@login_required(login_url="/uauth/login/")
@require_GET
def log_out(request):
    logout(request)
    return redirect("/uauth/login/")


@login_required(login_url="/uauth/login")
def index(request):
    return render(request, "uauth/index.html")


# 测试发送邮件
# @api_view(["POST"])
# def test_send_email(request):
#     to_email = request.data.get("to_email", "")
#     subject = request.data.get("subject", "")
#     message = request.data.get("message", "")
#     html_message = request.data.get("html_message", "")
#
#     print(to_email, subject, message)
#
#     if to_email:
#         ret = send_email(to_email=to_email, subject=subject, message=message, html_message=html_message)
#         return JsonResponse({"detail": str(ret)})
#     return JsonResponse({"detail": "to_email is None."})





