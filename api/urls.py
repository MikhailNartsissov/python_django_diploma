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
    PaymentCreateView,
    ProfileListCreateView,
    AvatarListCreateView,
    sign_out_view,
    LoginView,
    CreateUserView,
    PasswordChangeView,
    TagListView,
)

app_name = "api"

routers = DefaultRouter(trailing_slash=False)
routers.register(r'product', CatalogItemViewSet, basename="product")
routers.register(r'basket', BasketViewSet, basename="basket")
routers.register(r'orders', OrderViewSet, basename="orders")
routers.register(r'order', OrderViewSet, basename="order")

urlpatterns = [
    path("", include(routers.urls)),
    path("catalog", CatalogListView.as_view(), name="catalog"),
    path("tags", TagListView.as_view(), name="tags"),
    path("profile", ProfileListCreateView.as_view(), name="profile"),
    path("profile/avatar", AvatarListCreateView.as_view(), name="avatar"),
    path("product/<int:id>/reviews", ReviewCreateView.as_view(), name="review_create"),
    path("payment/<int:id>", PaymentCreateView.as_view(), name="payment_create"),
    path("categories", CategoriesListView.as_view(), name="categories"),
    path("catalog/", CatalogListView.as_view(), name="catalog"),
    path("products/popular", PopularProductsListView.as_view(), name="popular"),
    path("products/limited", LimitedProductsListView.as_view(), name="limited"),
    path("sales", SaleProductsListView.as_view(), name="sales"),
    path("banners", BannerListView.as_view(), name="banners"),
    path("sign-out", sign_out_view, name="sign-out"),
    path("sign-in", LoginView.as_view(), name="sign-in"),
    path("sign-up", CreateUserView.as_view(), name="sign-up"),
    path("profile/password", PasswordChangeView.as_view(), name="password"),
]
