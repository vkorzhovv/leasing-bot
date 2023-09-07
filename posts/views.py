from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, PostMedia
from .serializers import PostSerializer, PostMediaSerializer, CliquePostSerializer
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from src.permissions import IsStaffAndSuperuser

class ApprovePost(APIView):
    permission_classes = [IsStaffAndSuperuser]
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        post.approved = True
        post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data)


@api_view(['GET'])
def get_media_urls(request, post_id):
    permission_classes = [IsStaffAndSuperuser]
    post_media_instances = PostMedia.objects.filter(post_id=post_id)
    serializer = PostMediaSerializer(post_media_instances, many=True)
    media_urls = [item['absolute_media_path'] for item in serializer.data]
    return Response(media_urls)


class CliqueListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = Post.objects.all()
    serializer_class = CliquePostSerializer
