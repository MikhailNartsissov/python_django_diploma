from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "title",
            "description",
            "price",
            "count",
            "freeDelivery",
            "date",
            "archived",
            "tags",
        )
