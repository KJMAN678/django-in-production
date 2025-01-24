from blog import views
from django.urls import path

urlpatterns = [
    path("get_blog/", views.get_blog),
    path("async_get_blog/", views.async_get_blog),
]
