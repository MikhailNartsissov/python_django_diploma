from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Count, Avg
from django.contrib.auth import logout, login
from django import db


from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.mixins import LoginRequiredMixin

from .pagination import (
    CustomPagination,
    ProfilePagination,
)

from .models import (
    Product,
    Category,
    ProductSale,
    Basket,
    Profile,
    ProfileImage,
    Order,
    OrderItem,
    Payment,
    TemporaryBasket,
)

from .serializers import (
    CategorySerializer,
    CatalogSerializer,
    PopularProductsSerializer,
    SaleProductSerializer,
    CatalogItemSerializer,
    ReviewSerializer,
    BasketSerializer,
    OrderSerializer,
    OrdersSerializer,
    PaymentSerializer,
    ProfileSerializer,
    AvatarSerializer,
    LoginSerializer,
    UserSerializer,
    PasswordChangeSerializer,
    TemporaryBasketSerializer,
)


class CategoriesListView(APIView):
    def get(self, request: Request) -> Response:
        categories = Category.objects.all().prefetch_related()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class SaleProductsListView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = SaleProductSerializer

    def get_queryset(self):
        queryset = ProductSale.objects.all().prefetch_related()
        sort_param = "product_title"
        return queryset


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


class BasketViewSet(ModelViewSet):
    serializer_class = BasketSerializer
    session = SessionStore()
    session.create()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.session.session_key:
                for item in TemporaryBasket.objects.filter(session=self.session.session_key):
                    Basket.objects.create(
                        user=self.request.user,
                        date=item.date,
                        product=item.product,
                        count=item.count
                    )
                    item.delete()
            return Basket.objects.filter(user=self.request.user).prefetch_related()
        self.serializer_class = TemporaryBasketSerializer
        return TemporaryBasket.objects.filter(session=self.session.session_key)

    def create(self, request, *args, **kwargs):
        data = dict()
        data['user'] = request.user.id
        data['product'] = request.data['id']
        data['count'] = request.data['count']
        partial = False
        if request.user.is_authenticated:
            instance = Basket.objects.filter(user=request.user.id, product=request.data['id'])
        else:
            data['session'] = self.session.session_key
            instance = TemporaryBasket.objects.filter(session=self.session.session_key, product=request.data['id'])
        if instance:
            partial = True
            instance = instance[0]
            data['count'] += instance.count
            if request.user.is_authenticated:
                serializer = self.get_serializer(instance=instance, data=data, partial=partial)
            else:
                serializer = TemporaryBasketSerializer(instance=instance, data=data, partial=partial)
        else:
            if request.user.is_authenticated:
                serializer = self.get_serializer(data=data, partial=partial)
            else:
                serializer = TemporaryBasketSerializer(data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        count = request.data['count']
        if request.user.is_authenticated:
            instance = Basket.objects.filter(user=request.user, product=request.data['id'])
        else:
            session = self.session
            instance = TemporaryBasket.objects.filter(session=session.session_key, product=request.data['id'])
        if instance:
            instance = instance[0]
        if instance.count > count:
            data = dict()
            partial = True
            if request.user.is_authenticated:
                serializer = self.get_serializer(instance=instance, data=data, partial=partial)
            else:
                serializer = TemporaryBasketSerializer(instance=instance, data=data, partial=partial)
            data['count'] = instance.count - count
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class OrdersViewSet(ModelViewSet):
    serializer_class = OrdersSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        data = dict()
        data['user'] = request.user.pk
        order = Order.objects.filter(
            user=request.user,
            status="accepted",
            city="Enter city of the delivery",
            address="Enter address of the delivery",
            email="user@domain.com",
            phone=0
        ).last()
        if request.user.first_name or request.user.last_name:
            data['fullName'] = request.user.first_name + " " + request.user.last_name
        else:
            data['fullName'] = request.user.username
        if order:
            serializer = self.get_serializer(order, data=data)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        data = request.data
        data['totalCost'] = round(request.data['basketCount']['price'], 2)
        order = Order.objects.get(id=data['orderId'])
        serializer = self.get_serializer(order, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for product_id in request.data["basket"].keys():
            if not OrderItem.objects.filter(product=product_id):
                OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=product_id),
                    count=request.data['basket'][product_id]['count']
                )
        return Response(OrdersSerializer(order).data)


class PaymentCreateView(CreateAPIView):
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        order = Order.objects.get(id=self.kwargs["id"])
        number = data["number"]
        if not number.isdigit():
            error_message = "Error: Card number must contain only digits."
            order.status = "Awaiting payment. " + error_message
            order.save()
            return Response(status=status.HTTP_400_BAD_REQUEST, data=error_message)
        if len(number) > 8:
            error_message = "Error: Card number can't be longer than 8 digits."
            order.status = "Awaiting payment. " + error_message
            order.save()
        number = int(number)
        if number % 2 != 0 or number % 10 == 0:
            error_message = "Error: Card number must be even and may not have 0 at the end."
            order.status = "Awaiting payment. " + error_message
            order.save()
            return Response(status=status.HTTP_400_BAD_REQUEST, data=error_message)
        data['order'] = self.kwargs["id"]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        order = Order.objects.get(id=data['order'])
        order.status = "paid"
        order.save()
        Basket.objects.filter(user=request.user).delete()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProfileListCreateView(ListCreateAPIView):
    pagination_class = ProfilePagination
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.filter(user=self.request.user.id).prefetch_related()
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        profile = Profile.objects.filter(user=request.user.id).first()
        if profile:
            image = ProfileImage.objects.filter(profile=profile.id).first()
            if image:
                data.pop("avatar")
            serializer = self.get_serializer(profile, data=data)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PasswordChangeView(UpdateAPIView):
    serializer_class = PasswordChangeSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    def post(self, request):
        data = dict()
        data["password"] = request.data["newPassword"]
        user = request.user
        serializer = self.get_serializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        request.data["password"] = data["password"]
        login(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvatarListCreateView(ListCreateAPIView):
    serializer_class = AvatarSerializer

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user.id).first()
        queryset = ProfileImage.objects.filter(profile=profile.id).first()
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data['src'] = request.FILES["avatar"]
        profile = Profile.objects.filter(user=request.user.id).first()
        if not profile:
            profile = Profile.objects.create(user=request.user, phone=0)
        data["profile"] = profile.id
        profile_image = ProfileImage.objects.filter(profile=profile.id).first()
        if profile_image:
            serializer = self.get_serializer(profile_image, data=data)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid()
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def sign_out_view(request: Request) -> Response:
    logout(request)
    return Response(status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        data = dict()
        for key in request.data.keys():
            msg = key.strip("{").strip("}").split(",")
        for item in msg:
            data[item.split(":")[0].strip('"')] = item.split(":")[1].strip('"')
        serializer = LoginSerializer(data=data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = dict()
        for key in request.data.keys():
            msg = key.strip("{").strip("}").split(",")
        for item in msg:
            data[item.split(":")[0].strip('"')] = item.split(":")[1].strip('"')
        data["first_name"] = data["name"]
        data.pop("name")
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = User.objects.get(pk=serializer.data["id"])
        login(request, user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
