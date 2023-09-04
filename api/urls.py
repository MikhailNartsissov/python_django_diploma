from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesListView,
    CatalogListView,
    PopularProductsListView,
    LimitedProductsListView,
    SaleProductsListView,
    BannerListView,
    CatalogItemViewSet,
    ReviewCreateView,
    BasketViewSet,
    OrderViewSet,
    OrdersViewSet,
)

app_name = "api"

routers = DefaultRouter(trailing_slash=False)
routers.register(r'product', CatalogItemViewSet, basename="product")
routers.register(r'basket', BasketViewSet, basename="basket")
routers.register(r'orders', OrdersViewSet, basename="orders")
routers.register(r'order', OrderViewSet, basename="order")

urlpatterns = [
    path("", include(routers.urls)),
    path("catalog/", CatalogListView.as_view(), name="catalog"),
    path("product/<int:id>/reviews", ReviewCreateView.as_view(), name="review_create"),
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path("catalog", CatalogListView.as_view(), name="catalog"),
    path("products/popular/", PopularProductsListView.as_view(), name="popular"),
    path("products/limited/", LimitedProductsListView.as_view(), name="limited"),
    path("sales", SaleProductsListView.as_view(), name="sales"),
    path("banners/", BannerListView.as_view(), name="banners"),
]
