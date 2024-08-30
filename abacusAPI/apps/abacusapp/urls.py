from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, PortfolioAssetViewSet, PortfolioViewSet, AssetViewSet, PriceViewSet, TransactionViewSet, UploadExcelView

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'prices', PriceViewSet) 
router.register(r'portfolio-assets', PortfolioAssetViewSet)
router.register(r'deposits', DepositViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-excel/', UploadExcelView.as_view(), name='upload-excel'),
]
