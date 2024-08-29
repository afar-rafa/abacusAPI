from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioAssetViewSet, PortfolioViewSet, AssetViewSet, PriceViewSet

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'prices', PriceViewSet) 
router.register(r'portfolio-assets', PortfolioAssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
