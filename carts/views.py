from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartDetailView(APIView):
    def get_object(self, user_id):
        try:
            return Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return None

    def get(self, request, user_id):
        cart = self.get_object(user_id)
        if cart:
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

class CartItemCreateView(APIView):
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailView(APIView):
    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return None

    def delete(self, request, pk):
        cart_item = self.get_object(pk)
        if cart_item:
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
