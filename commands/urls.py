from django.urls import path
from .views import CommandListView, CommandCreateView


urlpatterns = [
    path('commands/', CommandListView.as_view(), name='list_of_commands'),
    path('create_command/', CommandCreateView.as_view(), name='create_command'),
]
