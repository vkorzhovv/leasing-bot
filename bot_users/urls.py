from django.urls import path
from .views import *

urlpatterns = [
    path('create_bot_user/', BotUserCreateView.as_view(), name='create_bot_user'),
    path('activate/<str:user_id>/', ActivateUserView.as_view(), name='activate_user'),
    path('update_last_interaction/', update_last_interaction, name='update_last_interaction'),
    path('register/', ManagerView.as_view(), name='user-registration'),
    path('list_bot_user/', BotUserListView.as_view(), name='list_bot_user'),
    path('manager_results/', manager_results, name='manager_results'),
    path('check_bot_user_exists/', CheckBotUserExistsView.as_view(), name='check-bot-user-exists'),
    path('check_bot_user_activated/', CheckBotUserActivatedView.as_view(), name='check-bot-user-activated'),
    path('users_with_category/<int:product_id>/', UsersWithCategoryAPIView.as_view(), name='users-with-category'),
    path('botusers/<str:user_id>/update_city/', BotUserCityUpdateView.as_view(), name='update-city'),
    path('bot_user/search/<str:username>/', BotUserSearchView.as_view(), name='bot-user-search'),
    path('bot_user_id/search/<str:user_id>/', BotUserSearchByIdView.as_view(), name='bot-user-search_by_id'),
]
