from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, PortfolioAssetViewSet, PortfolioViewSet, AssetViewSet, PriceViewSet, UploadExcelView

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'portfolios/(?P<portfolio_id>\d+)/assets', PortfolioAssetViewSet, basename='portfolio-details')
router.register(r'assets', AssetViewSet)
router.register(r'prices', PriceViewSet) 
router.register(r'portfolio-assets', PortfolioAssetViewSet)
router.register(r'deposits', DepositViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-excel/', UploadExcelView.as_view(), name='upload-excel'),
]
