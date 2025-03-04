from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # نمایش اطلاعات محصول به صورت توکار

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # نمایش آیتم‌های سبد خرید به صورت توکار

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']