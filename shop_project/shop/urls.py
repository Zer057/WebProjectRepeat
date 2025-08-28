from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('return-refund/', views.return_refund, name='return_refund'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
