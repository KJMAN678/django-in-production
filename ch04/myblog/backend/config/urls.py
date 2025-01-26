from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from blog.models import Blog
from django.conf import settings


def index(request):
    Blog.objects.all()
    return HttpResponse("Hello, Django!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("author/", include("author.urls")),
    path("index/", index, name="index"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
