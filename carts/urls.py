from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('favorites/', views.favorites, name='favorites'),
    path('add_favorites/', views.add_favorites, name='add_favorites'),
    path('move_to_cart/', views.move_to_cart, name='move_to_cart'),
    path('delete_favorites/', views.delete_favorites, name='delete_favorites'),

    path('checkout/', views.checkout, name='checkout'),
]