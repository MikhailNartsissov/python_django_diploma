from django.db import models
from django.contrib.auth.models import User


def category_images_directory_path(instance: "Category", filename: str) -> str:
    """
    Returns path, where category or subcategory image will be saved
    :param instance:
    :param filename:
    :return:
    """
    return "api/categories/{filename}".format(filename=filename)


class Category(models.Model):
    """
    Class for top level menu items
    Images stored in "api/categories"
    """
    id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0, default=1, unique=True)
    title = models.CharField(max_length=30, blank=False, null=False)
    src = models.ImageField(null=True, blank=True, upload_to=category_images_directory_path)
    alt = models.CharField(max_length=50, default="There should be an image of the category")


class Subcategory(models.Model):
    """
    Class for lower level menu items
    Images stored in "api/categories" with the images for Categories
    Relations with corresponding Categories establish through "category" Foreign key
    """
    id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0, default=1001, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    src = models.ImageField(null=True, blank=True, upload_to=category_images_directory_path)
    alt = models.CharField(max_length=50, default="There should be an image of the subcategory")


class Tag(models.Model):
    """
    Class for product tags
    Relations with corresponding Subcategories establish through "category" Many to Many field
    """
    name = models.CharField(max_length=20, null=False, blank=False)
    category = models.ManyToManyField(Subcategory)


class Product(models.Model):
    """
    Class for product information
    Images stored in separate model named "ProductImage"
    Relations with corresponding Subcategories establish through "category" Foreign key
    Relations with corresponding Tags establish through "tags" Many to Many field
    """

    category = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=True, max_length=500)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    freeDelivery = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    limited = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        """
        Returns string representation of Product instance
        :return:
        """
        return f"Product(pk={self.pk}, name={self.title!r})"


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    """
    Returns path, where Product instance images will be saved
    :param instance:
    :param filename:
    :return:
    """
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    """
    Class for product images
    Relation with corresponding Product instance establishes through "product" Foreign key
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    src = models.ImageField(null=True, blank=True, upload_to=product_images_directory_path)
    alt = models.CharField(max_length=50, default="There should be an image of the product")


class Review(models.Model):
    """
    Class for product reviews
    Relation with corresponding User establishes through "author" Foreign key
    Relation with corresponding Product instance establishes through "product" Foreign key
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=5)
    text = models.TextField(null=False, blank=False, max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductSale(models.Model):
    """
    Class for products on sale
    Relation with corresponding Product instance establishes through "product" Foreign key
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    salePrice = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()


class ProductSpecifications(models.Model):
    """
    Class for product specifications
    Relation with corresponding Product instance establishes through "product" Foreign key
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=50)
    value = models.CharField(null=False, blank=True, max_length=50)


class Basket(models.Model):
    """
    Class for user basket items
    Relation with corresponding User instance establishes through "user" Foreign key
    Relation with corresponding Product instance establishes through "product" Foreign key
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_id')
    count = models.DecimalField(max_digits=6, decimal_places=0)


class TemporaryBasket(models.Model):
    """
    Class for Anonymous users temporary basket items
    Values of the field "session" are session identifiers, used as an id of the specific Anonymous user
    When corresponding user logs in, items from the temporary basket moving into Basket instances with the user id.
    Relation with corresponding Product instance establishes through "product" Foreign key
    """

    session = models.CharField(max_length=32, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tmp')
    count = models.DecimalField(max_digits=6, decimal_places=0)


def avatar_images_directory_path(instance: "ProfileImage", filename: str) -> str:
    """
    Returns path, where user Profile image will be saved
    :param instance:
    :param filename:
    :return:
    """
    return "avatars/user_{pk}/images/{filename}".format(
        pk=instance.profile.pk,
        filename=filename,
    )


class Profile(models.Model):
    """
    Class for additional information about users
    Relation with corresponding User instance establishes through "user" Foreign key
    Relation with corresponding Product instance establishes through "product" Foreign key
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=80, null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.PositiveSmallIntegerField(null=False, blank=False)


class ProfileImage(models.Model):
    """
    Class for user profile images
    Relation with corresponding Profile instance establishes through "profile" Foreign key
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    src = models.ImageField(null=True, blank=True, upload_to=avatar_images_directory_path)
    alt = models.CharField(max_length=50, default="There should be an image of the profile")


class Order(models.Model):
    """
    Class for user orders
    Relation with corresponding User instance establishes through "user" Foreign key
    Field "phone" was made PositiveInteger in sake of making sure that it contains digits only
    """
    createdAt = models.DateTimeField(auto_now_add=True)
    paymentType = models.CharField(max_length=30, default='online')
    deliveryType = models.CharField(max_length=30, default='ordinary')
    status = models.CharField(max_length=90, default='accepted')
    city = models.CharField(max_length=100, default="Enter city of the delivery")
    address = models.TextField(max_length=200, default="Enter address of the delivery")
    fullName = models.CharField(max_length=80)
    email = models.EmailField(default='user@domain.com')
    phone = models.PositiveSmallIntegerField(default=0000000)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class OrderItem(models.Model):
    """
    Class for user Order items
    Relation with corresponding Order instance establishes through "order" Foreign key
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=6, decimal_places=0)


class Payment(models.Model):
    """
    Class for payments
    Relation with corresponding Order instance establishes through "order" Foreign key
    Rest fields contain information about bank card, used to make the payment
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    number = models.CharField(max_length=20, null=False, blank=False)
    month = models.CharField(max_length=2, null=False, blank=False)
    year = models.CharField(max_length=4, null=False, blank=False)
    code = models.CharField(max_length=3, null=False, blank=False)
