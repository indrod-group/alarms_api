from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DetailViewSet, UserViewSet

router = DefaultRouter()
router.register(r'details', DetailViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
