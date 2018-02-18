from image import views
from django.conf.urls import url
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"albums", views.AlbumListView)
router.register(r"album-mod", views.AlbumModView)
router.register(r"picture", views.PictureCreateView)

urlpatterns = [
    url(r"^index/$", views.index),
    url(r"^index1/$", views.index1),
    url(r"^upload-pic/$", views.upload_pic),
    url(r"^album-page/(\d+)/(\d+)/$", views.album_page),
    # url(r"^album-page/(\d+)/$", views),
]
urlpatterns += router.urls
