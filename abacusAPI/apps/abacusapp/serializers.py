from rest_framework import serializers

from .models import (Asset, Deposit, Portfolio, PortfolioAsset, Price,
                     Transaction)


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"


class PortfolioDailyValueSerializer(serializers.Serializer):
    date = serializers.DateField()
    value = serializers.DecimalField(max_digits=20, decimal_places=4)
    weights = serializers.DictField(
        child=serializers.DecimalField(max_digits=7, decimal_places=4)
    )


class AssetSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return obj.price

    class Meta:
        model = Asset
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"


class PortfolioAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAsset
        fields = "__all__"


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
