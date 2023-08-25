from django.db.models import Count, Avg

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .pagination import CustomPagination
from .models import (
    Product,
    Category,
    ProductSale,
    Basket,
)

from .serializers import (
    CategorySerializer,
    CatalogSerializer,
    PopularProductsSerializer,
    SaleProductSerializer,
    CatalogItemSerializer,
    ReviewSerializer,
    BasketSerializer,
)


class CategoriesListView(APIView):
    def get(self, request: Request) -> Response:
        categories = Category.objects.all().prefetch_related()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class CatalogListView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = CatalogSerializer

    def get_queryset(self):

        queryset = Product.objects.all().prefetch_related()

        name = self.request.query_params.get('filter[name]')
        if name is not None:
            queryset = queryset.filter(title__icontains=name)

        minprice = self.request.query_params.get('filter[minPrice]')
        if minprice is not None:
            queryset = queryset.filter(price__gte=minprice)

        maxprice = self.request.query_params.get('filter[maxPrice]')
        if maxprice is not None:
            queryset = queryset.filter(price__lte=maxprice)

        freedelivery = self.request.query_params.get('filter[freeDelivery]')
        if freedelivery is not None:
            freedelivery = freedelivery.capitalize()
            if freedelivery == "True":
                queryset = queryset.filter(freeDelivery=freedelivery)

        available = self.request.query_params.get('filter[available]')
        if available is not None:
            available = available.capitalize()
            if available == "True":
                queryset = queryset.filter(available=available)

        category = self.request.query_params.get('category')
        if category is not None and category.isdigit():
            if int(category) >= 1000:
                queryset = queryset.filter(category=category)
            else:
                queryset = queryset.filter(category__category=category)

        sort_param = self.request.query_params.get('sort')
        if sort_param is not None:
            if sort_param == "reviews":
                queryset = queryset.annotate(reviews_count=Count("review"))
                sort_param = "reviews_count"
            if sort_param == "rating":
                queryset = queryset.annotate(rating=Avg("review__rate"))
                sort_param = "rating"
            sort_type = self.request.query_params.get('sortType')
            if sort_type is not None:
                if sort_type == 'inc':
                    sort_param = "-" + sort_param
            queryset = queryset.order_by(sort_param)
        return queryset


class CatalogItemViewSet(ModelViewSet):
    serializer_class = CatalogItemSerializer

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related()

        product_id = self.kwargs.get('pk')
        if product_id is not None:
            queryset = queryset.filter(id=product_id)
        return queryset


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product = Product.objects.filter(pk=self.kwargs["id"])[0]
        serializer.save(product=product, author=self.request.user)


class PopularProductsListView(ListAPIView):
    queryset = Product.objects.annotate(rating=Avg("review__rate")).filter(rating__gte=4.2).prefetch_related()[:8]
    serializer_class = PopularProductsSerializer


class LimitedProductsListView(ListAPIView):
    queryset = Product.objects.filter(limited=True).prefetch_related()[:16]
    serializer_class = PopularProductsSerializer


class BannerListView(ListAPIView):
    queryset = Product.objects.filter(id__in=[6, 9, 13]).prefetch_related()
    serializer_class = PopularProductsSerializer


class SaleProductsListView(ListAPIView):
    queryset = ProductSale.objects.all().prefetch_related()
    pagination_class = CustomPagination
    serializer_class = SaleProductSerializer
    ordering = ['product__title']


class BasketViewSet(ModelViewSet):
    serializer_class = BasketSerializer

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user).prefetch_related()

    def create(self, request, *args, **kwargs):
        data = dict()
        data['user'] = request.user.id
        data['product'] = request.data['id']
        data['count'] = request.data['count']
        partial = False
        instance = Basket.objects.filter(user=request.user.id, product=request.data['id'])
        if instance:
            partial = True
            instance = instance[0]
            data['count'] += instance.count
            serializer = self.get_serializer(instance=instance, data=data, partial=partial)
        else:
            serializer = self.get_serializer(data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        count = request.data['count']
        instance = Basket.objects.filter(user=request.user.id, product=request.data['id'])
        if instance:
            instance = instance[0]
        if instance.count > count:
            data = dict()
            partial = True
            serializer = self.get_serializer(instance=instance, data=data, partial=partial)
            data['count'] = instance.count - count
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            print(headers)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
