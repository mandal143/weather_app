# weather_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_city/', views.add_city, name='add_city'),
    path('remove_city/<int:city_id>/', views.remove_city, name='remove_city'),
]
