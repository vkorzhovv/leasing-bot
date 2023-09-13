from rest_framework import serializers
from .models import PollUsersCount, PostUsersCount, StoryNewsViews, ProductViews, CategoryViews, ManagerChatRequest, KpRequest, ProductKp, ProductChat

class PollUsersCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollUsersCount
        fields = '__all__'


class PostUsersCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostUsersCount
        fields = '__all__'


class StoryNewsViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryNewsViews
        fields = '__all__'


class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        fields = '__all__'

class ProductKpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductKp
        fields = '__all__'

class ProductChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductChat
        fields = '__all__'


class CategoryViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryViews
        fields = '__all__'


class ManagerChatRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerChatRequest
        fields = '__all__'


class KpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = KpRequest
        fields = '__all__'
