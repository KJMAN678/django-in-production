from django.urls import path
from blog import views

urlpatterns = [
    path("blogs/", views.get_blogs_by_author),
]
