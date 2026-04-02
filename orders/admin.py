from django.contrib import admin


from orders.models import Cart, CartItem, Order, OrderItem
# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at', 'total_items', 'total_price']
    inlines = [CartItemInline]
    ordering = ['-created_at']

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'cart', 'product', 'quantity']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['total_price']  # Чтобы не редактировалось вручную
    inlines = [OrderItemInline]
    ordering = ['-created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']