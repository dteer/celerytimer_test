from django.urls import path, include
from web import views

urlpatterns = [
    path("app", views.index)
]
