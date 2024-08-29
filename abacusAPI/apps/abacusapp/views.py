from rest_framework import viewsets
from .models import Deposit, Portfolio, Asset, PortfolioAsset, Price
from .serializers import DepositSerializer, PortfolioAssetSerializer, PortfolioSerializer, AssetSerializer, PriceSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

class PortfolioAssetViewSet(viewsets.ModelViewSet):
    queryset = PortfolioAsset.objects.all()
    serializer_class = PortfolioAssetSerializer

class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
