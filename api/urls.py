from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesListView,
)

app_name = "api"

# routers = DefaultRouter()
# routers.register("", ProductViewSet)

urlpatterns = [
    # path("", include(routers.urls)),
    path("categories/", CategoriesListView.as_view(), name="categories"),
]
