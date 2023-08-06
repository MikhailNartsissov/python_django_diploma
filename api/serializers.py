from .models import Product, Category, Subcategory, ProductImage, Tag, Review

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "price",
            "count",
            "freeDelivery",
            "date",
            "archived",
            "tags",
        )


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['src', 'alt']


class SubCategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['src', 'alt']


class SubcategorySerializer(serializers.ModelSerializer):
    image = SubCategoryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'title', 'image']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image'] = SubCategoryImageSerializer(instance).data
        return response


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer(many=True, read_only=True)
    subcategories = SubcategorySerializer(many=True, read_only=True, source='subcategory_set')

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image'] = CategoryImageSerializer(instance).data
        return response


class PopularProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "category",
            "id",
            "title",
            "description",
            "price",
            "count",
            "freeDelivery",
            "date",
            "archived",
            "tags",
        )
