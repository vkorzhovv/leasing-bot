from django.urls import path
from .views import ProductListView, PromotionProductListView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='list_of_products'),
    path('promotion_products/', PromotionProductListView.as_view(), name='list_of_promotion_products'),
]
