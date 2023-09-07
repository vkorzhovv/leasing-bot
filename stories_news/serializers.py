from rest_framework import serializers
from .models import StoryNews


class StoryNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryNews
        fields = '__all__'
