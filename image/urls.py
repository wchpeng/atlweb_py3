from image import views
from django.conf.urls import url
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"albums", views.AlbumListView)
router.register(r"album-mod", views.AlbumModView)
router.register(r"picture", views.PictureCreateView)

urlpatterns = [
    url(r"^index/$", views.index),                                # 图片主页
    url(r"^index1/$", views.index1),                              # 图片主页数据
    url(r"^upload-pic/$", views.upload_pic),                      # 上传图片页面，自动切图
    url(r"^search-index/$", views.search_index),                  # 搜索页面数据
    url(r"^album-page/(.+?)/(\d+)/$", views.album_detail_page),   # 图册页
    # url(r"^album-page/(\d+)/$", views),
]
urlpatterns += router.urls
