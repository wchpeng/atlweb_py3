from rest_framework import routers
from django.conf.urls import url

from community import views

router = routers.SimpleRouter()
router.register(r"mod-reply", views.ReplyUpdateView)
router.register(r"replies", views.ReplyListCreateDetailView)

router.register(r"mod-review", views.ReviewUpdateView)
router.register(r"reviews", views.ReviewListView)
router.register(r"review", views.ReviewCreateRetrieveView)

urlpatterns = [
    url(r'^blog/all-blog/$', views.all_blog),                        # all blog
    url(r'^blog/all-blog-json/$', views.blog_list_json),             # all blog / json
    url(r'^blog/my-blog/$', views.my_blog),                          # my blog
    url(r'^blog/his-blog/(\d+)/$', views.his_blog),                  # his blog
    url(r'^blog/blog-category/(\d+)/$', views.blog_category),        # category blog
    url(r'^blog/blog-detail/(\d+)/$', views.blog_detail),            # blog detail
    url(r'^blog/blog-detail-json/(\d+)/$', views.blog_detail_json),  # blog detail / json
]

urlpatterns += router.urls
