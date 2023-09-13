from rest_framework import generics
from .models import PollUsersCount, PostUsersCount, StoryNewsViews, ProductViews, CategoryViews, ManagerChatRequest, KpRequest, ProductChat, ProductKp
from .serializers import PollUsersCountSerializer, PostUsersCountSerializer, StoryNewsViewsSerializer, ProductViewsSerializer, CategoryViewsSerializer, ManagerChatRequestSerializer, KpRequestSerializer, ProductChatSerializer, ProductKpSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models.functions import TruncMonth
from src.permissions import IsStaffAndSuperuser
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.timezone import make_aware
from bot_users.models import BotUser
from products.models import Product
from categories.models import Category
from stories_news.models import StoryNews
from django.db.models import Count


class PollUsersCountCreateView(generics.CreateAPIView):
    queryset = PollUsersCount.objects.all()
    serializer_class = PollUsersCountSerializer


class PostUsersCountCreateView(generics.CreateAPIView):
    queryset = PostUsersCount.objects.all()
    serializer_class = PostUsersCountSerializer


class StoryNewsViewsCreateView(generics.CreateAPIView):
    queryset = StoryNewsViews.objects.all()
    serializer_class = StoryNewsViewsSerializer


class ProductViewsCreateView(generics.CreateAPIView):
    queryset = ProductViews.objects.all()
    serializer_class = ProductViewsSerializer

class ProductKpCreateView(generics.CreateAPIView):
    queryset = ProductKp.objects.all()
    serializer_class = ProductKpSerializer

class ProductChatCreateView(generics.CreateAPIView):
    queryset = ProductChat.objects.all()
    serializer_class = ProductChatSerializer


class IncrementStoryNewsViews(APIView):
    def post(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')  # Предполагаем, что вы передаете item_id через POST запрос
        if item_id is not None:
            try:
                story_news_views = StoryNewsViews.objects.get(item_id=item_id)
                story_news_views.views += 1
                story_news_views.save()
                serializer = StoryNewsViewsSerializer(story_news_views)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except StoryNewsViews.DoesNotExist:
                return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "item_id is required."}, status=status.HTTP_400_BAD_REQUEST)


class IncrementProductViews(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')  # Предполагаем, что вы передаете item_id через POST запрос
        if product_id is not None:
            try:
                product_views = ProductViews.objects.get(product_id=product_id)
                product_views.views += 1
                product_views.save()
                serializer = ProductViewsSerializer(product_views)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ProductViews.DoesNotExist:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)


class IncrementProductKp(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')  # Предполагаем, что вы передаете item_id через POST запрос
        if product_id is not None:
            try:
                product_views = ProductViews.objects.get(product_id=product_id)
                product_views.kp += 1
                product_views.save()
                serializer = ProductViewsSerializer(product_views)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ProductViews.DoesNotExist:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)


class IncrementProductManagerChat(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')  # Предполагаем, что вы передаете item_id через POST запрос
        if product_id is not None:
            try:
                product_views = ProductViews.objects.get(product_id=product_id)
                product_views.manager_chat += 1
                product_views.save()
                serializer = ProductViewsSerializer(product_views)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ProductViews.DoesNotExist:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)




class CategoryViewsCreateView(generics.CreateAPIView):
    queryset = CategoryViews.objects.all()
    serializer_class = CategoryViewsSerializer


class IncrementCategoryViews(APIView):
    def post(self, request, *args, **kwargs):
        category_id = request.data.get('category_id')  # Предполагаем, что вы передаете item_id через POST запрос
        if category_id is not None:
            try:
                category_views = CategoryViews.objects.get(category_id=category_id)
                category_views.views += 1
                category_views.save()
                serializer = CategoryViewsSerializer(category_views)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CategoryViews.DoesNotExist:
                return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "category_id is required."}, status=status.HTTP_400_BAD_REQUEST)




from django.utils import timezone
from datetime import timedelta

@login_required
def poll_users_count(request):
    permission_classes = [IsStaffAndSuperuser]
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))

    categories_entries = []
    categories = Category.objects.all()
    for category in categories:
        category_views_count = category.views.filter(created_at__range=(start_date, end_date)).count()
        categories_entries.append([category, category_views_count])
    categories_entries = categories_entries[1:]

    storynews_entries = []
    storynews = StoryNews.objects.all()
    for item in storynews:
        storynews_views_count = item.views.filter(created_at__range=(start_date, end_date)).count()
        storynews_entries.append([item, storynews_views_count])

    product_entries = []
    products = Product.objects.all()
    for product in products:
        product_chat_count = product.chats.filter(created_at__range=(start_date, end_date)).count()
        product_kp_count = product.kps.filter(created_at__range=(start_date, end_date)).count()
        product_views_count = product.views.filter(created_at__range=(start_date, end_date)).count()
        product_entries.append([product, product_views_count, product_kp_count, product_chat_count])


    entries = PollUsersCount.objects.filter(created_at__range=(start_date, end_date))
    posts_entries = PostUsersCount.objects.filter(created_at__range=(start_date, end_date))
    users_entries = BotUser.objects.filter(created_at__range=(start_date, end_date)).count()

    try:
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
    except:
        start_date_str = None
        end_date_str = None

    return render(request, 'bot_statistics/poll_users_count.html', {'start_date_str': start_date_str, 'end_date_str': end_date_str, 'product_entries': product_entries, 'entries': entries, 'posts_entries': posts_entries, 'storynews_entries': storynews_entries, 'categories_entries': categories_entries, 'users_entries': users_entries})


from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO
from openpyxl.styles import Font

def download_excel(request):
    wb = Workbook()
    ws = wb.active


    bold_font = Font(bold=True)

    # Добавляем заголовки для секции "Пользовательский охват опроса"
    ws.append(["Опрос", "Сколько пользователям отправлено"])

    # Получаем данные из моделей и добавляем их в таблицу
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))


    entries = PollUsersCount.objects.filter(created_at__range=(start_date, end_date))  # Здесь добавьте необходимые фильтры
    for entry in entries:
        ws.append([entry.poll.title, entry.users_count])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Пользовательский охват поста"
    ws.append(["Пост", "Сколько пользователям отправлено"])

    post_entries = PostUsersCount.objects.filter(created_at__range=(start_date, end_date))
    for entry in post_entries:
        ws.append([entry.post.text, entry.users_count])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Просмотры актуального/Новости"
    ws.append(["Актуальное/Новость", "Тип", "Сколько просмотров"])


    storynews_entries = []
    storynews = StoryNews.objects.all()
    for item in storynews:
        storynews_views_count = item.views.filter(created_at__range=(start_date, end_date)).count()
        storynews_entries.append([item, storynews_views_count])
    for entry in storynews_entries:
        ws.append([entry[0].name, entry[0].sort, entry[1]])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Просмотры товаров"
    ws.append(["Товар", "Сколько просмотров", "Сколько запросов на КП", "Сколько запросов чата менеджера"])

    product_entries = []
    products = Product.objects.all()
    for product in products:
        product_chat_count = product.chats.filter(created_at__range=(start_date, end_date)).count()
        product_kp_count = product.kps.filter(created_at__range=(start_date, end_date)).count()
        product_views_count = product.views.filter(created_at__range=(start_date, end_date)).count()
        product_entries.append([product, product_views_count, product_kp_count, product_chat_count])
    for entry in product_entries:
        ws.append([entry[0].name, entry[1], entry[2], entry[3]])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Просмотры категорий"
    ws.append(["Категория", "Сколько просмотров"])

    categories_entries = []
    categories = Category.objects.all()
    for category in categories:
        category_views_count = category.views.filter(created_at__range=(start_date, end_date)).count()
        categories_entries.append([category, category_views_count])
    categories_entries = categories_entries[1:]
    for entry in categories_entries:
        ws.append([f"{'>'.join(entry[0].get_level2()[0])}>{entry[0].name}", entry[1]])

    ws.append(['', '', ''])

    ws.append(["Количество регистраций"])

    users_entries = BotUser.objects.filter(created_at__range=(start_date, end_date)).count()
    ws.append([users_entries])

    # Создаем объект BytesIO для хранения Excel-файла в памяти
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    # Создаем HttpResponse с содержимым Excel-файла
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=statistic.xlsx'
    return response


class ManagerChatRequestCreateView(generics.CreateAPIView):
    queryset = ManagerChatRequest.objects.all()
    serializer_class = ManagerChatRequestSerializer


class KpRequestCreateView(generics.CreateAPIView):
    queryset = KpRequest.objects.all()
    serializer_class = KpRequestSerializer


def category_products(request, category_id, start_date=None, end_date=None):
    if start_date and end_date:
        start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))


    product_entries = []
    products = Product.objects.filter(category_id=category_id).annotate(views_count=Count('views')).order_by('-views_count')
    for product in products:
        product_chat_count = product.chats.filter(created_at__range=(start_date, end_date)).count()
        product_kp_count = product.kps.filter(created_at__range=(start_date, end_date)).count()
        product_views_count = product.views.filter(created_at__range=(start_date, end_date)).count()
        product_entries.append([product, product_views_count, product_kp_count, product_chat_count])


    context = {'product_entries': product_entries}
    return render(request, 'bot_statistics/category_products.html', context)
