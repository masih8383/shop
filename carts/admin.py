from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):  # برای نمایش CartItemها درون Cart
    model = CartItem
    extra = 1  # تعداد فرم‌های خالی برای اضافه کردن CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]  # نمایش CartItemها درون Cart

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)