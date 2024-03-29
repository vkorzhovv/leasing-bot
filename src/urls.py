"""
URL configuration for src project.

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
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from bot_users.views import dashboard_view

urlpatterns = [
    path('', dashboard_view),
    path("admin/", admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path("api/", include("bot_users.urls")),
    path("api/", include("commands.urls")),
    path("api/", include("categories.urls")),
    path("api/", include("products.urls")),
    path("api/", include("stories_news.urls")),
    path("api/", include("posts.urls")),
    path("api/", include("polls.urls")),
    path("api/", include("bot_statistics.urls")),
    path("api/", include("xml_import.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
