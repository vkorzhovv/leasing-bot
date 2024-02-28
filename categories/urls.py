from django.urls import path
from .views import CategoryListView, GetManager


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='list_of_categories'),
    path('get_manager/<int:product_id>/', GetManager.as_view(), name='get_manager'),
]
