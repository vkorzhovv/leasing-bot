from rest_framework.generics import ListAPIView
from .models import Product
from .serializers import ProductListSerializer
from src.permissions import IsStaffAndSuperuser
from django.db.models import Q

class ProductListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(hide=False, promotion=False)
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
