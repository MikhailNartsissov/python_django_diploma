from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesListView,
    CatalogListView,
    PopularProductsListView,
    LimitedProductsListView,
    SaleProductsListView,
    CatalogViewSet,
    # SaleProductsViewSet,
)

app_name = "api"

routers = DefaultRouter()
routers.register(r'^catalog', CatalogViewSet, basename="catalog")
# routers.register(r'^sales', SaleProductsViewSet, basename="sales")

urlpatterns = [
    path("", include(routers.urls)),
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path("catalog", CatalogListView.as_view(), name="catalog"),
    path("products/popular/", PopularProductsListView.as_view(), name="popular"),
    path("products/limited/", LimitedProductsListView.as_view(), name="limited"),
    # path("sale/", SaleProductsListView.as_view(), name="sale"),
    path("sales", SaleProductsListView.as_view(), name="sales"),
]
