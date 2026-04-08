from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # don't show extra blank order items by default in the admin interface


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total_price", "created_at"]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)