from django.urls import path
from blog import views

urlpatterns = [
    path("blogs_logs/", views.get_blogs_by_author),
    path("blogs_auto_invalidation/", views.get_blogs_by_author_auto_invalidation),
    path("blogs_anon_view/", views.BlogAnonAPIView.as_view()),
    path("blogs_user_view/", views.BlogUserAPIView.as_view()),
    path("blogs_scoped_view/", views.BlogScopedAPIView.as_view()),
]
