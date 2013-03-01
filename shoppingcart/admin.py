from django.contrib import admin
from shoppingcart.models import Product, Category, Store, Order, Item
from django.db import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 1
    ordering = ['name']
    search_fields = ('name', 'description')

admin.site.register(Category, CategoryAdmin,)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'internal_id', 'created_at', 'updated_at', )
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)
    list_display_links = ('name',)
    list_per_page = 10
    ordering = ['name']
    search_fields = ('name', 'email', 'city', 'state')

admin.site.register(Store, StoreAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'store')
    ordering = ['-order_date']
    search_fields = ('user', 'order_date',)


admin.site.register(Order, OrderAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order',)
    ordering = ['order']
    search_fields = ('product', 'order',)

admin.site.register(Item, ItemAdmin)