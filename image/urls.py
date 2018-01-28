from image import views
from django.conf.urls import url
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"albums", views.AlbumListView)
router.register(r"album-mod", views.AlbumModView)
router.register(r"picture", views.PictureCreateView)

urlpatterns = []
urlpatterns += router.urls
