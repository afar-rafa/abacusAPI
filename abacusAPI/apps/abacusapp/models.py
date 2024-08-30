import logging
from datetime import datetime
from django.db import models, transaction
from rest_framework.exceptions import ValidationError
from django.utils import timezone


logger = logging.getLogger('abacusapp')

class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Asset(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    @property
    def price(self):
        # Get the latest price for this asset
        latest_price = self.prices.order_by('-date').first()
        return latest_price.price if latest_price else None

    def price_by_date(self, date: datetime):
        # Get the price on the given date
        price = self.prices.get(date=date)
        return price.price if price else None


class Price(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()

    class Meta:
        # Ensure unique price per asset per date
        unique_together = ('asset', 'date')

    def __str__(self):
        return f"{self.asset.name} - {self.price} on {self.date}"

class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    class Meta:
        unique_together = ('portfolio', 'asset')

    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} (q={self.quantity}, w={self.weight}%)"    
    

class Deposit(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.distribute_deposit()

    def distribute_deposit(self):
        portfolio_assets = PortfolioAsset.objects.filter(portfolio=self.portfolio)
        logger.info(f"Deposit Started [p={self.portfolio}, cant={self.amount}]")

        total_weight = sum(pa.weight for pa in portfolio_assets)
        if total_weight != 1:
            raise ValidationError("The weights of the assets must sum up to 100%.")

        for pa in portfolio_assets:
            allocation = pa.weight * self.amount
            logger.debug(
                f"Deposit for Asset: {pa.weight} * {self.amount} = {allocation} "
                f"[p={self.portfolio.name}, a={pa.asset.name}, cant={self.amount}]",
            )

            asset_price = pa.asset.price_by_date(self.date)
            if not asset_price:
                raise ValidationError(f"Missing asset value for the given date [a={pa.asset}, date={self.date}].")
            
            logger.debug(
                f"Deposit for Asset: Adding {allocation} / {asset_price} to {pa.quantity} "
                f"[p={self.portfolio.name}, a={pa.asset.name}, cant={self.amount}]",
            )
            pa.quantity += allocation / asset_price
            logger.info(
                f"Deposit for Asset Done "
                f"[p={self.portfolio.name}, a={pa.asset.name}, cant={self.amount}, q={pa.quantity}]",
            )

            pa.save()

    def __str__(self):
        return f"Deposit of {self.amount} to {self.portfolio.name} on {self.date}"


class Transaction(models.Model):
    """
    Saves what transactions are don on each asset and portfolio regarding buying and selling
    """

    TRANSACTION_BUY = 'buy'
    TRANSACTION_SELL = 'sell'

    TRANSACTION_TYPE_CHOICES = [
        (TRANSACTION_BUY, 'Buy'),
        (TRANSACTION_SELL, 'Sell'),
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES)
    # Cash involved in the transaction
    value = models.DecimalField(max_digits=12, decimal_places=2)


    def save(self, *args, **kwargs):
        """
        Update also the PortfolioAsset model when saving a transaction with the amounts
        """
        logger.info("Preparing transaction changes on PortfolioAsset")
        # Get the price based on the asset and date
        price = self.asset.price_by_date(self.date)
        if not price:
            raise ValidationError(
                f"Price not found for the given Asset [a={self.asset.name}, d={self.date}]"
            )

        # Calculate quantity based on value and price
        quantity = self.value / price

        # to avoid partial updates
        with transaction.atomic():
            # Retrieve or create the PortfolioAsset object
            portfolio_asset, _ = PortfolioAsset.objects.select_for_update().get_or_create(
                portfolio=self.portfolio,
                asset=self.asset,
            )

            logger.debug(
                "Saving transaction on PortfolioAsset [id=%d, p=%s, a=%s, t=%s, curr_q=%d, q=%d]",
                portfolio_asset.id,
                self.portfolio,
                self.asset,
                self.transaction_type,
                portfolio_asset.quantity,
                quantity,
            )

            # Adjust quantity based on transaction type
            if self.transaction_type == self.TRANSACTION_BUY:
                portfolio_asset.quantity += quantity
            elif self.transaction_type == self.TRANSACTION_SELL:
                if portfolio_asset.quantity < quantity:
                    raise ValidationError(
                        f"Cannot sell more assets than owned! (current={portfolio_asset.quantity:.2f} < selling={quantity:.2f})",
                    )
                portfolio_asset.quantity -= quantity

            # Save the PortfolioAsset changes
            portfolio_asset.save()

            # delete the portfolio_asset if quantities becomes zero
            if portfolio_asset.quantity == 0 and portfolio_asset.weight == 0:
                portfolio_asset.delete()

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.transaction_type.capitalize()} {self.value} value of {self.asset.name} for {self.portfolio.name} on {self.date}"
