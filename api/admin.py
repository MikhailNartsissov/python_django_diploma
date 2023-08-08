from django.contrib import admin
from .models import Product, ProductImage, ProductSale, Tag, Review, Category, Subcategory


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSale)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Subcategory)
