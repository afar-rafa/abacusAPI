import logging
from django.db import models
from django.forms import ValidationError


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
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    weight = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('portfolio', 'asset')

    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} (q={self.quantity}, w={self.weight}%)"    
    

class Deposit(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.distribute_deposit()

    def distribute_deposit(self):
        portfolio_assets = PortfolioAsset.objects.filter(portfolio=self.portfolio)
        total_weight = sum(pa.weight for pa in portfolio_assets)
        logger.info(f"Deposit Started [p={self.portfolio}, cant={self.amount}]")

        if total_weight != 1:
            raise ValidationError("The weights of the assets must sum up to 100%.")

        for pa in portfolio_assets:
            allocation = pa.weight * self.amount
            logger.debug(
                f"Deposit for Asset: {pa.weight} * {self.amount} = {allocation} "
                f"[p={self.portfolio.name}, a={pa.asset.name}, cant={self.amount}]",
            )

            # TODO: It's assuming price is accessible
            logger.debug(
                f"Deposit for Asset: Adding {allocation} / {pa.asset.price} to {pa.quantity} "
                f"[p={self.portfolio.name}, a={pa.asset.name}, cant={self.amount}]",
            )
            pa.quantity += allocation / pa.asset.price
            logger.info(
                f"Deposit for Asset Done "
                f"[p={self.portfolio.name}, a={pa.asset.name}, cant={self.amount}, q={pa.quantity}]",
            )

            pa.save()

    def __str__(self):
        return f"Deposit of {self.amount} to {self.portfolio.name} on {self.date}"
