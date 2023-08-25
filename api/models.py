from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)


def category_images_directory_path(instance: "Category", filename: str) -> str:
    return "api/categories/{filename}".format(filename=filename)


def subcategory_images_directory_path(instance: "Subcategory", filename: str) -> str:
    return "api/categories/{filename}".format(filename=filename)


class Category(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0, default=1, unique=True)
    title = models.CharField(max_length=30, blank=False, null=False)
    src = models.ImageField(null=True, blank=True, upload_to=category_images_directory_path)
    alt = models.CharField(max_length=50, default="There should be an image of the category")


class Subcategory(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0, default=1001, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    src = models.ImageField(null=True, blank=True, upload_to=category_images_directory_path)
    alt = models.CharField(max_length=50, default="There should be an image of the category")


class Product(models.Model):
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

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.title!r})"


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    src = models.ImageField(null=True, blank=True, upload_to=product_images_directory_path)
    alt = models.CharField(max_length=50, default="There should be an image of the product")


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=5)
    text = models.TextField(null=False, blank=False, max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    salePrice = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()


class ProductSpecifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=50)
    value = models.CharField(null=False, blank=True, max_length=50)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_id')
    count = models.DecimalField(max_digits=6, decimal_places=0)
