from .models import Portfolio, PortfolioAsset, Price
from collections import defaultdict
from decimal import Decimal


def calculate_portfolio_daily_value(portfolio: Portfolio, date):
    assets = PortfolioAsset.objects.filter(portfolio=portfolio)
    prices = Price.objects.filter(asset__in=assets.values('asset'), date=date)

    total_value = Decimal(0)
    weights = {}

    for price in prices:
        asset_quantity = assets.get(asset=price.asset).quantity
        value = asset_quantity * price.price
        total_value += value
        weights[price.asset.name] = assets.get(asset=price.asset).weight

    return {
        'date': date,
        'value': total_value,
        'weights': weights,
    }


def calculate_portfolio_daily_values(portfolio: Portfolio, initial_date, end_date):
    assets = PortfolioAsset.objects.filter(portfolio=portfolio)
    prices = Price.objects.filter(asset__in=assets.values('asset'), date__range=[initial_date, end_date])

    daily_values = defaultdict(lambda: {
        'value': Decimal(0),
        'weights': {},
    })
    
    for price in prices:
        asset_quantity = assets.get(asset=price.asset).quantity
        value = asset_quantity * price.price
        daily_values[price.date]['value'] += value
        daily_values[price.date]['weights'][price.asset.name] = assets.get(asset=price.asset).weight

    return [
        {
            'date': date,
            'value': data['value'],
            'weights': data['weights'],
        }
        for date, data in daily_values.items()
    ]
