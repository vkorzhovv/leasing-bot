from rest_framework import serializers
from .models import Post, PostMedia

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'text', 'approved')



class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('absolute_media_path',)


class CliqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('media',)

class CliquePostSerializer(serializers.ModelSerializer):
    mediafiles = CliqueSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'approved', 'mediafiles')
