from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('meal/<str:meal_id>/', views.detail, name='detail'),
]
