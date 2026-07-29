from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APITestCase
from box_selection.models import Product, Box, Order, OrderItem
from box_selection.services import recommend_box_for_order
from box_selection.serializers import ProductSerializer, BoxSerializer, OrderSerializer


class BoxSelectionServiceTests(TestCase):
    def setUp(self):
        # Create test products
        self.small_product = Product.objects.create(
            name="Small Mug",
            length=Decimal('10.00'),
            width=Decimal('10.00'),
            height=Decimal('10.00'),
            weight=Decimal('0.50')
        )
        self.long_product = Product.objects.create(
            name="Keyboard",
            length=Decimal('45.00'),
            width=Decimal('15.00'),
            height=Decimal('5.00'),
            weight=Decimal('1.20')
        )
        self.heavy_product = Product.objects.create(
            name="Dumbbell",
            length=Decimal('20.00'),
            width=Decimal('10.00'),
            height=Decimal('10.00'),
            weight=Decimal('25.00')
        )

        # Create test boxes
        self.small_box = Box.objects.create(
            name="Small Box",
            internal_length=Decimal('15.00'),
            internal_width=Decimal('15.00'),
            internal_height=Decimal('15.00'),
            max_weight=Decimal('5.00'),
            cost=Decimal('2.00')
        )  # Vol = 3,375 cm3

        self.medium_box = Box.objects.create(
            name="Medium Box",
            internal_length=Decimal('50.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('10.00'),
            cost=Decimal('5.00')
        )  # Vol = 10,000 cm3

        self.same_vol_cheap_box = Box.objects.create(
            name="Medium Cheap Box",
            internal_length=Decimal('50.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('10.00'),
            cost=Decimal('3.50')
        )  # Vol = 10,000 cm3, Cost = $3.50

        self.large_heavy_box = Box.objects.create(
            name="Large Heavy Duty Box",
            internal_length=Decimal('100.00'),
            internal_width=Decimal('100.00'),
            internal_height=Decimal('100.00'),
            max_weight=Decimal('50.00'),
            cost=Decimal('15.00')
        )  # Vol = 1,000,000 cm3

    def test_empty_order(self):
        order = Order.objects.create()
        result = recommend_box_for_order(order)
        self.assertFalse(result['success'])
        self.assertIsNone(result['recommended_box'])
        self.assertEqual(result['total_weight'], Decimal('0.00'))
        self.assertEqual(result['reason'], 'Order contains no items.')

    def test_single_item_fits_in_smallest_box(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.small_product, quantity=1)

        result = recommend_box_for_order(order)
        self.assertTrue(result['success'])
        self.assertEqual(result['recommended_box'], self.small_box)
        self.assertEqual(result['total_weight'], Decimal('0.50'))

    def test_product_rotation_selection(self):
        # Keyboard (45x15x5) rotated fits in medium box (50x20x10) but not small box (15x15x15)
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.long_product, quantity=1)

        result = recommend_box_for_order(order)
        self.assertTrue(result['success'])
        # Medium Cheap Box (cost $3.50) preferred over Medium Box (cost $5.00) due to lower cost for same volume
        self.assertEqual(result['recommended_box'], self.same_vol_cheap_box)

    def test_quantity_expansion_and_weight_limit(self):
        # 8 Mugs = 4.00 kg (Vol = 8,000 cm3). Exceeds Small Box Vol (3,375 cm3), fits in Medium Cheap Box (10,000 cm3, max 10.00 kg)
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.small_product, quantity=8)

        result = recommend_box_for_order(order)
        self.assertTrue(result['success'])
        self.assertEqual(result['recommended_box'], self.same_vol_cheap_box)
        self.assertEqual(result['total_weight'], Decimal('4.00'))

    def test_heavy_item_selects_heavy_duty_box(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.heavy_product, quantity=1)

        result = recommend_box_for_order(order)
        self.assertTrue(result['success'])
        self.assertEqual(result['recommended_box'], self.large_heavy_box)

    def test_no_suitable_box_when_exceeding_all_capacities(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.heavy_product, quantity=3)  # 75 kg > max 50 kg

        result = recommend_box_for_order(order)
        self.assertFalse(result['success'])
        self.assertIsNone(result['recommended_box'])
        self.assertIn('No suitable box found', result['reason'])



class SerializerTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Wireless Mouse",
            length=Decimal('12.00'),
            width=Decimal('8.00'),
            height=Decimal('4.00'),
            weight=Decimal('0.15')
        )

    def test_product_serializer_valid(self):
        data = {
            'name': 'Gaming Headset',
            'length': '20.00',
            'width': '18.00',
            'height': '10.00',
            'weight': '0.45'
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, 'Gaming Headset')

    def test_product_serializer_invalid_dimensions(self):
        data = {
            'name': 'Invalid Product',
            'length': '-5.00',
            'width': '0.00',
            'height': '10.00',
            'weight': '0.45'
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('length', serializer.errors)
        self.assertIn('width', serializer.errors)

    def test_box_serializer_valid(self):
        data = {
            'name': 'Standard Box A',
            'internal_length': '30.00',
            'internal_width': '20.00',
            'internal_height': '15.00',
            'max_weight': '10.00',
            'cost': '4.50'
        }
        serializer = BoxSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_box_serializer_invalid_cost_or_weight(self):
        data = {
            'name': 'Bad Box',
            'internal_length': '30.00',
            'internal_width': '20.00',
            'internal_height': '15.00',
            'max_weight': '-1.00',
            'cost': '0.00'
        }
        serializer = BoxSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('max_weight', serializer.errors)
        self.assertIn('cost', serializer.errors)

    def test_order_serializer_creation(self):
        data = {
            'items': [
                {'product_id': self.product.id, 'quantity': 3}
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
        self.assertEqual(order.items.first().quantity, 3)

    def test_order_serializer_empty_items_invalid(self):
        data = {'items': []}
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('items', serializer.errors)


class ProductAPITests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            length=Decimal('10.00'),
            width=Decimal('10.00'),
            height=Decimal('10.00'),
            weight=Decimal('1.00')
        )

    def test_create_product(self):
        response = self.client.post('/api/products/', {
            'name': 'New Product',
            'length': '15.00',
            'width': '10.00',
            'height': '5.00',
            'weight': '2.00'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_retrieve_non_existent_product(self):
        response = self.client.get('/api/products/9999/')
        self.assertEqual(response.status_code, 404)

    def test_create_product_negative_length(self):
        response = self.client.post('/api/products/', {
            'name': 'Bad Product',
            'length': '-5.00',
            'width': '10.00',
            'height': '10.00',
            'weight': '1.00'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('length', response.data)

    def test_create_product_zero_weight(self):
        response = self.client.post('/api/products/', {
            'name': 'Bad Product',
            'length': '10.00',
            'width': '10.00',
            'height': '10.00',
            'weight': '0.00'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('weight', response.data)

    def test_create_product_missing_field(self):
        response = self.client.post('/api/products/', {
            'name': 'Incomplete Product'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('length', response.data)


class BoxAPITests(APITestCase):
    def setUp(self):
        self.box = Box.objects.create(
            name="Test Box",
            internal_length=Decimal('20.00'),
            internal_width=Decimal('15.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('5.00'),
            cost=Decimal('3.00')
        )

    def test_create_box(self):
        response = self.client.post('/api/boxes/', {
            'name': 'New Box',
            'internal_length': '30.00',
            'internal_width': '25.00',
            'internal_height': '20.00',
            'max_weight': '15.00',
            'cost': '8.00'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Box.objects.count(), 2)

    def test_list_boxes(self):
        response = self.client.get('/api/boxes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_box(self):
        response = self.client.get(f'/api/boxes/{self.box.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Box')

    def test_retrieve_non_existent_box(self):
        response = self.client.get('/api/boxes/9999/')
        self.assertEqual(response.status_code, 404)

    def test_create_box_negative_internal_length(self):
        response = self.client.post('/api/boxes/', {
            'name': 'Bad Box',
            'internal_length': '-10.00',
            'internal_width': '20.00',
            'internal_height': '15.00',
            'max_weight': '10.00',
            'cost': '5.00'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('internal_length', response.data)

    def test_create_box_zero_cost(self):
        response = self.client.post('/api/boxes/', {
            'name': 'Bad Box',
            'internal_length': '20.00',
            'internal_width': '15.00',
            'internal_height': '10.00',
            'max_weight': '5.00',
            'cost': '0.00'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('cost', response.data)


class OrderAPITests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            length=Decimal('10.00'),
            width=Decimal('10.00'),
            height=Decimal('10.00'),
            weight=Decimal('1.00')
        )

    def test_create_order_with_valid_items(self):
        response = self.client.post('/api/orders/', {
            'items': [
                {'product_id': self.product.id, 'quantity': 2}
            ]
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('items', response.data)
        self.assertEqual(len(response.data['items']), 1)

    def test_retrieve_order(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.product, quantity=2)
        response = self.client.get(f'/api/orders/{order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['quantity'], 2)

    def test_create_order_invalid_product_id(self):
        response = self.client.post('/api/orders/', {
            'items': [
                {'product_id': 9999, 'quantity': 1}
            ]
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('product_id', str(response.data))

    def test_create_order_empty_items(self):
        response = self.client.post('/api/orders/', {
            'items': []
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('items', response.data)

    def test_create_order_missing_items(self):
        response = self.client.post('/api/orders/', {
            'status': 'PENDING'
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('items', response.data)

    def test_create_order_quantity_zero(self):
        response = self.client.post('/api/orders/', {
            'items': [
                {'product_id': self.product.id, 'quantity': 0}
            ]
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('quantity', str(response.data))

    def test_create_order_negative_quantity(self):
        response = self.client.post('/api/orders/', {
            'items': [
                {'product_id': self.product.id, 'quantity': -1}
            ]
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('quantity', str(response.data))

    def test_retrieve_non_existent_order(self):
        response = self.client.get('/api/orders/9999/')
        self.assertEqual(response.status_code, 404)


class BoxRecommendationAPITests(APITestCase):
    def setUp(self):
        self.small_product = Product.objects.create(
            name="Small Mug",
            length=Decimal('10.00'),
            width=Decimal('10.00'),
            height=Decimal('10.00'),
            weight=Decimal('0.50')
        )
        self.long_product = Product.objects.create(
            name="Keyboard",
            length=Decimal('45.00'),
            width=Decimal('15.00'),
            height=Decimal('5.00'),
            weight=Decimal('1.20')
        )
        self.heavy_product = Product.objects.create(
            name="Dumbbell",
            length=Decimal('20.00'),
            width=Decimal('10.00'),
            height=Decimal('10.00'),
            weight=Decimal('25.00')
        )
        self.exact_product = Product.objects.create(
            name="Exact Fit Item",
            length=Decimal('15.00'),
            width=Decimal('15.00'),
            height=Decimal('15.00'),
            weight=Decimal('1.00')
        )

        self.small_box = Box.objects.create(
            name="Small Box",
            internal_length=Decimal('15.00'),
            internal_width=Decimal('15.00'),
            internal_height=Decimal('15.00'),
            max_weight=Decimal('5.00'),
            cost=Decimal('2.00')
        )

        self.medium_box = Box.objects.create(
            name="Medium Box",
            internal_length=Decimal('50.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('10.00'),
            cost=Decimal('5.00')
        )

        self.same_vol_cheap_box = Box.objects.create(
            name="Medium Cheap Box",
            internal_length=Decimal('50.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('10.00'),
            cost=Decimal('3.50')
        )

        self.large_heavy_box = Box.objects.create(
            name="Large Heavy Duty Box",
            internal_length=Decimal('100.00'),
            internal_width=Decimal('100.00'),
            internal_height=Decimal('100.00'),
            max_weight=Decimal('50.00'),
            cost=Decimal('15.00')
        )

        self.exact_box = Box.objects.create(
            name="Exact Fit Box",
            internal_length=Decimal('15.00'),
            internal_width=Decimal('15.00'),
            internal_height=Decimal('15.00'),
            max_weight=Decimal('5.00'),
            cost=Decimal('4.00')
        )

    def test_order_fits_in_smallest_box(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.small_product, quantity=1)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['recommended_box']['id'], self.small_box.id)

    def test_order_requires_larger_box(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.long_product, quantity=1)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['recommended_box']['id'], self.same_vol_cheap_box.id)

    def test_order_weight_exceeds_all_boxes(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.heavy_product, quantity=3)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['success'])
        self.assertIsNone(response.data['recommended_box'])
        self.assertIn('No suitable box found', response.data['reason'])

    def test_order_dimensions_exceed_all_boxes(self):
        oversized_product = Product.objects.create(
            name="Oversized",
            length=Decimal('200.00'),
            width=Decimal('200.00'),
            height=Decimal('200.00'),
            weight=Decimal('1.00')
        )
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=oversized_product, quantity=1)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['success'])
        self.assertIsNone(response.data['recommended_box'])
        self.assertIn('No suitable box found', response.data['reason'])

    def test_order_multiple_quantities_same_product(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.small_product, quantity=5)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['total_item_count'], 5)

    def test_non_existent_order_recommendation(self):
        response = self.client.get('/api/orders/9999/recommend-box/')
        self.assertEqual(response.status_code, 404)

    def test_missing_order_id_get(self):
        response = self.client.get('/api/orders/recommend-box/')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Order ID is required', response.data['error'])

    def test_missing_order_id_post(self):
        response = self.client.post('/api/orders/recommend-box/')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Order ID is required', response.data['error'])

    def test_empty_order_recommendation(self):
        order = Order.objects.create()
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['success'])
        self.assertIsNone(response.data['recommended_box'])
        self.assertEqual(response.data['reason'], 'Order contains no items.')

    def test_single_item_exactly_matching_box_dimensions(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.exact_product, quantity=1)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        # exact_box and small_box have identical dimensions and max_weight,
        # but small_box is cheaper ($2.00 vs $4.00), so cheaper box wins
        self.assertEqual(response.data['recommended_box']['id'], self.small_box.id)

    def test_tie_breaking_cheaper_box_wins(self):
        # same_vol_cheap_box ($3.50) vs medium_box ($5.00), same volume
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.long_product, quantity=1)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['recommended_box']['id'], self.same_vol_cheap_box.id)

    def test_tie_breaking_lower_max_weight_wins(self):
        # Create two boxes with same volume and cost but different max_weight
        box_a = Box.objects.create(
            name="Box A",
            internal_length=Decimal('30.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('8.00'),
            cost=Decimal('5.00')
        )
        box_b = Box.objects.create(
            name="Box B",
            internal_length=Decimal('30.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('12.00'),
            cost=Decimal('5.00')
        )
        product = Product.objects.create(
            name="Tie Product",
            length=Decimal('25.00'),
            width=Decimal('15.00'),
            height=Decimal('5.00'),
            weight=Decimal('3.00')
        )
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=product, quantity=1)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['recommended_box']['id'], box_a.id)

    def test_tie_breaking_smallest_id_wins(self):
        # Create two identical boxes
        box_x = Box.objects.create(
            name="Box X",
            internal_length=Decimal('30.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('10.00'),
            cost=Decimal('5.00')
        )
        box_y = Box.objects.create(
            name="Box Y",
            internal_length=Decimal('30.00'),
            internal_width=Decimal('20.00'),
            internal_height=Decimal('10.00'),
            max_weight=Decimal('10.00'),
            cost=Decimal('5.00')
        )
        product = Product.objects.create(
            name="Tie Product 2",
            length=Decimal('25.00'),
            width=Decimal('15.00'),
            height=Decimal('5.00'),
            weight=Decimal('3.00')
        )
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=product, quantity=1)
        response = self.client.get(f'/api/orders/{order.id}/recommend-box/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['recommended_box']['id'], box_x.id)
