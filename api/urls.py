from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesListView,
    CatalogListView,
    CatalogViewSet,
)

app_name = "api"

routers = DefaultRouter()
routers.register(r'^catalog', CatalogViewSet, basename="catalog")

urlpatterns = [
    path("", include(routers.urls)),
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path("catalog", CatalogListView.as_view(), name="catalog"),
]
