from rest_framework import serializers
from .models import Poll, PollMedia

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'title', 'options', 'correct_answer', 'approved')



class PollMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollMedia
        fields = ('absolute_media_path',)
