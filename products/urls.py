from django.urls import path
from .views import ProductListView, PromotionProductListView, ProductMediaListView, KpPathView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='list_of_products'),
    path('promotion_products/', PromotionProductListView.as_view(), name='list_of_promotion_products'),
    path('product_media/<str:product_id>/', ProductMediaListView.as_view(), name='product_media_list'),
    path('get_kp_path/<int:pk>/', KpPathView.as_view(), name='get_kp_path'),
]
