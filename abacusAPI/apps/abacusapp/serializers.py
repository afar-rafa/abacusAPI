from rest_framework import serializers
from .models import Portfolio, Asset, PortfolioAssetQuantity, Price


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class PortfolioAssetQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAssetQuantity
        fields = '__all__'