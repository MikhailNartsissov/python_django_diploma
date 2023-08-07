from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .pagination import CustomPagination
from .models import Product, Category
from .serializers import CategorySerializer, CatalogSerializer


class CategoriesListView(APIView):
    def get(self, request: Request) -> Response:
        categories = Category.objects.all().prefetch_related()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class CatalogListView(ListAPIView):
    queryset = Product.objects.all().prefetch_related()
    filterset_fields = ["title", "price"]
    pagination_class = CustomPagination
    serializer_class = CatalogSerializer


class CatalogViewSet(ModelViewSet):
    queryset = Product.objects.all().prefetch_related().order_by('title')
    pagination_class = CustomPagination
    serializer_class = CatalogSerializer
    ordering = ['title']
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        "title",
        "price"
        "freeDelivery",
        "available",
    ]
    ordering_fields = [
        "title",
        "price",
    ]
