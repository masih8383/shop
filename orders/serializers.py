from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # نمایش اطلاعات محصول به صورت توکار

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # نمایش آیتم‌های سفارش به صورت توکار

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'items', 'created_at', 'updated_at']