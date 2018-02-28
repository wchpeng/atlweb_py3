from django import forms
from uauth.models import UserInfo


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ("username", "signature", "birthday", "gender", "avatar")
