from django.urls import path
from .views import StoriesListView, NewsListView, ApproveStoryNews


urlpatterns = [
    path('news/', NewsListView.as_view(), name='list_of_news'),
    path('stories/', StoriesListView.as_view(), name='list_of_stories'),
    path('approve/<int:pk>/', ApproveStoryNews.as_view(), name='approve-story-news'),
]
