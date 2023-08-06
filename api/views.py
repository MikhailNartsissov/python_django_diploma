from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoriesListView(APIView):
    def get(self, request: Request) -> Response:
        categories = Category.objects.all().prefetch_related()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        "title",
        "description",
    ]
    ordering_fields = [
        "title",
        "price",
        "freeDelivery",
    ]
