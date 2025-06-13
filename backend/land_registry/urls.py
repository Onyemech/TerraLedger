from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import LandViewSet

router = DefaultRouter()
router.register(r'lands', LandViewSet, basename='land')

urlpatterns = [
    path('api/', include(router.urls)),
]