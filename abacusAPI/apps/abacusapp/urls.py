from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet, AssetViewSet

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'assets', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]