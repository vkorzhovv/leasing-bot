from django.db import models
from polls.models import PollOptions, Poll
from posts.models import Post
from stories_news.models import StoryNews
from products.models import Product
from categories.models import Category
import datetime


class PollUsersCount(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    users_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class PostUsersCount(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    users_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class StoryNewsViews(models.Model):
    item = models.ForeignKey(StoryNews, on_delete=models.CASCADE, related_name='views')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductViews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    views = models.PositiveIntegerField(default=0)
    kp = models.PositiveIntegerField(default=0)
    manager_chat = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductKp(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='kps')
    kp = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductChat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chats')
    manager_chat = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class CategoryViews(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='views')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ManagerChatRequest(models.Model):
    product = models.TextField()
    manager = models.CharField(max_length=32)
    bot_user = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)


class KpRequest(models.Model):
    product = models.TextField()
    manager = models.CharField(max_length=32)
    bot_user = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)


class PollOptionUserInfo(models.Model):
    option = models.ForeignKey(PollOptions, on_delete=models.CASCADE, related_name='statistic')
    bot_user_tg = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
