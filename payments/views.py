from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from order.models import Order

class PaymentCreateView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            # دریافت سفارش مربوطه
            order_id = request.data.get('order')
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return Response({"error": "سفارش مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

            # بررسی وضعیت سفارش
            if order.status != 'pending':
                return Response({"error": "سفارش قبلاً پرداخت شده یا لغو شده است."}, status=status.HTTP_400_BAD_REQUEST)

            # ذخیره پرداخت
            payment = serializer.save()

            # بررسی وضعیت پرداخت (مثلاً از درگاه پرداخت)
            # اینجا می‌توانید با درگاه پرداخت ارتباط برقرار کنید و وضعیت پرداخت را بررسی کنید.
            # برای مثال، فرض می‌کنیم پرداخت موفق بوده است:
            payment.status = 'success'
            payment.save()

            # به‌روزرسانی وضعیت سفارش
            order.status = 'paid'
            order.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return None

    def get(self, request, pk):
        payment = self.get_object(pk)
        if payment:
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        return Response({"error": "پرداخت مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        payment = self.get_object(pk)
        if payment:
            serializer = PaymentSerializer(payment, data=request.data)
            if serializer.is_valid():
                # بررسی وضعیت جدید پرداخت
                new_status = request.data.get('status')
                if new_status not in ['pending', 'success', 'failed']:
                    return Response({"error": "وضعیت پرداخت نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

                # به‌روزرسانی وضعیت پرداخت
                payment.status = new_status
                payment.save()

                # اگر پرداخت موفق بود، وضعیت سفارش را به‌روزرسانی کنید
                if new_status == 'success':
                    order = payment.order
                    order.status = 'paid'
                    order.save()

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "پرداخت مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        payment = self.get_object(pk)
        if payment:
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "پرداخت مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
