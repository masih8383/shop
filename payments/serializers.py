from rest_framework import serializers
from .models import Payment
from orders.serializers import OrderSerializer

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)  # نمایش اطلاعات سفارش به صورت توکار

    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'status', 'transaction_id', 'created_at', 'updated_at']