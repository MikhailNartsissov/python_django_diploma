from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)

urlpatterns = [
    path("", include(routers.urls)),
]
