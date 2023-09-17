from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Count, Avg
from django.contrib.auth import logout, login


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
    Subcategory,
    Tag,
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
    TagSerializer,
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
    """
    View for categories
    """
    def get(self, request: Request) -> Response:
        categories = Category.objects.all().prefetch_related()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class SaleProductsListView(ListAPIView):
    """
    View for products on sale
    """
    pagination_class = CustomPagination
    serializer_class = SaleProductSerializer

    def get_queryset(self):
        queryset = ProductSale.objects.all().prefetch_related()
        sort_param = "product_title"
        return queryset


class CatalogListView(ListAPIView):
    """
    View for products catalog
    """
    pagination_class = CustomPagination
    serializer_class = CatalogSerializer

    def get_queryset(self):
        """
        Modified "get_queryset" method
        returns queryset, constructed on the base of query parameters
        :return:
        """

        queryset = Product.objects.all().prefetch_related()

        # getting name of the product to filter by
        name = self.request.query_params.get('filter[name]')
        if name is not None:
            queryset = queryset.filter(title__icontains=name)

        # getting minimal price of the product to filter by price
        minprice = self.request.query_params.get('filter[minPrice]')
        if minprice is not None:
            queryset = queryset.filter(price__gte=minprice)

        # getting maximal price of the product to filter by price
        maxprice = self.request.query_params.get('filter[maxPrice]')
        if maxprice is not None:
            queryset = queryset.filter(price__lte=maxprice)

        # getting free delivery flag to filter only products with free delivery
        freedelivery = self.request.query_params.get('filter[freeDelivery]')
        if freedelivery is not None:
            freedelivery = freedelivery.capitalize()
            if freedelivery == "True":
                queryset = queryset.filter(freeDelivery=freedelivery)

        # getting "available" flag to filter only available products
        available = self.request.query_params.get('filter[available]')
        if available is not None:
            available = available.capitalize()
            if available == "True":
                queryset = queryset.filter(available=available)

        # getting category to filter by
        category = self.request.query_params.get('category')
        if category is not None and category.isdigit():
            if int(category) >= 1000:
                queryset = queryset.filter(category=category)
            else:
                queryset = queryset.filter(category__category=category)

        # getting sorting parameters
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
    """
    View for specific products in catalog
    """
    serializer_class = CatalogItemSerializer

    def get_queryset(self):
        """
        Modified "get_queryset" method
        Checks if product id specified and returns
        specified product data if it is, or all products in opposite case
        :return:
        """
        queryset = Product.objects.all().prefetch_related()

        product_id = self.kwargs.get('pk')
        if product_id is not None:
            queryset = queryset.filter(id=product_id)
        return queryset


class ReviewCreateView(CreateAPIView):
    """
    View for product reviews
    """

    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        """
        Modified "perform_create" method for review creation
        :param serializer:
        :return:
        """
        product = Product.objects.filter(pk=self.kwargs["id"])[0]
        serializer.save(product=product, author=self.request.user)


class PopularProductsListView(ListAPIView):
    """
    View for popular products (First 8 products with average rate greater than 4,2)
    """
    queryset = Product.objects.annotate(rating=Avg("review__rate")).filter(rating__gte=4.2).prefetch_related()[:8]
    serializer_class = PopularProductsSerializer


class LimitedProductsListView(ListAPIView):
    """
    View for limited products (First 16 products with "limited"=True)
    """
    queryset = Product.objects.filter(limited=True).prefetch_related()[:16]
    serializer_class = PopularProductsSerializer


class BannerListView(ListAPIView):
    """
    View for banners (manually specified product ids in queryset)
    """
    queryset = Product.objects.filter(id__in=[6, 9, 13]).prefetch_related()
    serializer_class = PopularProductsSerializer


class BasketViewSet(ModelViewSet):
    """
    ViewSet for user basket
    """
    serializer_class = BasketSerializer
    session = SessionStore()
    session.create()

    def get_queryset(self):
        """
        Modified method "get_queryset" checks if there are any products with a specific session_id
        in temporary basket (user added them into temporary basket before log in) and? if they are, moves
        them into user's basket? deleting them from temporary basket
        If user is Anonymous TemporaryBasket model and serializer used instead of Basket.
        :return:
        """
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
        """
        Modified method "create" checks if user is authenticated and if there is corresponding item in the basket
        If item exists, it will be modified, if not, it will be created.
        If user is Anonymous TemporaryBasket model and serializer used instead of Basket and "session" id will be
        calculated and set.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
        """
        Modified method "delete" checks if user is authenticated and if "count" value in request parameter
        equals or more than "count" of the basket. If it is, basket will be deleted, if not "count" will be reduced
        correspondingly to "count" parameter of the request.
        If user is Anonymous TemporaryBasket model and serializer used instead of Basket.
        :param request:
        :return:
        """
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
        """
        Modified method "perform_destroy" destroys the instance
        :param instance:
        :return:
        """
        instance.delete()


class OrdersViewSet(LoginRequiredMixin, ModelViewSet):
    """
    ViewSet for Orders creation and representation.
    It takes part in the steps of the order creation after specifying user, delivery and payment data.
    Before it another ViewSet named "OrderViewSet" used.
    """
    serializer_class = OrdersSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Modified method "create" checks if the order exists and if so, modifies it.
        If not, it creates a new order.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
            # fullName construction
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
    """
    ViewSet for specific user's Order creation and representation.
    It takes part in initial steps of the order creation (before specifying user, delivery and payment data).
    Then another ViewSet named "OrdersViewSet" used.
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        """
        Modified method "post" creates a new order. It checks if the products from the basket
        are already in order and if not, adds them. It's necessary to be able to pay previously
        created orders correctly.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        data['totalCost'] = round(request.data['basketCount']['price'], 2)
        order = Order.objects.get(id=data['orderId'])
        serializer = self.get_serializer(order, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for product_id in request.data["basket"].keys():
            if not OrderItem.objects.filter(order=order, product=product_id):
                OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=product_id),
                    count=request.data['basket'][product_id]['count']
                )
        return Response(OrdersSerializer(order).data)


class PaymentCreateView(CreateAPIView):
    """
    View for payments
    """
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        """
        Modified method "create" performs checks, specified in the technical requirements
        and, if everything is Ok, sets status of order to "paid" and returns HTTP_201_CREATED.
        If checks fail, it sets status of order to "Awaiting payment + {error description}" and
        returns HTTP_400_BAD_REQUEST
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
    """
    View for user profile
    """
    pagination_class = ProfilePagination
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.filter(user=self.request.user.id).prefetch_related()
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Modified method "create" checks if user profile exists before adding profile data
        and, if not, creates it or modifies it in the opposite case.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
    """
    View for password change
    """
    serializer_class = PasswordChangeSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    def post(self, request):
        """
        Modified method "post" changes user password and logs in a user with the new credentials
        :param request:
        :return:
        """
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
    """
    View for user profile image
    """
    serializer_class = AvatarSerializer

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user.id).first()
        queryset = ProfileImage.objects.filter(profile=profile.id).first()
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Modified method "create" checks if user profile exists before adding profile image
        and, if not, creates it or modifies it in the opposite case.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
    """
    View for user logout
    :param request:
    :return:
    """
    logout(request)
    return Response(status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    View for user log in
    """
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        """
        Modified method "post" makes a dictionary from a string, which comes in request
        and logs user in after necessary checks
        :param request:
        :return:
        """
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
    """
    View for user creation
    """
    model = User
    # need to allow Anonymous users
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Modified method "post" makes a dictionary from a string, which comes in request
        and creates user after necessary checks if the user doesn't exist yet
        :param request:
        :return:
        """

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


class TagListView(ListAPIView):
    """
    View for product tags
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Modified method "get_queryset" checks if the "category" parameter from the request
        corresponds "Category" instance or "Subcategory" instance and returns a queryset
        constructed depends on it.
        :return:
        """
        category = self.request.query_params.get("category")
        if category:
            if len(category) < 4:
                category = Subcategory.objects.filter(category=category).values("id")
                return Tag.objects.filter(category__in=[(item["id"]) for item in category]).distinct()
            return Tag.objects.filter(category=category)
        return Tag.objects.all()
