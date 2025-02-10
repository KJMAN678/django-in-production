from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import render


def top_view(request):
    return render(request, "top.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("author/", include("author.urls")),
    path("accounts/", include("allauth.urls")),
    path("", top_view),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
