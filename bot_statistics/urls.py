from django.urls import path
from .views import (PostUsersCountCreateView, PollUsersCountCreateView, IncrementStoryNewsViews,
                    StoryNewsViewsCreateView, ProductViewsCreateView, IncrementProductViews,
                    CategoryViewsCreateView, IncrementCategoryViews, ManagerChatRequestCreateView,
                    KpRequestCreateView, IncrementProductManagerChat, IncrementProductKp,
                    poll_users_count, download_excel, category_products, ProductChatCreateView,
                    ProductKpCreateView, create_poll_option_user_info, poll_option_user_info_list,
                    download_polls_excel)

urlpatterns = [
    # ... Другие маршруты ...
    path('create_poll_users_count/', PollUsersCountCreateView.as_view(), name='create-poll-users-count'),
    path('create_post_users_count/', PostUsersCountCreateView.as_view(), name='create-post-users-count'),
    path('create_storynews_views/', StoryNewsViewsCreateView.as_view(), name='create-storynews-views'),
    path('create_product_views/', ProductViewsCreateView.as_view(), name='create-product-views'),
    path('create_product_kp/', ProductKpCreateView.as_view(), name='create-product-kp'),
    path('create_product_chat/', ProductChatCreateView.as_view(), name='create-product-chat'),
    path('increment_story_views/', IncrementStoryNewsViews.as_view(), name='increment-story-views'),
    path('increment_products_views/', IncrementProductViews.as_view(), name='increment-product-views'),
    path('increment_products_manager_chat/', IncrementProductManagerChat.as_view(), name='increment-product-manager-chat'),
    path('increment_products_kp/', IncrementProductKp.as_view(), name='increment-product-kp'),
    path('create_category_views/', CategoryViewsCreateView.as_view(), name='create-category-views'),
    path('increment_category_views/', IncrementCategoryViews.as_view(), name='increment-category-views'),
    path('create_option_user_info/', create_poll_option_user_info, name='create_option_user_info'),
    path('create_manager_request/', ManagerChatRequestCreateView.as_view(), name='create-manager-request'),
    path('create_kp_request/',KpRequestCreateView.as_view(), name='create-kp-request'),
    path('download_excel/', download_excel, name='download_excel'),
    path('download_polls_excel/', download_polls_excel, name='download_polls_excel'),
    path('statistics/', poll_users_count, name='poll-users-count'),
    path('category_products/<int:category_id>/<str:start_date>/<str:end_date>/', category_products, name='category_products'),
    path('poll_option_user_infos/', poll_option_user_info_list, name='poll_option_user_info_list'),
]
