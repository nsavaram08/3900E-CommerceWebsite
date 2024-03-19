from django.urls import path
from . import views

app_name = 'Cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<uuid:pk>/', views.cart_add, name='cart_add'),
    path('remove/<uuid:pk>/', views.cart_remove, name='cart_remove'),
]
