from django.urls import path
from blog import views

urlpatterns = [
    path("blog_get_create/", views.BlogGetCreateView.as_view()),
    path("blog_get_update/", views.BlogGetUpdateView.as_view()),
    path("blog_get_update_filter/", views.BlogGetUpdateFilterView.as_view()),
]
