from .models import Product, Category, Subcategory, ProductImage, Tag, Review

from rest_framework import serializers
from django.db.models import Avg


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class CatalogSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'rating',
        ]

    def get_reviews(self, obj):
        return obj.review_set.count()

    def get_rating(self, obj):
        return obj.review_set.aggregate(Avg('rate'))["rate__avg"]
