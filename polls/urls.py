from django.urls import path
from .views import get_poll_media_urls, ApprovePoll, get_poll_option, get_poll, CheckPollExistenceView

urlpatterns = [
    path('approve_poll/<int:poll_id>/', ApprovePoll.as_view(), name='approve-poll'),
    path('get_poll_media_urls/<int:poll_id>/', get_poll_media_urls, name='get_poll_media_urls'),
    path('get_poll_option/<int:option_id>/', get_poll_option, name='get_poll_option'),
    path('get_poll/<int:poll_id>/', get_poll, name='get_poll'),
    path('check_poll_exist/<int:poll_id>/', CheckPollExistenceView.as_view(), name='check_poll_exist')
]
