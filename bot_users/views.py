from rest_framework.generics import CreateAPIView, ListAPIView
from .models import BotUser, BotUserGroup, ExtendedUser
from .serializers import BotUserSerializer, ActivateUserSerializer, UserSerializer, ManagerRegistrationSerializer, BotUserExistsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from django.http import HttpResponse
from openpyxl.styles import Font
import xlsxwriter
from django.http import HttpResponse
from rest_framework import generics
from .models import BotUser
from .serializers import BotUserCitySerializer, BotUserSearchSerializer
from django.utils.timezone import make_aware
from datetime import datetime
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import AbstractUser, User


from .models import User  # Импортируйте вашу модель User
from .services import (
    get_approved_posts_of_manager,
    get_not_approved_posts_of_manager,
    get_approved_polls_of_manager,
    get_not_approved_polls_of_manager,
    get_approved_news_of_manager,
    get_not_approved_news_of_manager,
    get_approved_stories_of_manager,
    get_not_approved_stories_of_manager,
    get_chat_requests_of_manager,
    get_kp_requests_of_manager
)
from src.permissions import IsStaffAndSuperuser


class BotUserCreateView(CreateAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class ProductManagerListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsStaffAndSuperuser]

    def get_queryset(self):
        return User.objects.filter(extended_user__product_manager=True)


class ActivateUserView(APIView):
    permission_classes = [IsStaffAndSuperuser]
    def put(self, request, user_id):
        try:
            user = BotUser.objects.get(user_id=user_id)
        except BotUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActivateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "User activated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def update_last_interaction(request):
    permission_classes = [IsStaffAndSuperuser]
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id is required in the request body.'}, status=400)

    user = get_object_or_404(BotUser, user_id=user_id)
    user.last_interaction = timezone.now()
    user.save()
    return Response({'message': 'Last interaction updated successfully.'})


class ManagerView(APIView):
    permission_classes = [IsStaffAndSuperuser]
    def get(self, request):
        message = "This endpoint is for user registration. Send a POST request with 'username', 'password', and 'bot_user_id' to register."
        return Response({'message': message})

    def post(self, request):
        serializer = ManagerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BotUserListView(ListAPIView):
#     queryset = BotUser.objects.all()
#     serializer_class = BotUserSerializer

class BotUserListView(ListAPIView):
    permission_classes = [IsStaffAndSuperuser]
    serializer_class = BotUserSerializer

    def get_queryset(self):
        group_id = self.request.GET.get('group_id')

        if group_id:
            try:
                group = BotUserGroup.objects.get(id=group_id)
                return group.members.all()
            except BotUserGroup.DoesNotExist:
                return BotUser.objects.none()
        else:
            return BotUser.objects.all()


@login_required  # Декоратор, чтобы обеспечить доступ только для авторизованных пользователей
def manager_results(request):
    permission_classes = [IsStaffAndSuperuser]
    action = request.POST.get('action')
    if action == 'get_results':
        if request.method == 'POST':
            selected_managers = request.POST.getlist('managers')
            if not selected_managers:
                return HttpResponse("Выберите хотя бы одного менеджера.")
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Преобразуйте строки с датами в объекты datetime
            start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))

            results = {}

            try:
                for manager_id in selected_managers:
                    manager = User.objects.get(pk=manager_id)
                    results[manager.username] = {
                        'approved_posts': get_approved_posts_of_manager(manager, start_date, end_date),
                        'not_approved_posts': get_not_approved_posts_of_manager(manager, start_date, end_date),
                        'approved_polls': get_approved_polls_of_manager(manager, start_date, end_date),
                        'not_approved_polls': get_not_approved_polls_of_manager(manager, start_date, end_date),
                        'approved_news': get_approved_news_of_manager(manager, start_date, end_date),
                        'not_approved_news': get_not_approved_news_of_manager(manager, start_date, end_date),
                        'approved_stories': get_approved_stories_of_manager(manager, start_date, end_date),
                        'not_approved_stories': get_not_approved_stories_of_manager(manager, start_date, end_date),
                        'requests_for_chat': get_chat_requests_of_manager(manager.username, start_date, end_date),
                        'requests_for_kp': get_kp_requests_of_manager(manager.username, start_date, end_date),
                    }

                results['category'] = manager.extended_user.category.name

                return render(request, 'bot_users/manager_results.html', {'results': results})

            except (AttributeError, ExtendedUser.DoesNotExist):
                return HttpResponse("Свяжите выбранного менеджера с пользователем бота (поле 'Телеграм-пользователь менеджера')")

    elif action == 'download_excel':
        selected_managers = request.POST.getlist('managers')
        if not selected_managers:
                return HttpResponse("Выберите хотя бы одного менеджера.")
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Преобразуйте строки с датами в объекты datetime
        start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))
        results = []

        try:
            for manager_id in selected_managers:
                manager = User.objects.get(pk=manager_id)
                manager_data = {
                    'username': manager.username,
                    'approved_posts': get_approved_posts_of_manager(manager, start_date, end_date),
                    'not_approved_posts': get_not_approved_posts_of_manager(manager, start_date, end_date),
                    'approved_polls': get_approved_polls_of_manager(manager, start_date, end_date),
                    'not_approved_polls': get_not_approved_polls_of_manager(manager, start_date, end_date),
                    'approved_news': get_approved_news_of_manager(manager, start_date, end_date),
                    'not_approved_news': get_not_approved_news_of_manager(manager, start_date, end_date),
                    'approved_stories': get_approved_stories_of_manager(manager, start_date, end_date),
                    'not_approved_stories': get_not_approved_stories_of_manager(manager, start_date, end_date),
                    'requests_for_chat': get_chat_requests_of_manager(manager.username, start_date, end_date),
                    'requests_for_kp': get_kp_requests_of_manager(manager.username, start_date, end_date),
                }
                results.append(manager_data)

            # Create a new Excel workbook and add a worksheet
            output = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            output['Content-Disposition'] = 'attachment; filename="manager_results.xlsx"'
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            # Add headers
            headers = list(results[0].keys())
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header)

            # Add data
            for row_num, data in enumerate(results, start=1):
                for col_num, value in enumerate(data.values()):
                    worksheet.write(row_num, col_num, value)

            # Close the Excel workbook
            workbook.close()

            return output

        except (AttributeError, ExtendedUser.DoesNotExist):
                return HttpResponse("Свяжите выбранного менеджера с пользователем бота (поле 'Телеграм-пользователь менеджера')")



    managers = User.objects.filter(is_staff=True)
    return render(request, 'bot_users/select_managers.html', {'managers': managers})



class CheckBotUserExistsView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({'error': 'Missing user_id'}, status=status.HTTP_400_BAD_REQUEST)

        bot_user_exists = BotUser.objects.filter(user_id=user_id).exists()
        serializer = BotUserExistsSerializer(bot_user_exists)
        return Response(serializer.data)


class CheckBotUserActivatedView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({'error': 'Missing user_id'}, status=status.HTTP_400_BAD_REQUEST)

        bot_user_exists = BotUser.objects.filter(user_id=user_id, activated=True).exists()
        serializer = BotUserExistsSerializer(bot_user_exists)
        return Response(serializer.data)


class UsersWithCategoryAPIView(APIView):
    def get(self, request, product_id):
        try:
            # Находим продукт по product_id
            product = Product.objects.get(id=product_id)

            # Получаем категорию продукта
            product_category = product.category

            # Находим связанных пользователей через ExtendedUser с этой категорией
            users_with_category = ExtendedUser.objects.filter(category=product_category)

            # Сериализуем пользователей (при необходимости)
            serialized_users = [{'username': user.user.username, 'category': product_category.name, 'telegram_username': user.bot_user.username, 'telegram_id': user.bot_user.user_id} for user in users_with_category]

            return Response(serialized_users, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден.'}, status=status.HTTP_404_NOT_FOUND)



class BotUserCityUpdateView(generics.UpdateAPIView):
    permission_classes = [IsStaffAndSuperuser]
    queryset = BotUser.objects.all()
    serializer_class = BotUserCitySerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        return BotUser.objects.get(user_id=user_id)



class BotUserSearchView(APIView):
    def get(self, request, username, format=None):
        try:
            bot_user = BotUser.objects.get(username=username)
        except BotUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BotUserSearchSerializer(bot_user)
        return Response(serializer.data)


class BotUserSearchByIdView(APIView):
    def get(self, request, user_id, format=None):
        try:
            bot_user = BotUser.objects.get(user_id=user_id)
        except BotUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BotUserSearchSerializer(bot_user)
        return Response(serializer.data)


@login_required(login_url='/admin/login/')
def dashboard_view(request):
    return render(request, 'bot_users/dashboard.html')
