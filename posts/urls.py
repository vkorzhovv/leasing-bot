from django.urls import path
from .views import ApprovePost, get_media_urls, CliqueListView, CheckPostExistenceView, DisApprovePost

urlpatterns = [
    # ... другие URL-пути ...
    path('approve_post/<int:post_id>/', ApprovePost.as_view(), name='approve-post'),
    path('disapprove_post/<int:post_id>/', DisApprovePost.as_view(), name='disapprove-post'),
    path('get_media_urls/<int:post_id>/', get_media_urls, name='get_media_urls'),
    path('get_media_post/', CliqueListView.as_view(), name='media_post'),
    path('check_post_exist/<int:post_id>/', CheckPostExistenceView.as_view(), name='check_post_exist')
]
