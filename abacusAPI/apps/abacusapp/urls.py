from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet, AssetViewSet, PriceViewSet

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'prices', PriceViewSet) 

urlpatterns = [
    path('', include(router.urls)),
]