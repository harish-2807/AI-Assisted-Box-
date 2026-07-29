from django.contrib import admin
from .models import Product, Box, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ('product',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'length', 'width', 'height', 'weight')
    search_fields = ('name',)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'internal_length',
        'internal_width',
        'internal_height',
        'max_weight',
        'cost'
    )
    search_fields = ('name',)
    list_filter = ('max_weight', 'cost')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'total_items')
    list_filter = ('status', 'created_at')
    search_fields = ('id',)
    inlines = [OrderItemInline]

    @admin.display(description='Total Line Items')
    def total_items(self, obj):
        return obj.items.count()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__id')
    raw_id_fields = ('order', 'product')


