from image import views
from django.conf.urls import url
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"album-list", views.AlbumListSerializer)
router.register(r"album-detail", views.AlbumDetailSerializer)
router.register(r"album-mod", views.AlbumModViews)

urlpatterns = []
urlpatterns += router.urls
