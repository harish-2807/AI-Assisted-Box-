from decimal import Decimal
from rest_framework import serializers
from .models import Product, Box, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving Product catalog items.
    Validates physical dimensions and weight to ensure positive values.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'length', 'width', 'height', 'weight']

    def validate_length(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Length must be greater than zero.")
        return value

    def validate_width(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Width must be greater than zero.")
        return value

    def validate_height(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Height must be greater than zero.")
        return value

    def validate_weight(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Weight must be greater than zero.")
        return value


class BoxSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving shipping Box containers.
    Validates internal dimensions, max weight capacity, and cost to ensure positive values.
    """
    class Meta:
        model = Box
        fields = [
            'id',
            'name',
            'internal_length',
            'internal_width',
            'internal_height',
            'max_weight',
            'cost'
        ]

    def validate_internal_length(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Internal length must be greater than zero.")
        return value

    def validate_internal_width(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Internal width must be greater than zero.")
        return value

    def validate_internal_height(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Internal height must be greater than zero.")
        return value

    def validate_max_weight(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Maximum weight capacity must be greater than zero.")
        return value

    def validate_cost(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Cost must be greater than zero.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem line items.
    Supports writing product references via `product_id` and reading full nested Product objects.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
        help_text="ID of the product to order"
    )
    quantity = serializers.IntegerField(
        default=1,
        min_value=1,
        help_text="Quantity of the product (must be at least 1)"
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving Orders.
    Handles nested creation of OrderItems and validates that orders contain at least one valid item.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at', 'items']
        read_only_fields = ['id', 'created_at']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("An order must contain at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        order_items = [
            OrderItem(
                order=order,
                product=item_data['product'],
                quantity=item_data.get('quantity', 1)
            )
            for item_data in items_data
        ]
        OrderItem.objects.bulk_create(order_items)

        return order

