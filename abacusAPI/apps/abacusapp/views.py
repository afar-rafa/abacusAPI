from rest_framework import viewsets
from .models import Portfolio, Asset, PortfolioAssetQuantity, Price
from .serializers import PortfolioAssetQuantitySerializer, PortfolioSerializer, AssetSerializer, PriceSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class PortfolioAssetQuantityViewSet(viewsets.ModelViewSet):
    queryset = PortfolioAssetQuantity.objects.all()
    serializer_class = PortfolioAssetQuantitySerializer