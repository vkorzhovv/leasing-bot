from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer
from src.permissions import IsStaffAndSuperuser


class CategoryListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
