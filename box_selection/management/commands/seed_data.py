from decimal import Decimal
from django.core.management.base import BaseCommand
from box_selection.models import Product, Box, Order, OrderItem


class Command(BaseCommand):
    help = 'Seeds the database with sample products, boxes, and orders for manual testing.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Clear existing data
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Box.objects.all().delete()

        # --- Products ---
        products = [
            Product.objects.create(
                name='Small Mug',
                length=Decimal('10.00'),
                width=Decimal('10.00'),
                height=Decimal('10.00'),
                weight=Decimal('0.50'),
            ),
            Product.objects.create(
                name='Hardcover Book',
                length=Decimal('25.00'),
                width=Decimal('18.00'),
                height=Decimal('4.00'),
                weight=Decimal('1.20'),
            ),
            Product.objects.create(
                name='Dumbbell',
                length=Decimal('30.00'),
                width=Decimal('15.00'),
                height=Decimal('15.00'),
                weight=Decimal('25.00'),
            ),
        ]
        self.stdout.write(f'Created {len(products)} products.')

        # --- Boxes ---
        boxes = [
            Box.objects.create(
                name='Small Box',
                internal_length=Decimal('20.00'),
                internal_width=Decimal('20.00'),
                internal_height=Decimal('15.00'),
                max_weight=Decimal('5.00'),
                cost=Decimal('2.50'),
            ),
            Box.objects.create(
                name='Medium Box',
                internal_length=Decimal('50.00'),
                internal_width=Decimal('30.00'),
                internal_height=Decimal('20.00'),
                max_weight=Decimal('15.00'),
                cost=Decimal('6.00'),
            ),
            Box.objects.create(
                name='Large Box',
                internal_length=Decimal('100.00'),
                internal_width=Decimal('80.00'),
                internal_height=Decimal('60.00'),
                max_weight=Decimal('50.00'),
                cost=Decimal('18.00'),
            ),
        ]
        self.stdout.write(f'Created {len(boxes)} boxes.')

        # --- Orders ---
        # Order 1: 1x Small Mug -> fits Small Box
        order1 = Order.objects.create()
        OrderItem.objects.create(order=order1, product=products[0], quantity=1)

        # Order 2: 1x Hardcover Book -> needs Medium Box (25x18x4 doesn't fit in Small Box 20x20x15)
        order2 = Order.objects.create()
        OrderItem.objects.create(order=order2, product=products[1], quantity=1)

        # Order 3: 2x Hardcover Book -> fits Medium Box
        order3 = Order.objects.create()
        OrderItem.objects.create(order=order3, product=products[1], quantity=2)

        # Order 4: 1x Dumbbell -> needs Large Box (25 kg > Small/Medium max weight)
        order4 = Order.objects.create()
        OrderItem.objects.create(order=order4, product=products[2], quantity=1)

        # Order 5: 3x Dumbbell -> exceeds all boxes (75 kg > 50 kg)
        order5 = Order.objects.create()
        OrderItem.objects.create(order=order5, product=products[2], quantity=3)

        self.stdout.write(f'Created 5 orders with items.')
        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
