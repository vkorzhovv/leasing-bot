from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer
from src.permissions import IsStaffAndSuperuser
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from bot_users.serializers import UserSerializer
from products.models import Product



class CategoryListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GetManager(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            category = product.category
            try:
                last_position = category.last_position
            except:
                last_position = 0
            managers = list(category.users.all())
            if managers:
                managers = [UserSerializer(i).data for i in managers]
                next_position = (last_position + 1) % len(managers)
                category.last_position = next_position
                category.save()
                next_manager = managers[next_position]
                return Response(next_manager)
            else:
                return None
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)




            
            

            
            