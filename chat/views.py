from django.shortcuts import render
from django.db.models import F
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

from uauth.models import UserInfo
from atlweb_py3.settings import rong_app_key
from social.models import FollowUser, BlackUser


@login_required(login_url="/uauth/login/")
def chat_index(request):
    app_key = rong_app_key
    im_token = request.user.userinfo.im_token
    my_info = {
        "user_id": request.user.id,
        "id": request.user.userinfo.user_hash,
        "avatar": request.user.userinfo.avatar.name,
        "username": request.user.userinfo.username,
    }
    friends_info = FollowUser.objects.filter(from_user_id=request.user.id).\
        annotate(username=F("to_user__userinfo__username"), user_hash=F("to_user__userinfo__user_hash"), avatar=F("to_user__userinfo__avatar")).\
        values("username", "user_hash", "avatar")
    blacks_info = BlackUser.objects.filter(from_user_id=request.user.id). \
        annotate(username=F("to_user__userinfo__username"), user_hash=F("to_user__userinfo__user_hash"), avatar=F("to_user__userinfo__avatar")). \
        values("username", "user_hash", "avatar")
    ret = {
        "my_info": my_info,
        "app_key": app_key,
        "im_token": im_token,
        "blacks_info": blacks_info,
        "friends_info": friends_info,
    }
    return render(request, "chat/chat_ok.html", ret)

























# @login_required(login_url="/uauth/login/")
# def we_chat(request):
#     info = UserInfo.objects.filter(user=request.user).values("username", "user_hash")
#     return render(request, "we_chat/my_friends.html", info[0])
#     # return JsonResponse(info[0])
#
#
# @login_required(login_url="/uauth/login/")
# def we_chat2(request):
#     info = UserInfo.objects.filter(user=request.user).values("username", "user_hash")
#     return render(request, "we_chat/index.html", info[0])
#     # return JsonResponse(info[0])