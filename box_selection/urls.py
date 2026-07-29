from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    BoxListCreateView,
    BoxDetailView,
    OrderListCreateView,
    OrderDetailView,
    BoxRecommendationView,
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('boxes/', BoxListCreateView.as_view(), name='box-list-create'),
    path('boxes/<int:pk>/', BoxDetailView.as_view(), name='box-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/recommend-box/', BoxRecommendationView.as_view(), name='box-recommendation'),
    path('orders/recommend-box/', BoxRecommendationView.as_view(), name='box-recommendation-query'),
]
