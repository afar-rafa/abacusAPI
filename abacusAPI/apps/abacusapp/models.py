from django.db import models


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
    

class Price(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        # Ensure unique price per asset per date
        unique_together = ('asset', 'date')

    def __str__(self):
        return f"{self.asset.name} - {self.price} on {self.date}"

class PortfolioAssetQuantity(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('portfolio', 'asset')

    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} ({self.quantity})"
    