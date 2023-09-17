from django.contrib.auth import authenticate

from .models import (
    Product,
    Category,
    Subcategory,
    ProductImage,
    Tag,
    Review,
    ProductSale,
    ProductSpecifications,
    Basket,
    Profile,
    ProfileImage,
    Order,
    OrderItem,
    Payment,
    TemporaryBasket,
)

from django.contrib.auth.models import User

from rest_framework import serializers
from django.db.models import Avg


class CategoryImageSerializer(serializers.ModelSerializer):
    """
    Serializer for categories images
    """

    class Meta:
        model = Category
        fields = ['src', 'alt']


class SubCategoryImageSerializer(serializers.ModelSerializer):
    """
    Serializer for subcategories images
    Differs from CategoryImageSerializer by model only
    """

    class Meta:
        model = Subcategory
        fields = ['src', 'alt']


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Serializer for product subcategories
    """
    image = SubCategoryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'title', 'image']

    def to_representation(self, instance):
        """
        Modified "to_representation" method.
        Added SubCategoryImageSerializer data to fit swagger requirements
        :param instance:
        :return:
        """
        response = super().to_representation(instance)
        response['image'] = SubCategoryImageSerializer(instance).data
        return response


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for product categories
    """
    image = CategoryImageSerializer(many=True, read_only=True)
    subcategories = SubcategorySerializer(many=True, read_only=True, source='subcategory_set')

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def to_representation(self, instance):
        """
        Modified "to_representation" method.
        Added CategoryImageSerializer data to fit swagger requirements
        :param instance:
        :return:
        """
        response = super().to_representation(instance)
        response['image'] = CategoryImageSerializer(instance).data
        return response


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for product tags
    """

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for product images
    """

    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class CatalogSerializer(serializers.ModelSerializer):
    """
    Serializer for catalog items (i.e. products in specific category or subcategory)
    """

    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')
    price = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
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

    def get_price(self, obj):
        """
        Method for calculating product price. First it checks, whether the product on sale, and, if so,
        returns its sale price (reduced). If not, it returns product price (ordinary).
        :param obj:
        :return:
        """
        sale = ProductSale.objects.filter(product=obj)
        if sale:
            return sale.first().salePrice
        return obj.price

    def get_reviews(self, obj):
        """
        Method calculates aggregate number of the products reviews.
        :param obj:
        :return:
        """
        return obj.review_set.count()

    def get_rating(self, obj):
        """
        Method calculates average rate of the product, based on rates, made by users.
        :param obj:
        :return:
        """
        return obj.review_set.aggregate(Avg('rate'))["rate__avg"]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for product reviews
    """

    email = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "author",
            "email",
            "text",
            "rate",
            "date",
        ]

    def get_email(self, obj):
        """
        Method returns email of the specific user
        :param obj:
        :return:
        """
        return obj.author.email

    def get_author(self, obj):
        """
        Method returns username of the specific user
        :param obj:
        :return:
        """
        return obj.author.username


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    """
    Serializer for product specifications
    """

    class Meta:
        model = ProductSpecifications
        fields = [
            'name',
            'value',
        ]


class CatalogItemSerializer(serializers.ModelSerializer):
    """
    Serializer for specific catalog item (i.e. single product in specific category or subcategory)
    """

    fullDescription = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    tags = TagSerializer(many=True, read_only=True)
    specifications = ProductSpecificationsSerializer(many=True, read_only=True, source='productspecifications_set')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'specifications',
            'rating',
        ]

    def get_price(self, obj):
        """
        Method for calculating product price. First it checks, whether the product on sale, and, if so,
        returns its sale price (reduced). If not, it returns product price (ordinary).
        :param obj:
        :return:
        """
        sale = ProductSale.objects.filter(product=obj)
        if sale:
            return sale.first().salePrice
        return obj.price

    def get_description(self, obj):
        """
        Method returns first 100 symbols of the product description.
        :param obj:
        :return:
        """
        return obj.description[:100]

    def get_fullDescription(self, obj):
        """
        Method returns all symbols of the product description, not only first 100, opposite to "get_description" above.
        :param obj:
        :return:
        """
        return obj.description

    def get_rating(self, obj):
        """
        Method calculates average rate of the product, based on rates, made by users.
        :param obj:
        :return:
        """
        return obj.review_set.aggregate(Avg('rate'))["rate__avg"]


class PopularProductsSerializer(serializers.ModelSerializer):
    """
    Serializer for first 8 products with average rate greater than 4,2
    """

    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
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
        """
        Method calculates aggregate number of the products reviews.
        :param obj:
        :return:
        """
        return obj.review_set.count()

    def get_rating(self, obj):
        """
        Method calculates average rate of the product, based on rates, made by users.
        :param obj:
        :return:
        """
        return obj.review_set.aggregate(Avg('rate'))["rate__avg"]


class SaleProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for products on sale images
    """

    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')

    class Meta:
        model = Product
        fields = "images",


class SaleProductSerializer(serializers.ModelSerializer):
    """
    Serializer for products on sale
    """
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    images = SaleProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductSale
        fields = [
            'id',
            'price',
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images"
        ]

    def get_id(self, obj):
        """
        Method returns product id
        :param obj:
        :return:
        """
        return obj.product.pk

    def get_price(self, obj):
        """
        Method returns product ordinary price with no discount
        :param obj:
        :return:
        """
        return obj.product.price

    def get_title(self, obj):
        """
        Method returns product name
        :param obj:
        :return:
        """
        return obj.product.title

    def to_representation(self, instance):
        """
        Modified "to_representation" method.
        Added SaleProductImageSerializer data to fit swagger requirements and
        modified "dateFrom" and "dateTo" values to fit frontend forms
        :param instance:
        :return:
        """
        response = super().to_representation(instance)
        product = instance.product
        response["dateFrom"] = instance.dateFrom.strftime("%d/%m")
        response["dateTo"] = instance.dateTo.strftime("%d/%m")
        response['images'] = SaleProductImageSerializer(product).data['images']
        return response


class BasketSerializer(serializers.ModelSerializer):
    """
    Serializer for products in user's basket
    """
    class Meta:
        model = Basket
        fields = [
            'user',
            'date',
            'product',
            'count',
        ]

    def to_representation(self, instance):
        """
        Modified "to_representation" method.
        Added CatalogSerializer data to present products data in a way, which fits swagger requirements
        :param instance:
        :return:
        """
        response = CatalogSerializer(instance.product).data
        response['count'] = instance.count
        return response


class TemporaryBasketSerializer(serializers.ModelSerializer):
    """
    Serializer for products in temporary Anonymous user's basket
    Differs from BasketSerializer by model and fields
    """
    class Meta:
        model = TemporaryBasket
        fields = [
            'session',
            'date',
            'product',
            'count',
        ]

    def to_representation(self, instance):
        """
        Modified "to_representation" method.
        Added CatalogSerializer data to present products data in a way, which fits swagger requirements
        :param instance:
        :return:
        """
        response = CatalogSerializer(instance.product).data
        response['count'] = instance.count
        return response


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for specific user's Order creation and representation.
    It takes part in initial steps of the order creation (before specifying user, delivery and payment data).
    Then another serializer named "OrdersSerializer" used.
    Differs from OrdersSerializer by fields set and output data.
    """

    totalCost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, rounding='ROUND_HALF_EVEN')
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'city',
            'address',
            'products',
        ]

    def get_products(self, obj):
        """
        Method returns a list of products in user's basket or order
        First it checks, if any products are in the basket or no. If they are,
        method adds them into list. If not, it uses OrderItems instead.
        :param obj:
        :return:
        """
        result = []
        basket = Basket.objects.filter(user=self.context['request'].user)
        if basket:
            for product in basket:
                result.append(BasketSerializer(product).data)
        else:
            order_items = OrderItem.objects.filter(order=obj.id)
            for item in order_items:
                result.append(BasketSerializer(item).data)
        return result


class OrdersSerializer(serializers.ModelSerializer):
    """
    Serializer for Orders creation and representation.
    It takes part in the steps of the order creation after specifying user, delivery and payment data.
    Before it another serializer named "OrderSerializer" used.
    Differs from OrderSerializer by fields set and output data.
    """
    totalCost = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
        ]

    def get_products(self, obj):
        """
        Method returns a list of products in user's order
        :param obj:
        :return:
        """
        result = []
        for item in OrderItem.objects.filter(order=obj.id):
            result.append(CatalogSerializer(item.product).data)
        return result

    def get_totalCost(self, obj):
        """
        Method returns total cost of the order. First it checks whether the product on sale. If so, the method
        uses salePrice (reduced) instead of ordinary, if not, it uses ordinary product price.
        :param obj:
        :return:
        """
        result = 0
        for item in OrderItem.objects.filter(order=obj.id):
            sale = ProductSale.objects.filter(product=item.product)
            if sale:
                price = sale.first().salePrice
            else:
                price = item.product.price
            result += price * item.count
        return result

    def get_createdAt(self, obj):
        """
        Method returns modified order creation date to fit frontend form
        :param obj:
        :return:
        """
        return obj.createdAt.strftime("%d/%m/%y %H:%M:%S")

    def to_representation(self, instance):
        """
        Modified "to_representation" method.
        Added "orderId" data to fit swagger requirements
        :param instance:
        :return:
        """
        result = super().to_representation(instance=instance)
        result["orderId"] = instance.id
        return result


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payments creation and representation.
    """
    class Meta:
        model = Payment
        fields = [
            'order',
            'name',
            'number',
            'month',
            'year',
            'code',
        ]


class AvatarSerializer(serializers.ModelSerializer):
    """
    Serializer for user's profile image.
    """
    avatar = serializers.SerializerMethodField(required=False)

    class Meta:
        model = ProfileImage
        fields = [
            'profile',
            'src',
            'alt',
            'avatar',
        ]

    def get_avatar(self, obj):
        """
        Method returns profile image data in form corresponding swagger requirements
        :param obj:
        :return:
        """
        avatar = dict()
        if obj.src:
            avatar['src'] = obj.src.path

        else:
            avatar['src'] = None
        avatar['alt'] = obj.alt
        return avatar


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user's profile.
    """
    avatar = AvatarSerializer(source='profileimage', required=False)

    class Meta:
        model = Profile
        fields = [
            'user',
            'fullName',
            'email',
            'phone',
            'avatar',
        ]


class PasswordChangeSerializer(serializers.ModelSerializer):
    """
    Serializer for user's password.
    """

    password = serializers.CharField(
        label="password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            "password",
        )

    def update(self, instance, validated_data):
        """
        Method updates user's password
        :param instance:
        :param validated_data:
        :return:
        """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in users.
    """
    username = serializers.CharField(
        label="username",
        write_only=True
    )
    password = serializers.CharField(
        label="password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        """
        Method validates login credentials. It checks both username and password are specified and both are valid.
        :param attrs:
        :return:
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user's data.
    """

    password = serializers.CharField(
        label="password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "username",
            "password",
        )

    def create(self, validated_data):
        """
        Method creates a new user
        :param validated_data:
        :return:
        """
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
