from django.urls import path
from .views import CartDetailView, CartItemCreateView, CartItemDetailView

urlpatterns = [
    path('carts/<int:user_id>/', CartDetailView.as_view(), name='cart-detail'),
    path('cart-items/', CartItemCreateView.as_view(), name='cart-item-create'),
    path('cart-items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
]