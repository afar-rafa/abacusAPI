from rest_framework import serializers
from .models import Deposit, Portfolio, Asset, PortfolioAsset, Price


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return obj.price

    class Meta:
        model = Asset
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class PortfolioAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAsset
        fields = '__all__'


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'