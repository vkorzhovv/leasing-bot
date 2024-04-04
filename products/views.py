from rest_framework.generics import ListAPIView
from .models import Product, ProductMedia
from .serializers import ProductListSerializer, ProductMediaSerializer, ProductKPSerializer
from src.permissions import IsStaffAndSuperuser
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProductListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(hide=False)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(Q(category_id=category_id) | Q(category2_id=category_id))
        return queryset


class PromotionProductListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(hide=False, promotion=True)
        return queryset


class ProductMediaListView(ListAPIView):
    serializer_class = ProductMediaSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']  # Получаем id продукта из URL
        if product_id.isdigit():
            return ProductMedia.objects.filter(product_id=product_id)
        else:
            return ProductMedia.objects.filter(product__char_id=product_id)



class KpPathView(APIView):
    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductKPSerializer(product)
            return Response({'kp_path': serializer.data['kp_path']})
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
