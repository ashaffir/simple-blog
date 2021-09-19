from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions

urlpatterns = [
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path(
        "api-docs/",
        include_docs_urls(
            title="TradeCore API Docs",
            permission_classes=[
                permissions.AllowAny,
            ],
        ),
        name="api-docs",
    ),
]
