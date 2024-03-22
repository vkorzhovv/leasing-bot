from rest_framework import serializers
from .models import Product, ProductMedia
import os
from django.conf import settings

class ProductListSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'char_id', 'category', 'category2', 'brand', 'kp', 'photo', 'name', 'description', 'price', 'product_model', 'year', 'equipment', 'manufacturer', 'status', 'currency', 'hide', 'promotion', 'promotion_description', 'position', 'wheels', 'species')

    def get_status(self, obj):
        # Ваша логика для получения display_status на основе obj.status
        return obj.get_status_display()  # Замените на ваш метод


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['absolute_media_path']


class ProductKPSerializer(serializers.ModelSerializer):
    kp_path = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'kp', 'kp_path')

    def get_kp_path(self, obj):
        if obj.kp:
            kp_filename = os.path.basename(obj.kp.path)
            return os.path.join(settings.BASE_DIR, 'media', 'kp', kp_filename)
            # return obj.kp.path
        return None
