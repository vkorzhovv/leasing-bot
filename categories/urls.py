from django.urls import path
from .views import CategoryListView


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='list_of_categories'),
]
