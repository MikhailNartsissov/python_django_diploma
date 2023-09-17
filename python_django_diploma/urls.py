"""
URL configuration for python_django_diploma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile', TemplateView.as_view(template_name="frontend/profile.html")),
    path('history-order', TemplateView.as_view(template_name="frontend/historyorder.html")),
    path('sign-in', TemplateView.as_view(template_name="frontend/signIn.html")),
    path('accounts/login/', TemplateView.as_view(template_name="frontend/signIn.html")),
    path('catalog', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('sale', TemplateView.as_view(template_name="frontend/sale.html")),
    path('sign-up', TemplateView.as_view(template_name="frontend/signUp.html")),
    path('', include('frontend.urls')),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
