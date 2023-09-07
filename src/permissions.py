from rest_framework import permissions

class IsStaffAndSuperuser(permissions.BasePermission):
    """
    Пользователь с атрибутами is_staff и is_superuser имеет доступ.
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_staff or user.is_superuser)
