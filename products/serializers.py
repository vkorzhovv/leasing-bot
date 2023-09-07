from rest_framework import serializers
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'category2', 'brand', 'photo', 'name', 'description', 'price', 'product_model', 'year', 'equipment', 'manufacturer', 'status', 'currency', 'hide', 'promotion', 'promotion_description', 'position', 'wheels', 'species')
