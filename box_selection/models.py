from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    """
    Represents an item/product available in the warehouse catalog.
    Dimensions are measured in centimeters (cm) and weight in kilograms (kg).
    """
    name = models.CharField(max_length=255)
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Length in cm"
    )
    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Width in cm"
    )
    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Height in cm"
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Weight in kg"
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height} cm, {self.weight} kg)"


class Box(models.Model):
    """
    Represents a shipping container/box available in the warehouse.
    Internal dimensions in cm, max weight capacity in kg, and cost in currency units.
    """
    name = models.CharField(max_length=255)
    internal_length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Internal length in cm"
    )
    internal_width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Internal width in cm"
    )
    internal_height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Internal height in cm"
    )
    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Maximum weight capacity in kg"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Cost per box"
    )

    class Meta:
        ordering = ['cost', 'name']
        verbose_name = 'Box'
        verbose_name_plural = 'Boxes'

    def __str__(self):
        return f"{self.name} ({self.internal_length}x{self.internal_width}x{self.internal_height} cm, Max Weight: {self.max_weight} kg, Cost: ${self.cost})"


class Order(models.Model):
    """
    Represents a customer order containing one or more order items.
    """
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSED = 'PROCESSED', 'Processed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.get_status_display()} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class OrderItem(models.Model):
    """
    Represents an individual line item (product + quantity) within a customer order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Quantity of product in order"
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order_id})"

