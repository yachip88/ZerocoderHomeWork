from django.urls import path

from . import views

urlpatterns = [
    path("count/", views.users_count, name="users_count"),
]
