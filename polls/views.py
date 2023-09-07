from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Poll, PollMedia
from .serializers import PollSerializer, PollMediaSerializer
from rest_framework.decorators import api_view
from src.permissions import IsStaffAndSuperuser

class ApprovePoll(APIView):
    permission_classes = [IsStaffAndSuperuser]
    def patch(self, request, poll_id):
        try:
            poll = Poll.objects.get(pk=poll_id)
        except Poll.DoesNotExist:
            return Response({'error': 'Poll not found'}, status=status.HTTP_404_NOT_FOUND)

        poll.approved = True
        poll.save()

        serializer = PollSerializer(poll)
        return Response(serializer.data)


@api_view(['GET'])
def get_poll_media_urls(request, poll_id):
    permission_classes = [IsStaffAndSuperuser]
    poll_media_instances = PollMedia.objects.filter(poll_id=poll_id)
    serializer = PollMediaSerializer(poll_media_instances, many=True)
    media_urls = [item['absolute_media_path'] for item in serializer.data]
    return Response(media_urls)
