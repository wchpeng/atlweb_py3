from rest_framework import routers

from community import views


router = routers.SimpleRouter()
router.register(r"mod-reply", views.ReplyUpdateView)
router.register(r"replies", views.ReplyListCreateDetailView)

router.register(r"mod-review", views.ReviewUpdateView)
router.register(r"reviews", views.ReviewListView)
router.register(r"review", views.ReviewCreateRetrieveView)

urlpatterns = []
urlpatterns += router.urls
