from django.urls import path
from .views import get_poll_media_urls, ApprovePoll

urlpatterns = [
    path('approve_poll/<int:poll_id>/', ApprovePoll.as_view(), name='approve-poll'),
    path('get_poll_media_urls/<int:poll_id>/', get_poll_media_urls, name='get_poll_media_urls'),
]
