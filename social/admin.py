from django.contrib import admin

from social.models import FollowUser, BlackUser

admin.site.register(BlackUser)
admin.site.register(FollowUser)
