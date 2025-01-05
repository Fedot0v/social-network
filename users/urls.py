from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, ProfileViewSet


router = DefaultRouter()
router.register("users", UserViewSet)
router.register("profiles", ProfileViewSet)

urlpatterns = router.urls

app_name = "users"
