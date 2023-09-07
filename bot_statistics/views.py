from rest_framework import generics
from .models import PollUsersCount, PostUsersCount, StoryNewsViews, ProductViews, CategoryViews, ManagerChatRequest
from .serializers import PollUsersCountSerializer, PostUsersCountSerializer, StoryNewsViewsSerializer, ProductViewsSerializer, CategoryViewsSerializer, ManagerChatRequestSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models.functions import TruncMonth
from src.permissions import IsStaffAndSuperuser
from django.contrib.auth.decorators import login_required

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

@login_required
def poll_users_count(request):
    permission_classes = [IsStaffAndSuperuser]
    selected_month = request.GET.get('month')  # Получение параметра из запроса
    if selected_month is None:
        selected_month = timezone.now().month

    entries = PollUsersCount.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    posts_entries = PostUsersCount.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    storynews_entries = StoryNewsViews.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    products_entries = ProductViews.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    categories_entries = CategoryViews.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)

    return render(request, 'bot_statistics/poll_users_count.html', {'entries': entries, 'posts_entries': posts_entries, 'storynews_entries': storynews_entries, 'products_entries': products_entries, 'categories_entries': categories_entries, 'selected_month': selected_month})


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
    selected_month = request.GET.get('month')


    entries = PollUsersCount.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)  # Здесь добавьте необходимые фильтры
    for entry in entries:
        ws.append([entry.poll.title, entry.users_count])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Пользовательский охват поста"
    ws.append(["Пост", "Сколько пользователям отправлено"])

    post_entries = PostUsersCount.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    for entry in post_entries:
        ws.append([entry.post.text, entry.users_count])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Просмотры актуального/Новости"
    ws.append(["Актуальное/Новость", "Тип", "Сколько просмотров"])


    storynews_entries = StoryNewsViews.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    for entry in storynews_entries:
        ws.append([entry.item.name, entry.item.sort, entry.views])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Просмотры товаров"
    ws.append(["Товар", "Сколько просмотров"])

    product_entries = ProductViews.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    for entry in product_entries:
        ws.append([entry.product.name, entry.views])

    ws.append(['', '', ''])

    # Добавляем заголовки для секции "Просмотры категорий"
    ws.append(["Категория", "Сколько просмотров"])

    category_entries = CategoryViews.objects.filter(created_at__year=timezone.now().year, created_at__month=selected_month)
    for entry in category_entries:
        ws.append([f"{'>'.join(entry.category.get_level2()[0])}>{entry.category.name}", entry.views])

    ws.append(['', '', ''])

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
