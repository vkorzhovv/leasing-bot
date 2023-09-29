from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BotUser, ExtendedUser


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = '__all__'


class ActivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['activated']



class ManagerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    bot_user_id = serializers.CharField()  # Переименовано поле

    class Meta:
        model = User
        fields = ['username', 'password', 'bot_user_id']  # Обновлено поле

    def create(self, validated_data):
        bot_user_id = validated_data.pop('bot_user_id', None)
        user = User(username=validated_data['username'], is_staff=True)
        user.set_password(validated_data['password'])
        user.save()

        if bot_user_id:
            try:
                bot_user = BotUser.objects.get(user_id=bot_user_id)
                ExtendedUser.objects.create(user=user, bot_user=bot_user)
            except BotUser.DoesNotExist:
                pass

        return user


class BotUserExistsSerializer(serializers.Serializer):
    user_id = serializers.CharField()

    def to_representation(self, instance):
        return {'user_id': instance}


class BotUserCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['city']


class BotUserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ('user_id', 'username', 'phone')
