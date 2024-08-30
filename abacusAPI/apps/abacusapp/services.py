import io
import base64

import matplotlib.pyplot as plt
from collections import defaultdict
from decimal import Decimal
from matplotlib.dates import DateFormatter

from .models import Asset, Portfolio, PortfolioAsset, Price, Transaction


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


def generate_portfolio_plots(portfolio, initial_date, end_date):
    # Get the daily values
    daily_values = calculate_portfolio_daily_values(portfolio, initial_date, end_date)

    if not daily_values:
        return None

    dates = [entry['date'] for entry in daily_values]
    values = [entry['value'] for entry in daily_values]
    weights = {asset: [] for asset in daily_values[0]['weights'].keys()}

    for entry in daily_values:
        for asset, weight in entry['weights'].items():
            weights[asset].append(weight)

    # Set the portfolio value as a line graph
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(dates, values, label=f'{portfolio.name}', color='blue')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Valor (t)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Format date on x-axis
    ax1.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()

    # Make a second y-axis for the stacked area plot
    ax2 = ax1.twinx()
    ax2.stackplot(dates, *weights.values(), labels=weights.keys(), alpha=0.4)
    ax2.set_ylabel('Weights (t)')

    # Adding legends and title
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title(f'Portfolio Value and Weights for "{portfolio.name}"')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    # Encode the image to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return image_base64


def buy_asset(portfolio: Portfolio, asset: Asset, quantity: Decimal, price: Decimal, date):
    # Create the transaction
    transaction = Transaction.objects.create(
        portfolio=portfolio,
        asset=asset,
        date=date,
        transaction_type=Transaction.TRANSACTION_BUY,
        quantity=quantity,
        price=price
    )

    # Update the portfolio's holdings
    portfolio_asset, _ = PortfolioAsset.objects.get_or_create(portfolio=portfolio, asset=asset)
    portfolio_asset.quantity += quantity
    portfolio_asset.save()

    return transaction

def sell_asset(portfolio: Portfolio, asset: Asset, quantity: Decimal, price: Decimal, date):
    portfolio_asset = PortfolioAsset.objects.get(portfolio=portfolio, asset=asset)
    
    if portfolio_asset.quantity < quantity:
        raise ValueError("Cannot sell more assets than owned.")

    # Create the transaction
    transaction = Transaction.objects.create(
        portfolio=portfolio,
        asset=asset,
        date=date,
        transaction_type=Transaction.TRANSACTION_SELL,
        quantity=quantity,
        price=price
    )

    # Update the portfolio's holdings
    portfolio_asset.quantity -= quantity
    if portfolio_asset.quantity == 0:
        portfolio_asset.delete()
    else:
        portfolio_asset.save()

    return transaction