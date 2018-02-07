from django.conf.urls import url
from rest_framework import routers

from social import views

router = routers.SimpleRouter()
router.register(r"follows", views.FollowView)
router.register(r"blacks", views.BlackView)


urlpatterns = []
urlpatterns += router.urls
