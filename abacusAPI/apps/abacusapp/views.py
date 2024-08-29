from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Deposit, Portfolio, Asset, PortfolioAsset, Price
from .serializers import DepositSerializer, PortfolioAssetSerializer, PortfolioSerializer, AssetSerializer, PriceSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class PortfolioAssetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet used to show all Assets under the same portfolio
    under the portfolios/{portfolio_id}/assets/ url
    """
    serializer_class = AssetSerializer

    def get_queryset(self):
        portfolio_id = self.kwargs.get('portfolio_id')
        return Asset.objects.filter(portfolioasset__portfolio_id=portfolio_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'detail': 'No assets found for this portfolio'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
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
