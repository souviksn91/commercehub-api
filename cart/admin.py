from django.contrib import admin
from .models import Cart, CartItem


# inline view to show cart items inside cart admin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# admin view for Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    inlines = [CartItemInline]


# admin view for CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "product", "quantity", "created_at"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)