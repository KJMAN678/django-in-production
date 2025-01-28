from django.urls import path
from blog import views

urlpatterns = [
    path("update_blog_title/", views.update_blog_title, name="update_blog_title"),
    path("blog_view/", views.blog_view, name="blog_view"),
]
