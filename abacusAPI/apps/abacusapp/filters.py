import django_filters
from .models import PortfolioAsset

class PortfolioAssetFilter(django_filters.FilterSet):
    portfolio = django_filters.CharFilter(field_name="portfolio__name", lookup_expr='iexact')
    portfolio_id = django_filters.NumberFilter(field_name="portfolio__id")

    class Meta:
        model = PortfolioAsset
        fields = ['portfolio', 'portfolio_id']
