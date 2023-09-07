from django.db import models
from polls.models import Poll
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
    item = models.ForeignKey(StoryNews, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductViews(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class CategoryViews(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ManagerChatRequest(models.Model):
    product = models.TextField()
    manager = models.CharField(max_length=32)
    bot_user = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
