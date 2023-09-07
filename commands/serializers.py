from rest_framework import serializers
from .models import Command


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('key', 'text', 'photo')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {data['key']: [data['text'], data['photo']]}

class CommandCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = '__all__'
