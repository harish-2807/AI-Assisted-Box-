from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Box, Order
from .serializers import (
    ProductSerializer,
    BoxSerializer,
    OrderSerializer,
)
from .services import recommend_box_for_order


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise Http404("Product not found.")


class BoxListCreateView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class BoxDetailView(generics.RetrieveAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise Http404("Box not found.")


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise Http404("Order not found.")


class BoxRecommendationView(APIView):
    def _recommend(self, order_id):
        try:
            order = get_object_or_404(Order, pk=order_id)
        except Http404:
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'Invalid order ID format.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = recommend_box_for_order(order)
        except Exception:
            return Response(
                {'error': 'An unexpected error occurred while processing the recommendation.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        recommended_box_data = (
            BoxSerializer(result['recommended_box']).data
            if result['recommended_box']
            else None
        )

        return Response({
            'success': result['success'],
            'order_id': order.id,
            'recommended_box': recommended_box_data,
            'total_weight': str(result['total_weight']),
            'total_item_volume': str(result['total_item_volume']),
            'total_item_count': result['total_item_count'],
            'reason': result['reason'],
        }, status=status.HTTP_200_OK)

    def get(self, request, order_id=None):
        if not order_id:
            order_id = request.query_params.get('order_id')
        if not order_id:
            return Response(
                {'error': 'Order ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return self._recommend(order_id)

    def post(self, request, order_id=None):
        if not order_id:
            order_id = request.data.get('order_id')
        if not order_id:
            return Response(
                {'error': 'Order ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return self._recommend(order_id)
