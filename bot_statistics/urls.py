from django.urls import path
from .views import (PostUsersCountCreateView, PollUsersCountCreateView, IncrementStoryNewsViews,
                    StoryNewsViewsCreateView, ProductViewsCreateView, IncrementProductViews,
                    CategoryViewsCreateView, IncrementCategoryViews, ManagerChatRequestCreateView,
                    poll_users_count, download_excel)

urlpatterns = [
    # ... Другие маршруты ...
    path('create_poll_users_count/', PollUsersCountCreateView.as_view(), name='create-poll-users-count'),
    path('create_post_users_count/', PostUsersCountCreateView.as_view(), name='create-post-users-count'),
    path('create_storynews_views/', StoryNewsViewsCreateView.as_view(), name='create-storynews-views'),
    path('create_product_views/', ProductViewsCreateView.as_view(), name='create-product-views'),
    path('increment_story_views/', IncrementStoryNewsViews.as_view(), name='increment-story-views'),
    path('increment_products_views/', IncrementProductViews.as_view(), name='increment-product-views'),
    path('create_category_views/', CategoryViewsCreateView.as_view(), name='create-category-views'),
    path('increment_category_views/', IncrementCategoryViews.as_view(), name='increment-category-views'),
    path('create_manager_request/', ManagerChatRequestCreateView.as_view(), name='create-manager-request'),
    path('download_excel/', download_excel, name='download_excel'),
    path('statistics/', poll_users_count, name='poll-users-count'),
]
