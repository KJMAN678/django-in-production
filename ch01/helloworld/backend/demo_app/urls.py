from django.urls import path
from demo_app import views

urlpatterns = [
    path("hello-world-drf/", views.hello_world_drf),
    path("demo-version/", views.demo_version),
    path("custom-version/", views.DemoView.as_view()),
    path("another-custom-version/", views.AnotherView.as_view()),
    path("apiview-class/", views.DemoAPIView.as_view()),
]
