from django.urls import path
from blog import views

urlpatterns = [
    path("blogs/", views.get_blogs_by_author),
    path("blogs_auto_invalidation/", views.get_blogs_by_author_auto_invalidation),
]
