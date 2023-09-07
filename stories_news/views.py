from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StoryNews
from .serializers import StoryNewsSerializer
from src.permissions import IsStaffAndSuperuser


class NewsListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = StoryNews.objects.filter(sort='news', approved=True)
    serializer_class = StoryNewsSerializer


class StoriesListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = StoryNews.objects.filter(sort='story', approved=True)
    serializer_class = StoryNewsSerializer


class ApproveStoryNews(APIView):
    def patch(self, request, pk):
        try:
            story_news = StoryNews.objects.get(pk=pk)
        except StoryNews.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        story_news.approved = True
        story_news.save()

        return Response({"message": "StoryNews approved successfully"}, status=status.HTTP_200_OK)
