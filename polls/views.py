from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Poll, PollMedia, PollOptions
from .serializers import PollSerializer, PollMediaSerializer
from rest_framework.decorators import api_view
from src.permissions import IsStaffAndSuperuser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType


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




def get_poll_option(request, option_id):
    option = get_object_or_404(PollOptions, id=option_id)
    response_data = {
        'correct': option.correct,
        'options': [o.correct for o in option.poll.options.all()],
        'correct_message': option.poll.correct_message,
        'incorrect_message': option.poll.incorrect_message,
        'option_message': option.poll.option_message,  # Если вы хотите вернуть id связанного объекта Poll
    }
    return JsonResponse(response_data)


def get_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    scheduled_time = poll.scheduled_time if poll.scheduled_time else None
    poll_group = poll.group.id if poll.group else None
    response_data = {
        'options': [(option.id, option.option) for option in poll.options.all()],
        'poll_group': poll_group,
        'title': poll.title,
        'media_paths': [media.absolute_media_path for media in poll.mediafiles.all()],
        'scheduled_time': scheduled_time,
        'manager': poll.user.extended_user.bot_user.user_id

    }
    return JsonResponse(response_data)



class CheckPollExistenceView(APIView):
    def get(self, request, poll_id):
        try:
            obj = Poll.objects.get(id=int(poll_id))
            return Response({'exists': True}, status=status.HTTP_200_OK)
        except Poll.DoesNotExist:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)

    