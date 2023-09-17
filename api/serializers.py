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
        sale = ProductSale.objects.filter(product=obj)
        if sale:
            return sale.first().salePrice
        return obj.price
    def get_reviews(self, obj):
        return obj.review_set.count()

    def get_rating(self, obj):
        return obj.review_set.aggregate(Avg('rate'))["rate__avg"]


class ReviewSerializer(serializers.ModelSerializer):
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
        return obj.author.email

    def get_author(self, obj):
        return obj.author.username


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecifications
        fields = [
            'name',
            'value',
        ]


class CatalogItemSerializer(serializers.ModelSerializer):
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
        sale = ProductSale.objects.filter(product=obj)
        if sale:
            return sale.first().salePrice
        return obj.price

    def get_description(self, obj):
        return obj.description[:100]

    def get_fullDescription(self, obj):
        return obj.description

    def get_rating(self, obj):
        return obj.review_set.aggregate(Avg('rate'))["rate__avg"]


class PopularProductsSerializer(serializers.ModelSerializer):
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
        return obj.review_set.count()

    def get_rating(self, obj):
        return obj.review_set.aggregate(Avg('rate'))["rate__avg"]


class SaleProductImageSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')

    class Meta:
        model = Product
        fields = "images",


class SaleProductSerializer(serializers.ModelSerializer):
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
        return obj.product.pk

    def get_price(self, obj):
        return obj.product.price

    def get_title(self, obj):
        return obj.product.title

    def to_representation(self, instance):
        response = super().to_representation(instance)
        product = instance.product
        response["dateFrom"] = instance.dateFrom.strftime("%d/%m")
        response["dateTo"] = instance.dateTo.strftime("%d/%m")
        response['images'] = SaleProductImageSerializer(product).data['images']
        return response


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = [
            'user',
            'date',
            'product',
            'count',
        ]

    def to_representation(self, instance):
        response = CatalogSerializer(instance.product).data
        response['count'] = instance.count
        return response


class TemporaryBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryBasket
        fields = [
            'session',
            'date',
            'product',
            'count',
        ]

    def to_representation(self, instance):
        response = CatalogSerializer(instance.product).data
        response['count'] = instance.count
        return response


class OrderSerializer(serializers.ModelSerializer):
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
        result = []
        for product in Basket.objects.filter(user=self.context['request'].user):
            result.append(BasketSerializer(product).data)
        return result


class OrdersSerializer(serializers.ModelSerializer):
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
        result = []
        for item in OrderItem.objects.filter(order=obj.id):
            result.append(CatalogSerializer(item.product).data)
        return result

    def get_totalCost(self, obj):
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
        return obj.createdAt.strftime("%d/%m/%y %H:%M:%S")

    def to_representation(self, instance):
        result = super().to_representation(instance=instance)
        result["orderId"] = instance.id
        return result


class PaymentSerializer(serializers.ModelSerializer):
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
        avatar = dict()
        if obj.src:
            avatar['src'] = obj.src.path

        else:
            avatar['src'] = None
        avatar['alt'] = obj.alt
        return avatar


class ProfileSerializer(serializers.ModelSerializer):
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
        print(instance)
        print(validated_data['password'])
        instance.set_password(validated_data['password'])
        instance.save()
        print("Пароль установлен на", validated_data['password'])
        return instance


class LoginSerializer(serializers.Serializer):
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
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
