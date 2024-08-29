from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioAssetQuantityViewSet, PortfolioViewSet, AssetViewSet, PriceViewSet

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'prices', PriceViewSet) 
router.register(r'portfolio-quantities', PortfolioAssetQuantityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
