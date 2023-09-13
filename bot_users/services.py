from django.contrib.auth.models import User
from posts.models import Post
from polls.models import Poll
from stories_news.models import StoryNews
from bot_users.models import BotUser, ExtendedUser
from bot_statistics.models import ManagerChatRequest, KpRequest

#POSTS

def get_approved_posts_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_posts = Post.objects.filter(user=user, approved=True, created_at__range=[start_date, end_date]).count()
    return user_posts

def get_not_approved_posts_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_posts = Post.objects.filter(user=user, approved=False, created_at__range=[start_date, end_date]).count()
    return user_posts


#POLLS
def get_approved_polls_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_polls = Poll.objects.filter(user=user, approved=True, created_at__range=[start_date, end_date]).count()
    return user_polls

def get_not_approved_polls_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_polls = Poll.objects.filter(user=user, approved=False, created_at__range=[start_date, end_date]).count()
    return user_polls


#NEWS
def get_approved_news_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_news = StoryNews.objects.filter(user=user, sort='news', approved=True, created_at__range=[start_date, end_date]).count()
    return user_news

def get_not_approved_news_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_news = StoryNews.objects.filter(user=user, sort='news', approved=False, created_at__range=[start_date, end_date]).count()
    return user_news

#STORIES
def get_approved_stories_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_stories = StoryNews.objects.filter(user=user, sort='story', approved=True, created_at__range=[start_date, end_date]).count()
    return user_stories

def get_not_approved_stories_of_manager(manager, start_date, end_date):
    user = User.objects.get(username=manager)
    user_stories = StoryNews.objects.filter(user=user, sort='story', approved=False, created_at__range=[start_date, end_date]).count()
    return user_stories

def get_chat_requests_of_manager(manager, start_date, end_date): #dbte
    extended_user = ExtendedUser.objects.get(user__username=manager)
    user = extended_user.bot_user.username
    lst = []
    chat_requests = ManagerChatRequest.objects.filter(manager=user, created_at__range=[start_date, end_date]).count()
    # for request in chat_requests:
    #     lst.append(f"({request.product}, Менеджер: {request.manager},Пользователь: {request.bot_user}, Время: {request.created_at}")
    # return ')\n'.join(lst)
    return chat_requests


def get_kp_requests_of_manager(manager, start_date, end_date): #dbte
    extended_user = ExtendedUser.objects.get(user__username=manager)
    user = extended_user.bot_user.username
    lst = []
    kp_requests = KpRequest.objects.filter(manager=user, created_at__range=[start_date, end_date]).count()
    # for request in chat_requests:
    #     lst.append(f"({request.product}, Менеджер: {request.manager},Пользователь: {request.bot_user}, Время: {request.created_at}")
    # return ')\n'.join(lst)
    return kp_requests
