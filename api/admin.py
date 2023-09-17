from django.contrib import admin
from .models import (
    Product,
    ProductImage,
    ProductSale,
    Tag,
    Review,
    Category,
    Subcategory,
    ProductSpecifications,
    Basket,
    Profile,
    Order,
    OrderItem,
    Payment,
    ProfileImage,
    TemporaryBasket,
)


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSale)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ProductSpecifications)
admin.site.register(Basket)
admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(TemporaryBasket)
