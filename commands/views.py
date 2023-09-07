from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Command
from .serializers import CommandSerializer, CommandCreateSerializer
from src.permissions import IsStaffAndSuperuser


class CommandListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

class CommandCreateView(CreateAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = Command.objects.all()
    serializer_class = CommandCreateSerializer
